from pieces.piece import Piece


class King(Piece):
    """Classe représentant le Roi. Se déplace d'une case dans toutes les directions."""

    def __str__(self):
        """Retourne l'identifiant du Roi."""
        return 'K'

    def isValidMove(self, newPosition, board):
        """
        Vérifie si le déplacement est valide pour un Roi.

        Args:
            newPosition (Position): position de destination
            board (Board): plateau de jeu

        Returns:
            bool: True si le mouvement est valide
        """
        dc = abs(newPosition.col_index() - self._position.col_index())
        dr = abs(newPosition.row_index() - self._position.row_index())

        if dc > 1 or dr > 1 or (dc == 0 and dr == 0):
            return False

        return self._destination_free_or_enemy(newPosition, board)


if __name__ == "__main__":
    print("Tests King OK !")