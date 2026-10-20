from pieces.piece import Piece


class Rook(Piece):
    """Classe représentant la Tour. Se déplace en ligne droite."""

    def __str__(self):
        """Retourne l'identifiant de la Tour."""
        return 'R'

    def isValidMove(self, newPosition, board):
        """
        Vérifie si le déplacement est valide pour une Tour.

        Args:
            newPosition (Position): position de destination
            board (Board): plateau de jeu

        Returns:
            bool: True si le mouvement est valide
        """
        dc = abs(newPosition.col_index() - self._position.col_index())
        dr = abs(newPosition.row_index() - self._position.row_index())

        if (dc == 0 and dr == 0) or (dc != 0 and dr != 0):
            return False

        return (self._is_path_clear(newPosition, board) and
                self._destination_free_or_enemy(newPosition, board))


if __name__ == "__main__":
    print("Tests Rook OK !")