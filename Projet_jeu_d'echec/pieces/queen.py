from pieces.piece import Piece


class Queen(Piece):
    """Classe représentant la Reine. Se déplace en ligne droite ou en diagonale."""

    def __str__(self):
        """Retourne l'identifiant de la Reine."""
        return 'Q'

    def isValidMove(self, newPosition, board):
        """
        Vérifie si le déplacement est valide pour une Reine.

        Args:
            newPosition (Position): position de destination
            board (Board): plateau de jeu

        Returns:
            bool: True si le mouvement est valide
        """
        dc = abs(newPosition.col_index() - self._position.col_index())
        dr = abs(newPosition.row_index() - self._position.row_index())

        # Mouvement en ligne droite (tour) ou en diagonale (fou)
        mouvement_tour = (dc == 0) != (dr == 0)
        mouvement_fou = dc == dr and dc != 0

        if not mouvement_tour and not mouvement_fou:
            return False

        return (self._is_path_clear(newPosition, board) and
                self._destination_free_or_enemy(newPosition, board))


if __name__ == "__main__":
    print("Tests Queen OK !")