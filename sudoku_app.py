#!/usr/bin/env python3
import os

import pygame

from gui_state.menu_state import MainMenu
from gui_state.game_state import GameState
from gui_state.state_manager import StateManager


def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.key.set_repeat()
    win_width = 830
    win_height = 640
    pygame.display.set_caption('Sudoku')
    win = pygame.display.set_mode((win_width, win_height))

    state_manager = StateManager(win)
    main_menu = MainMenu(win_width, win_height, 'segoeuiblack', state_manager)
    GameState(state_manager)
    state_manager.set_initial_state(main_menu.name)

    clock = pygame.time.Clock()
    running = True

    while running:
        frame_time = clock.tick(60)
        time_delta = min(frame_time / 1000.0, 0.1)

        state_manager.update(time_delta)
        running = not state_manager.quit
        pygame.display.flip()  # flip all our drawn stuff onto the screen

    pygame.quit()  # exited game loop so quit pygame


if __name__ == '__main__':
    main()
