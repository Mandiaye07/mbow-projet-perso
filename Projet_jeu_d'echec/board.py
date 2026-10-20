from position import Position
from pieces.king import King
from pieces.queen import Queen
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.pawn import Pawn


class Board:
    """
    Classe représentant le plateau de jeu d'échecs.
    Gère l'état de l'échiquier et la position de toutes les pièces.

    Attributs:
        _board (dict): dictionnaire position -> pièce
    """

    def __init__(self):
        """
        Initialise le plateau avec toutes les pièces à leur position initiale.
        Utilise un dictionnaire pour stocker les pièces.
        """
        self._board = {}
        self._setup()

    def _setup(self):
        """Place toutes les pièces à leur position initiale."""
        pieces_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # Pièces blanches
        for i, PieceClass in enumerate(pieces_order):
            pos = Position(columns[i], 1)
            self._board[str(pos)] = PieceClass(pos, 0)

        for col in columns:
            pos = Position(col, 2)
            self._board[str(pos)] = Pawn(pos, 0)

        # Pièces noires
        for i, PieceClass in enumerate(pieces_order):
            pos = Position(columns[i], 8)
            self._board[str(pos)] = PieceClass(pos, 1)

        for col in columns:
            pos = Position(col, 7)
            self._board[str(pos)] = Pawn(pos, 1)

    def getPiece(self, position):
        """
        Retourne la pièce à la position donnée.

        Args:
            position (Position): position à vérifier

        Returns:
            Piece: la pièce à cette position, ou None si vide
        """
        return self._board.get(str(position), None)

    def getPosition(self, piece):
        """
        Retourne la position d'une pièce donnée.

        Args:
            piece (Piece): la pièce recherchée

        Returns:
            Position: position de la pièce, ou None si capturée
        """
        for pos_str, p in self._board.items():
            if p is piece:
                col = pos_str[0]
                row = int(pos_str[1])
                return Position(col, row)
        return None

    def movePiece(self, position, newPosition):
        """
        Déplace une pièce d'une position à une autre.

        Args:
            position (Position): position actuelle
            newPosition (Position): position de destination
        """
        piece = self.getPiece(position)
        if piece:
            del self._board[str(position)]
            self._board[str(newPosition)] = piece
            piece.position = newPosition

    def getAllPieces(self, color):
        """
        Retourne toutes les pièces d'une couleur donnée.

        Args:
            color (int): 0 pour blanc, 1 pour noir

        Returns:
            list: liste des pièces de cette couleur
        """
        return [p for p in self._board.values() if p.color == color]

    def display(self):
        """Affiche le plateau dans le terminal."""
        print("  a b c d e f g h")
        for row in range(8, 0, -1):
            line = f"{row} "
            for col in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                pos = Position(col, row)
                piece = self.getPiece(pos)
                line += (str(piece) if piece else '.') + ' '
            print(line)
        print()


if __name__ == "__main__":
    board = Board()
    print("Test affichage plateau initial :")
    board.display()

    p = board.getPiece(Position('e', 1))
    print(f"Pièce en e1 : {p}")  # Attendu : K

    p2 = board.getPiece(Position('e', 4))
    print(f"Pièce en e4 : {p2}")  # Attendu : None

    print("Tests Board OK !")