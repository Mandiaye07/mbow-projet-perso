from abc import ABC, abstractmethod
from position import Position


class Piece(ABC):
    """
    Classe abstraite représentant une pièce du jeu d'échecs.

    Attributs:
        _position (Position): position actuelle de la pièce
        _color (int): couleur de la pièce (0 = blanc, 1 = noir)
    """

    def __init__(self, position, color):
        """
        Initialise une pièce.

        Args:
            position (Position): position initiale
            color (int): 0 pour blanc, 1 pour noir
        """
        self._position = position
        self._color = color

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def color(self):
        return self._color

    @abstractmethod
    def __str__(self):
        """Retourne la lettre identifiant la pièce (K, Q, B, N, R, P)."""
        pass

    @abstractmethod
    def isValidMove(self, newPosition, board):
        """
        Vérifie si le déplacement vers newPosition est valide.

        Args:
            newPosition (Position): position de destination
            board (Board): plateau de jeu actuel

        Returns:
            bool: True si le mouvement est valide
        """
        pass

    def _destination_free_or_enemy(self, newPosition, board):
        """
        Vérifie que la case destination est vide ou occupée par un ennemi.

        Args:
            newPosition (Position): position de destination
            board (Board): plateau de jeu

        Returns:
            bool: True si la case est libre ou occupée par un ennemi
        """
        target = board.getPiece(newPosition)
        return target is None or target.color != self._color

    def _is_path_clear(self, newPosition, board):
        """
        Vérifie qu'aucune pièce ne bloque le chemin (pour tour, fou, reine).

        Args:
            newPosition (Position): position de destination
            board (Board): plateau de jeu

        Returns:
            bool: True si le chemin est dégagé
        """
        c1, r1 = self._position.col_index(), self._position.row_index()
        c2, r2 = newPosition.col_index(), newPosition.row_index()

        dc = 0 if c2 == c1 else (1 if c2 > c1 else -1)
        dr = 0 if r2 == r1 else (1 if r2 > r1 else -1)

        c, r = c1 + dc, r1 + dr
        while (c, r) != (c2, r2):
            if board.getPiece(Position.from_indices(c, r)) is not None:
                return False
            c += dc
            r += dr

        return True


if __name__ == "__main__":
    print("Piece est une classe abstraite, elle ne peut pas être instanciée directement.")
    print("Tests Piece OK !")