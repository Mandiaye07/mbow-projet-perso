from pieces.piece import Piece
from position import Position


class Pawn(Piece):
    """Classe représentant le Pion. Se déplace vers l'avant."""

    def __str__(self):
        """Retourne l'identifiant du Pion."""
        return 'P'

    def isValidMove(self, newPosition, board):
        """
        Vérifie si le déplacement est valide pour un Pion.

        Args:
            newPosition (Position): position de destination
            board (Board): plateau de jeu

        Returns:
            bool: True si le mouvement est valide
        """
        direction = 1 if self._color == 0 else -1
        start_row = 1 if self._color == 0 else 6

        c1, r1 = self._position.col_index(), self._position.row_index()
        c2, r2 = newPosition.col_index(), newPosition.row_index()

        dc = c2 - c1
        dr = r2 - r1

        target = board.getPiece(newPosition)

        # Avance d'une case
        if dc == 0 and dr == direction:
            return target is None

        # Avance de deux cases depuis la position initiale
        if dc == 0 and dr == 2 * direction and r1 == start_row:
            inter = Position.from_indices(c1, r1 + direction)
            return target is None and board.getPiece(inter) is None

        # Capture en diagonale
        if abs(dc) == 1 and dr == direction:
            return target is not None and target.color != self._color

        return False


if __name__ == "__main__":
    print("Tests Pawn OK !")