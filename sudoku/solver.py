from itertools import product


def copy_board(board: [[]]):
    new_board = []
    for i, row in enumerate(board):
        new_board.append(list(row))
    return new_board


def find_empty_cell(board: [[]]):
    for i, j in product(range(len(board)), range(len(board[0]))):
        if board[i][j] == 0:
            return i, j  # row, col tuple
    return None


def is_valid(board: [[]], row: int, col: int, val: int):
    # Checks row
    for i in range(len(board[0])):
        if board[row][i] == val and col != i:
            return False

    # Checks column
    for i in range(len(board)):
        if board[i][col] == val and row != i:
            return False

    # Checks inner grid
    inner_x = col // 3
    inner_y = row // 3

    for i, j in product(range(inner_y * 3, inner_y * 3 + 3), range(inner_x * 3, inner_x * 3 + 3)):
        if board[i][j] == val and i != row and j != col:
            return False

    return True


class SudokuSolver:

    def __init__(self, name: str):
        self.name = name
        self.on_next_step = self._on_next_pass

    def _on_next_pass(self, row: int, col: int, val: int):
        pass

    def solve(self, board: [[]], on_next_step):
        pass


class BacktrackingSolver(SudokuSolver):

    def __init__(self):
        super().__init__("Backtracking")
        self.on_next_step = self._on_next_pass

    def solve(self, board: [[]], on_next_step=None):

        if on_next_step:
            self.on_next_step = on_next_step

        board_copy = copy_board(board)
        self._solve(board_copy)
        return board_copy

    def _solve(self, board: [[]]):
        empty_cell = find_empty_cell(board)
        if not empty_cell:
            return True
        else:
            row, col = empty_cell

        for val in range(1, 10):
            if is_valid(board, row, col, val):
                board[row][col] = val
                if self.on_next_step:
                    self.on_next_step(row, col, val)

                if self._solve(board):
                    return True
                if self.on_next_step:
                    self.on_next_step(row, col, 0)
                board[row][col] = 0


class ExactCoverSolver(SudokuSolver):

    def __init__(self, generator=False):
        super().__init__("Exact Cover")
        self.on_next_step = self._on_next_pass
        self.inner_grid_size = 3
        self.grid_size = 9
        self.generator = generator

    def solve(self, board: [[]], on_next_step=None):
        new_solution = []
        board_copy = copy_board(board)

        if on_next_step:
            self.on_next_step = on_next_step

        for solution in self._solve(board_copy):
            new_solution += solution
            # Generator case should return first possible solution
            if self.generator and len(new_solution) == 9:
                return new_solution
            # In solver case, if there are more possible solutions we return None since its illegal
            if not self.generator and len(new_solution) > 9:
                return None
        return new_solution

    def _solve(self, board: [[]]):

        choices = ([("rc", rc) for rc in product(range(self.grid_size), range(self.grid_size))] +
                   [("rv", rv) for rv in product(range(self.grid_size), range(1, self.grid_size + 1))] +
                   [("cv", cv) for cv in product(range(self.grid_size), range(1, self.grid_size + 1))] +
                   [("gv", gv) for gv in product(range(self.grid_size), range(1, self.grid_size + 1))])

        constraints = {}

        for row, col, value in product(range(self.grid_size), range(self.grid_size), range(1, self.grid_size + 1)):
            inner_grid = (row // self.inner_grid_size) * self.inner_grid_size + (col // self.inner_grid_size)
            constraints[(row, col, value)] = [
                ("rc", (row, col)),
                ("rv", (row, value)),
                ("cv", (col, value)),
                ("gv", (inner_grid, value))]

        choices, constraints = self._exact_cover(choices, constraints)

        # Passing thru all occupied cells
        for i, row in enumerate(board):
            for j, value in enumerate(row):
                if value:
                    self._choose(choices, constraints, (i, j, value))

        for solution in self._solver(choices, constraints, []):
            for (row, col, value) in solution:
                board[row][col] = value
            yield board

    # Creates exact cover by linking choices and constraints
    def _exact_cover(self, choices: [], constraints: dict):
        choices = {j: set() for j in choices}
        for i, row in constraints.items():
            for j in row:
                choices[j].add(i)
        return choices, constraints

    def _solver(self, choices: dict, constraints: dict, solution: [(int, int, int)]):
        # No more choices left
        if len(choices) == 0:
            yield list(solution)
        else:
            # Take constraint with lowest number of choices
            best_constraint = min(choices, key=lambda c: len(choices[c]))

            # Iterate all choices for constraint and try each choice as solution
            for choice in list(choices[best_constraint]):
                solution.append(choice)
                col_solution = self._choose(choices, constraints, choice)
                for solution in self._solver(choices, constraints, solution):
                    yield solution
                self._unchoose(choices, constraints, choice, col_solution)
                solution.pop()

    # Chooses given choice, removing all choices that are not correct with given choice
    def _choose(self, choices: dict, constraints: dict, choice: (int, int, int)):
        column_solution = []
        row, col, val = choice

        self.on_next_step(row, col, val)
        for i in constraints[choice]:
            for j in choices[i]:
                for k in constraints[j]:
                    if k != i:
                        choices[k].remove(j)

            column_solution.append(choices.pop(i))
        return column_solution

    # Recalls previous choice, restoring the state to be same as before the choice was made
    def _unchoose(self, choices: dict, constraints: dict, choice: (int, int, int), cols: [(int, int, int)]):
        for i in reversed(constraints[choice]):
            choices[i] = cols.pop()
            for j in choices[i]:
                for k in constraints[j]:
                    if k != i:
                        choices[k].add(j)
