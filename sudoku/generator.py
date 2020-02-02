import random
from enum import Enum
from sudoku.solver import ExactCoverSolver


class Difficulty(Enum):
    EASY = 38
    NORMAL = 32
    HARD = 28
    VERY_HARD = 25


def generate_board(difficulty: Difficulty):
    generator = ExactCoverSolver(generator=True)
    solver = ExactCoverSolver()

    board = [_empty_row() for i in range(9)]
    random_row_index = random.randint(0, 8)
    board[random_row_index] = _randomize_row()

    generated_board = generator.solve(board)

    invalid_boards = 0

    while _count_empty(generated_board) < 81 - difficulty.value:
        row, col, val = _remove_random_element(generated_board)
        # Skip is value was already 0
        if val == 0:
            invalid_boards += 1
            # We got bad rng try again from start
            if invalid_boards == 80:
                return generate_board(difficulty)
            continue
        solved = solver.solve(generated_board)
        if not solved:
            generated_board[row][col] = val
    return generated_board


def _remove_random_element(board: [[]]):
    rand_row = random.randint(0, 8)
    rand_col = random.randint(0, 8)
    val = board[rand_row][rand_col]
    if val != 0:
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
