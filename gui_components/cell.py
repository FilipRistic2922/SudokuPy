import pygame

from gui_components.gui_util import get_font, BLACK, BLUE, GRAY


class Cell:

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.set_by_user = False
        self.selected = False

    def draw(self, win):
        font = get_font("arial", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, GRAY)
            win.blit(text, (x + 45, y + 5))
        elif not (self.value == 0):
            color = BLACK
            if self.set_by_user:
                color = BLUE
            text = font.render(str(self.value), 1, color)
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, BLUE, (x, y, gap, gap), 5)

    def set_value(self, val, set_by_user: bool = False):
        self.value = val
        self.temp = 0
        self.set_by_user = set_by_user

    def set_temp(self, val):
        self.value = 0
        self.temp = val
