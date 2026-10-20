from pieces.piece import Piece


class Bishop(Piece):
    """Classe représentant le Fou. Se déplace en diagonale."""

    def __str__(self):
        """Retourne l'identifiant du Fou."""
        return 'B'

    def isValidMove(self, newPosition, board):
        """
        Vérifie si le déplacement est valide pour un Fou.

        Args:
            newPosition (Position): position de destination
            board (Board): plateau de jeu

        Returns:
            bool: True si le mouvement est valide
        """
        dc = abs(newPosition.col_index() - self._position.col_index())
        dr = abs(newPosition.row_index() - self._position.row_index())

        if dc == 0 or dc != dr:
            return False

        return (self._is_path_clear(newPosition, board) and
                self._destination_free_or_enemy(newPosition, board))


if __name__ == "__main__":
    print("Tests Bishop OK !")