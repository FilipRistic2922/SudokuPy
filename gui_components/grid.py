from itertools import product

import pygame

from gui_components.cell import Cell
from gui_components.gui_util import BLACK


class Grid:
    user_choices = []

    def __init__(self, board, rows, cols, width, height):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.selected = None

    def update(self):
        self.board = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def set_board(self, board: [[]]):
        self.board = board
        for i, j in product(range(self.cols), range(self.rows)):
            self.cells[i][j].set_value(board[i][j])

    def set_value(self, val, set_by_user: bool = True):
        row, col = self.selected
        if self.cells[row][col].value == 0 or self.cells[row][col].set_by_user:
            self.cells[row][col].set_value(val, set_by_user)
            self.update()

    def reset(self):
        for i, j in product(range(self.cols), range(self.rows)):
            cell = self.cells[i][j]
            if cell.set_by_user:
                cell.set_value(0)
        self.update()

    def set_temp(self, val):
        row, col = self.selected
        self.cells[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(win, BLACK, (0, i * gap), (self.width, i * gap), thickness)
            pygame.draw.line(win, BLACK, (i * gap, 0), (i * gap, self.height), thickness)

        # Draw cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(win)

    def select(self, row, col):
        # Reset
        if self.selected is not None:
            old_row, old_col = self.selected
            self.cells[old_row][old_col].selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        cell = self.cells[row][col]
        if cell.temp != 0:
            cell.set_temp(0)
        elif cell.value != 0:
            cell.set_value(0)

    def on_click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None
