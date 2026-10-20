import unittest
import sys
sys.path.append('..')
from position import Position
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.rook import Rook
from board import Board


class TestKing(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_valid_move(self):
        king = King(Position('e', 4), 0)
        self.assertTrue(king.isValidMove(Position('e', 5), self.board))

    def test_invalid_move(self):
        king = King(Position('e', 4), 0)
        self.assertFalse(king.isValidMove(Position('e', 6), self.board))


class TestKnight(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_valid_move(self):
        knight = Knight(Position('b', 1), 0)
        self.assertTrue(knight.isValidMove(Position('c', 3), self.board))

    def test_invalid_move(self):
        knight = Knight(Position('b', 1), 0)
        self.assertFalse(knight.isValidMove(Position('b', 3), self.board))


class TestPawn(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_valid_move(self):
        pawn = Pawn(Position('e', 2), 0)
        self.assertTrue(pawn.isValidMove(Position('e', 3), self.board))

    def test_double_move(self):
        pawn = Pawn(Position('e', 2), 0)
        self.assertTrue(pawn.isValidMove(Position('e', 4), self.board))


if __name__ == '__main__':
    unittest.main()