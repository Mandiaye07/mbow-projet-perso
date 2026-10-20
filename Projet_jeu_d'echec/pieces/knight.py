from pieces.piece import Piece


class Knight(Piece):
    """Classe représentant le Cavalier. Se déplace en L."""

    def __str__(self):
        """Retourne l'identifiant du Cavalier."""
        return 'N'

    def isValidMove(self, newPosition, board):
        """
        Vérifie si le déplacement est valide pour un Cavalier.

        Args:
            newPosition (Position): position de destination
            board (Board): plateau de jeu

        Returns:
            bool: True si le mouvement est valide
        """
        dc = abs(newPosition.col_index() - self._position.col_index())
        dr = abs(newPosition.row_index() - self._position.row_index())

        if not ((dc == 2 and dr == 1) or (dc == 1 and dr == 2)):
            return False

        return self._destination_free_or_enemy(newPosition, board)


if __name__ == "__main__":
    print("Tests Knight OK !")