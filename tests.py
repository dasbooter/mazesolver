import unittest
from main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_zero_size(self):
        num_cols = 0
        num_rows = 0
        m2 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m2._cells), 0)

    def test_maze_non_square(self):
        num_cols = 15
        num_rows = 5
        m3 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m3._cells), num_cols)
        self.assertEqual(len(m3._cells[0]), num_rows)

    def test_maze_negative_size(self):
        num_cols = -5
        num_rows = -10
        with self.assertRaises(ValueError):
            Maze(0, 0, num_rows, num_cols, 10, 10)

    def test_maze_large_size(self):
        num_cols = 100
        num_rows = 100
        m4 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m4._cells), num_cols)
        self.assertEqual(len(m4._cells[0]), num_rows)

    def test_break_entrance_and_exit(self):
        num_cols = 10
        num_rows = 10
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        # Entrance cell should have no top wall
        self.assertFalse(m._cells[0][0].has_top_wall)
        # Exit cell should have no bottom wall
        self.assertFalse(m._cells[num_cols - 1][num_rows - 1].has_bottom_wall)

    def test_all_cells_visited(self):
        num_cols = 10
        num_rows = 10
        m = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertTrue(m._cells[i][j].visited)

    def test_reset_cells_visited(self):
        num_cols = 5
        num_rows = 5
        m = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)
        # After maze generation, all cells should be visited
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertTrue(m._cells[i][j].visited)
        # Now reset the visited status
        m._reset_cells_visited()
        # Now all cells should have visited == False
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertFalse(m._cells[i][j].visited)

if __name__ == "__main__":
    unittest.main()
