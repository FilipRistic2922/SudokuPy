import pygame
from pygame.locals import *
import pygameMenu

from gui_state.gui_state import GuiState

from gui_state.state_manager import StateManager
from sudoku.generator import Difficulty


class MainMenu(GuiState):

    def __init__(self, width, height, font: str, state_manager: StateManager):
        super().__init__('main_menu', state_manager)
        self.width = width
        self.height = height
        self.font = font
        self.menu = None
        self.win = None
        self.background_image = pygame.image.load("assets/menu_background.jpg").convert()
        self.data_out = {"diff": Difficulty.EASY, "solver_index": 0}

    def on_start(self, win):
        self.win = win
        if self.menu:
            self.menu.enable()
        else:
            self.menu = pygameMenu.Menu(win, self.width, self.height, back_box=False,
                                        menu_width=800,
                                        menu_height=640,
                                        draw_select=True,
                                        option_margin=50,
                                        bgfun=self.draw_background,
                                        font=self.font, title="Main Menu", dopause=True)
            self.menu.set_fps(60, True)

            self.menu.add_option("Start Game", self.on_start_game)
            self.menu.add_selector("Algorithm",
                                   [("Backtracking", 0), ("Exact Cover", 1)],
                                   selector_id="selector_solver",
                                   default=0,
                                   onchange=self.on_change_solver)
            self.menu.add_selector("Difficulty",
                                   [("Easy", Difficulty.EASY),
                                    ("Normal", Difficulty.NORMAL),
                                    ("Hard", Difficulty.HARD),
                                    ("Very Hard", Difficulty.VERY_HARD)],
                                   selector_id="selector_level",
                                   default=0,
                                   onchange=self.on_change_level)
            self.menu.add_option("Exit", pygameMenu.events.EXIT)

    def on_start_game(self):
        self.menu.disable()
        self.next_state = "play_game"

    def draw_background(self):
        self.win.blit(self.background_image, (0, 0))

    def on_change_solver(self, *args, **kwargs):
        self.data_out["solver_index"] = args[1]

    def on_change_level(self, *args, **kwargs):
        self.data_out["diff"] = args[1]

    def update(self, win, time_delta):
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                self.quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit = True
        if self.menu:
            self.menu.mainloop(events)
            self.menu.draw()
