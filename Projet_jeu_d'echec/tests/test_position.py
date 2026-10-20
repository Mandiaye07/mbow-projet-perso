import unittest
import sys
sys.path.append('..')
from position import Position


class TestPosition(unittest.TestCase):

    def test_str(self):
        p = Position('e', 4)
        self.assertEqual(str(p), 'e4')

    def test_col_index(self):
        p = Position('a', 1)
        self.assertEqual(p.col_index(), 0)
        p2 = Position('h', 1)
        self.assertEqual(p2.col_index(), 7)

    def test_row_index(self):
        p = Position('a', 1)
        self.assertEqual(p.row_index(), 0)

    def test_from_indices(self):
        p = Position.from_indices(4, 3)
        self.assertEqual(str(p), 'e4')

    def test_equality(self):
        p1 = Position('e', 4)
        p2 = Position('e', 4)
        self.assertEqual(p1, p2)

    def test_is_valid_indices(self):
        self.assertTrue(Position.is_valid_indices(0, 0))
        self.assertFalse(Position.is_valid_indices(8, 0))


if __name__ == '__main__':
    unittest.main()