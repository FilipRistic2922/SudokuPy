import unittest
import time
from sudoku.solver import ExactCoverSolver, BacktrackingSolver


class TestSolver(unittest.TestCase):
    boards = [
        # Easy
        [[0, 0, 0, 2, 6, 0, 7, 0, 1],
         [6, 8, 0, 0, 7, 0, 0, 9, 0],
         [1, 9, 0, 0, 0, 4, 5, 0, 0],
         [8, 2, 0, 1, 0, 0, 0, 4, 0],
         [0, 0, 4, 6, 0, 2, 9, 0, 0],
         [0, 5, 0, 0, 0, 3, 0, 2, 8],
         [0, 0, 9, 3, 0, 0, 0, 7, 4],
         [0, 4, 0, 0, 5, 0, 0, 3, 6],
         [7, 0, 3, 0, 1, 8, 0, 0, 0]],
        # Hard
        [[0, 0, 0, 6, 0, 0, 4, 0, 0],
         [7, 0, 0, 0, 0, 3, 6, 0, 0],
         [0, 0, 0, 0, 9, 1, 0, 8, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 5, 0, 1, 8, 0, 0, 0, 3],
         [0, 0, 0, 3, 0, 6, 0, 4, 5],
         [0, 4, 0, 2, 0, 0, 0, 6, 0],
         [9, 0, 3, 0, 0, 0, 0, 0, 0],
         [0, 2, 0, 0, 0, 0, 1, 0, 0]],
        # Extra Hard
        [[0, 2, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 6, 0, 0, 0, 0, 3],
         [0, 7, 4, 0, 8, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 3, 0, 0, 2],
         [0, 8, 0, 0, 4, 0, 0, 1, 0],
         [6, 0, 0, 5, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 7, 8, 0],
         [5, 0, 0, 0, 0, 9, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 4, 0]]

    ]

    correct_solutions = [
        [[4, 3, 5, 2, 6, 9, 7, 8, 1],
         [6, 8, 2, 5, 7, 1, 4, 9, 3],
         [1, 9, 7, 8, 3, 4, 5, 6, 2],
         [8, 2, 6, 1, 9, 5, 3, 4, 7],
         [3, 7, 4, 6, 8, 2, 9, 1, 5],
         [9, 5, 1, 7, 4, 3, 6, 2, 8],
         [5, 1, 9, 3, 2, 6, 8, 7, 4],
         [2, 4, 8, 9, 5, 7, 1, 3, 6],
         [7, 6, 3, 4, 1, 8, 2, 5, 9]],
        [[5, 8, 1, 6, 7, 2, 4, 3, 9],
         [7, 9, 2, 8, 4, 3, 6, 5, 1],
         [3, 6, 4, 5, 9, 1, 7, 8, 2],
         [4, 3, 8, 9, 5, 7, 2, 1, 6],
         [2, 5, 6, 1, 8, 4, 9, 7, 3],
         [1, 7, 9, 3, 2, 6, 8, 4, 5],
         [8, 4, 5, 2, 1, 9, 3, 6, 7],
         [9, 1, 3, 7, 6, 8, 5, 2, 4],
         [6, 2, 7, 4, 3, 5, 1, 9, 8]],
        [[1, 2, 6, 4, 3, 7, 9, 5, 8],
         [8, 9, 5, 6, 2, 1, 4, 7, 3],
         [3, 7, 4, 9, 8, 5, 1, 2, 6],
         [4, 5, 7, 1, 9, 3, 8, 6, 2],
         [9, 8, 3, 2, 4, 6, 5, 1, 7],
         [6, 1, 2, 5, 7, 8, 3, 9, 4],
         [2, 6, 9, 3, 1, 4, 7, 8, 5],
         [5, 4, 8, 7, 6, 9, 2, 3, 1],
         [7, 3, 1, 8, 5, 2, 6, 4, 9]]]

    #   Test for ExactCoverSolver
    #   Solving all 3 boards takes between ~30ms
    def test_exact_cover_solver(self):
        solver = ExactCoverSolver()

        for i, board in enumerate(self.boards):
            with self.subTest("Board {} Test".format(i)):
                time_start = int(time.time()*1000.0)
                solver_solution = solver.solve(board)
                time_end = int(time.time()*1000.0)
                print("Solving Board {} took {} ms".format(i+1, round(time_end - time_start, 3)))
                self.assertEqual(self.correct_solutions[i], solver_solution, "Solution doesn't match")

    #   Test for BackTrackingSolver
    #   Solving all 3 boards takes ~17s
    def test_back_tracking_solver(self):
        solver = BacktrackingSolver()

        for i, board in enumerate(self.boards):
            with self.subTest("Board {} Test".format(i)):
                time_start = int(time.time()*1000.0)
                solver_solution = solver.solve(board)
                time_end = int(time.time()*1000.0)
                print("Solving Board {} took {} ms".format(i+1, round(time_end - time_start, 2)))
                self.assertEqual(self.correct_solutions[i], solver_solution, "Solution doesn't match")


if __name__ == '__main__':
    unittest.main()
