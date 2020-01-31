import random
from enum import Enum
from sudoku.sudoku_solver import ExactCoverSolver


class SudokuLevel(Enum):
    EASY = 45
    NORMAL = 32
    HARD = 25
    VERY_HARD = 17


def generate_board(level: SudokuLevel):
    solver = ExactCoverSolver()

    board = [_empty_row() for i in range(9)]
    random_row_index = random.randint(0, 8)
    board[random_row_index] = _randomize_row()

    generated_board = solver.solve(board)

    while _count_empty(generated_board) < 81 - level.value:
        row, col, val = _remove_random_element(generated_board)

        solved = solver.solve(generated_board)
        count = _count_empty(solved)
        if count != 0:
            generated_board[row][col] = val
        # return emptied_board
    return generated_board


def _remove_random_element(board: [[]]):
    rand_row = random.randint(0, 8)
    rand_col = random.randint(0, 8)
    val = board[rand_row][rand_col]
    board[rand_row][rand_col] = 0
    return rand_row, rand_col, val


def _count_empty(board: [[]]):
    counter = 0
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == 0:
                counter += 1
    return counter


def _randomize_row():
    row = list(range(1, 10))
    random.shuffle(row)
    return row


def _empty_row():
    return [0] * 9
