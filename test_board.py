import unittest
import sys
sys.path.append('..')
from board import Board
from position import Position


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_get_piece(self):
        piece = self.board.getPiece(Position('e', 1))
        self.assertIsNotNone(piece)
        self.assertEqual(str(piece), 'K')

    def test_empty_square(self):
        piece = self.board.getPiece(Position('e', 4))
        self.assertIsNone(piece)

    def test_move_piece(self):
        self.board.movePiece(Position('e', 2), Position('e', 4))
        self.assertIsNotNone(self.board.getPiece(Position('e', 4)))
        self.assertIsNone(self.board.getPiece(Position('e', 2)))


if __name__ == '__main__':
    unittest.main()