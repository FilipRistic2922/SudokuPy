import time

from gui_state.gui_state import GuiState
from gui_state.state_manager import StateManager
from gui_components.grid import Grid
from gui_components.gui_util import *
from sudoku.solver import *
from sudoku.generator import generate_board


class GameState(GuiState):
    solvers = [BacktrackingSolver(), ExactCoverSolver()]

    def __init__(self, state_manager: StateManager):
        super().__init__('play_game', state_manager)
        self.level = None
        self.solver_index = 0
        self.solver = self.solvers[self.solver_index]
        self.board = None
        self.grid = None
        self.font = get_font("arialblack", 24)
        self.solving = False
        self.btn_new = PygButton((660, 150, 150, 36), 'New', font=self.font)
        self.btn_reset = PygButton((660, 200, 150, 36), 'Reset', font=self.font)
        self.btn_solve = PygButton((660, 250, 150, 36), 'Solve', font=self.font)
        self.btn_check = PygButton((660, 300, 150, 36), 'Check', font=self.font)
        self.btn_menu = PygButton((660, 350, 150, 36), 'Menu', font=self.font)
        self.btn_solver = PygButton((660, 400, 150, 36), 'Algorithm', font=self.font)
        self.buttons = (self.btn_new, self.btn_solve, self.btn_check, self.btn_reset, self.btn_menu, self.btn_solver)
        self.key = None
        self.start_time = None
        self.solve_event = pygame.USEREVENT + 1
        self.step_timer = 200
        self.steps = []
        self.solving_dots = 0
        self.solved = False

    def on_start(self, win):
        self.level = self.data_in["diff"]
        self.solver_index = self.data_in["solver_index"]
        self.solver = self.solvers[self.solver_index]
        self.board = generate_board(self.level)
        self.grid = Grid(self.board, 9, 9, 640, 640)
        pygame.time.set_timer(self.solve_event, self.step_timer)
        self.start_time = time.time()
        pass

    def update(self, win, time_delta):
        game_time = round(time.time() - self.start_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN and not self.solving:
                # Numbers 1-9 to set temporary value
                if pygame.K_0 < event.key <= pygame.K_9:
                    self.key = event.key - pygame.K_0
                # Delete or 0 to remove temporary
                if event.key == pygame.K_DELETE or event.key == pygame.K_0:
                    self.grid.clear()
                    self.key = None
                # Set as
                if event.key == pygame.K_RETURN and not self.solving:
                    i, j = self.grid.selected
                    if self.grid.cells[i][j].temp != 0:
                        self.grid.set_value(self.grid.cells[i][j].temp)
                        self.key = None

            if event.type == pygame.MOUSEBUTTONDOWN and not self.solving:
                pos = pygame.mouse.get_pos()
                clicked = self.grid.on_click(pos)
                if clicked:
                    self.grid.select(clicked[0], clicked[1])
                    self.key = None
            if 'click' in self.btn_new.handleEvent(event) and not self.solving:
                self.on_start(win)
            if 'click' in self.btn_reset.handleEvent(event) and not self.solving:
                self.start_time = time.time()
                self.solved = False
                self.grid.reset()
            if 'click' in self.btn_solve.handleEvent(event):
                if self.solving:
                    self.btn_solve.caption = "Solve"
                    self.steps.clear()
                    self.solving = False
                else:
                    self.grid.reset()
                    self.btn_solve.caption = "Solving" + ("." * self.solving_dots)
                    self.solver.solve(self.grid.board, lambda r, c, v: self.steps.append((r, c, v)))
                    self.solving = True
            if 'click' in self.btn_menu.handleEvent(event) and not self.solving:
                self.next_state = "main_menu"
            if 'click' in self.btn_check.handleEvent(event) and not self.solving:
                empty_cell = find_empty_cell(self.grid.board)
                if empty_cell is not None:
                    self.grid.select(empty_cell[0], empty_cell[1])
                else:
                    for i, j in product(range(len(self.grid.board)), range(len(self.grid.board[0]))):
                        if not is_valid(self.grid.board, i, j, self.grid.board[i][j]):
                            self.grid.select(i, j)
                            break
                        if i == 8 and j == 8:
                            self.solved = True

            if 'click' in self.btn_solver.handleEvent(event) and not self.solving:
                self.solver_index += 1
                if self.solver_index == len(self.solvers):
                    self.solver_index = 0

                self.solver = self.solvers[self.solver_index]
            if self.solving:
                if event.type == self.solve_event:
                    # Go step by step
                    if len(self.steps) > 0:
                        step = self.steps.pop(0)
                        row, col, val = step
                        self.grid.select(row, col)
                        self.grid.set_value(val, True)

                        if self.solving_dots == 3:
                            self.solving_dots = 0
                        else:
                            self.solving_dots += 1

                        self.btn_solve.caption = "Solving" + ("." * self.solving_dots)
                    else:
                        self.btn_solve.caption = "Solve"
                        self.solving = False

        if self.grid.selected and self.key is not None:
            self.grid.set_temp(self.key)

        # Update board
        self.draw_grid(win, self.grid, game_time)

        # Update all buttons
        for btn in self.buttons:
            btn.draw(win)

    def draw_grid(self, win, board, game_time):
        win.fill((255, 255, 255))
        # Draw time
        font = get_font("segoeui", 28)
        text = font.render(self.solver.name, 1, BLACK)
        win.blit(text, (660, 450))
        if self.solved:
            text = font.render("Solved", 1, GREEN)
            win.blit(text, (660, 500))
        else:
            text = font.render("Time: " + self.format_time(game_time), 1, BLACK)
            win.blit(text, (660, 500))
        # Draw grid and board
        board.draw(win)

    @staticmethod
    def format_time(sec):
        minute = sec // 60
        second = sec % 60
        formatted_time = " " + str(minute) + ":" + str(second)
        return formatted_time

    def on_end(self):
        self.level = None
        self.solver = None
        self.board = None
        self.grid = None
