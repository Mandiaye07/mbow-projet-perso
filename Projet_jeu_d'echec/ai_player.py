import random
from position import Position
from player import Player

class AIPlayer(Player):
    """
    Classe représentant un joueur IA
    Génère un mouvement aléatoire parmi les pièces disponibles
    """

    def __init__(self, color):
        """ Initialise le joueur IA
        Arguments:
            couleur
        """
        super().__init__("AI", color)

    def askMove(self, board):
        """ Génère un coup aléatoire valide
        Argumens: plateau du jeu """
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        my_pieces = []
        for col in columns:
            for row in range(1, 9):
                pos = Position(col, row)
                piece = board.getPiece(pos)
                if piece and piece.color == self._color:
                    my_pieces.append((piece, pos))

        random.shuffle(my_pieces)
        for piece, pos in my_pieces:
            destinations = []
            for col in columns:
                for row in range(1, 9):
                    newPos = Position(col, row)
                    if piece.isValidMove(newPos, board):
                        destinations.append(newPos)

            if destinations:
                newPos = random.choice(destinations)
                move = f"{str(piece)}{pos} {str(piece)}{newPos}"
                print(f"IA joue : {move}")
                return move

        return None

if __name__ == "__main__":
    print("Test AIPlayer :")
    ai = AIPlayer(1)
    print(f"IA : {ai.name}, couleur : {ai.color}")
    print("Tests AIPlayer OK !")
