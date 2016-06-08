import unittest
from board import Board
from disc import Disc


TEST_NUM_ROWS = 4
TEST_NUM_COLUMNS = 6
PINK = Disc('pink')
BROWN = Disc('brown')


class TestBoardBasics(unittest.TestCase):

    def setUp(self):
        self.board = Board(TEST_NUM_ROWS, TEST_NUM_COLUMNS)
        self.bottom_left = (self.board.bottom_row, self.board.left_column)
        self.bottom_right = (self.board.bottom_row, self.board.right_column)

    def test_board_dimensions(self):
        self.assertEqual(self.board.num_rows, TEST_NUM_ROWS)
        self.assertEqual(self.board.num_columns, TEST_NUM_COLUMNS)

    def test_board_extremes(self):
        self.assertEqual(self.board.left_column, 0)
        self.assertEqual(self.board.right_column, TEST_NUM_COLUMNS - 1)
        self.assertEqual(self.board.top_row, 0)
        self.assertEqual(self.board.bottom_row, TEST_NUM_ROWS - 1)

    def test_grid_dimensions(self):
        self.assertEqual(len(self.board.grid), TEST_NUM_ROWS)
        self.assertEqual(len(self.board.grid[0]), TEST_NUM_COLUMNS)

    def test_grid_size(self):
        num_positions = 0
        for i in self.board.grid:
            for j in i:
                num_positions += 1
        self.assertEqual(num_positions, TEST_NUM_ROWS * TEST_NUM_COLUMNS)

    def test_add_disc_out_of_bounds_left(self):
        with self.assertRaises(ValueError):
            self.board.add_disc(PINK, self.board.left_column - 1)

    def test_add_disc_out_of_bounds_right(self):
        with self.assertRaises(ValueError):
            self.board.add_disc(PINK, self.board.right_column + 1)

    def test_add_and_get_one_disc_left_column(self):
        self.board.add_disc(PINK, self.board.left_column)
        self.assertEqual(PINK, self.board.get_disc(self.bottom_left))
        self.assertIsNone(self.board.get_disc(self.bottom_right))

    def test_add_and_get_one_disc_right_column(self):
        self.board.add_disc(PINK, self.board.right_column)
        self.assertEqual(PINK, self.board.get_disc(self.bottom_right))
        self.assertIsNone(self.board.get_disc(self.bottom_left))
