import unittest

from sudoku.solver import ExactCoverSolver, BacktrackingSolver
from sudoku.generator import generate_board, Difficulty


class TestGenerator(unittest.TestCase):

    #   Test for ExactCoverSolver
    #   Solving all 3 boards takes between ~30ms
    def test_generator(self):
        for level in Difficulty:
            with self.subTest("Level {} Test".format(level)):
                generated_board = generate_board(level)
            backtracking_solver = BacktrackingSolver()
            exact_cover_solver = ExactCoverSolver()
            backtracking_solution = backtracking_solver.solve(generated_board)
            exact_cover_solution = exact_cover_solver.solve(generated_board)
            self.assertEqual(backtracking_solution, exact_cover_solution, "Solutions don't match")


if __name__ == '__main__':
    unittest.main()
