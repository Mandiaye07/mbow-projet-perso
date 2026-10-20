import pygame
import sys
from chess import Chess
from position import Position
from player import Player
from ai_player import AIPlayer

TILE_SIZE = 80
BOARD_SIZE = 8
WIDTH = TILE_SIZE * BOARD_SIZE
HEIGHT = TILE_SIZE * BOARD_SIZE
WHITE_TILE = (240, 217, 181)
BLACK_TILE = (181, 136, 99)


class GameUI:
    """
    Interface graphique du jeu d'échecs avec pygame.

    Attributs:
        _chess (Chess): instance du jeu
        _screen (Surface): fenêtre pygame
        _images (dict): dictionnaire des images des pièces
        _selected_pos (Position): pièce actuellement sélectionnée
        _valid_moves (list): liste des mouvements valides
    """

    def __init__(self):
        """Initialise pygame et charge les images."""
        pygame.init()
        self._screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jeu d'Échecs")
        self._chess = Chess()
        self._images = {}
        self._selected_pos = None
        self._valid_moves = []
        self._load_images()
        self._init_players()

    def _load_images(self):
        """Charge toutes les images des pièces depuis assets/images/."""
        pieces = ['K', 'Q', 'B', 'N', 'R', 'P']
        colors = ['w', 'b']
        for piece in pieces:
            for color in colors:
                key = f"{piece}{color}"
                path = f"assets/images/{piece}{color}.png"
                img = pygame.image.load(path)
                self._images[key] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

    def _init_players(self):
        """Initialise les joueurs via le terminal."""
        name1 = input("Nom du joueur 1 (Blanc) ou 'AI' : ")
        name2 = input("Nom du joueur 2 (Noir) ou 'AI' : ")

        if name1 == "AI":
            self._chess._players.append(AIPlayer(0))
        else:
            self._chess._players.append(Player(name1, 0))

        if name2 == "AI":
            self._chess._players.append(AIPlayer(1))
        else:
            self._chess._players.append(Player(name2, 1))

        self._chess._currentPlayer = self._chess._players[0]

    def _get_image_key(self, piece):
        """
        Retourne la clé de l'image pour une pièce donnée.

        Args:
            piece (Piece): la pièce

        Returns:
            str: clé ex: 'Kw', 'Pb'
        """
        color = 'w' if piece.color == 0 else 'b'
        return f"{str(piece)}{color}"

    def _draw_board(self):
        """Dessine le plateau de jeu."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = WHITE_TILE if (row + col) % 2 == 0 else BLACK_TILE
                pygame.draw.rect(
                    self._screen, color,
                    (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

    def _draw_highlights(self):
        """Dessine la case sélectionnée et les mouvements valides."""
        highlight_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

        if self._selected_pos:
            highlight_surface.fill((246, 246, 105, 160))
            col = self._selected_pos.col_index()
            row = 7 - self._selected_pos.row_index()
            self._screen.blit(highlight_surface, (col * TILE_SIZE, row * TILE_SIZE))

        highlight_surface.fill((186, 202, 43, 160))
        for pos in self._valid_moves:
            col = pos.col_index()
            row = 7 - pos.row_index()
            self._screen.blit(highlight_surface, (col * TILE_SIZE, row * TILE_SIZE))

    def _draw_pieces(self):
        """Dessine toutes les pièces sur le plateau."""
        for col_char in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            for row_num in range(1, 9):
                pos = Position(col_char, row_num)
                piece = self._chess._board.getPiece(pos)
                if piece:
                    key = self._get_image_key(piece)
                    col = pos.col_index()
                    row = 7 - pos.row_index()
                    self._screen.blit(self._images[key], (col * TILE_SIZE, row * TILE_SIZE))

    def _get_valid_moves(self, position):
        """
        Calcule tous les mouvements valides pour la pièce à position.

        Args:
            position (Position): position de la pièce sélectionnée

        Returns:
            list: liste des positions valides
        """
        piece = self._chess._board.getPiece(position)
        if not piece:
            return []

        valid = []
        for col in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            for row in range(1, 9):
                newPos = Position(col, row)
                if piece.isValidMove(newPos, self._chess._board):
                    valid.append(newPos)
        return valid

    def _pixel_to_position(self, x, y):
        """
        Convertit des coordonnées pixel en Position.

        Args:
            x (int): coordonnée x en pixels
            y (int): coordonnée y en pixels

        Returns:
            Position: position correspondante
        """
        col = x // TILE_SIZE
        row = 7 - (y // TILE_SIZE)
        return Position.from_indices(col, row)

    def _handle_click(self, x, y):
        """
        Gère un clic sur le plateau.

        Args:
            x (int): coordonnée x
            y (int): coordonnée y
        """
        clicked_pos = self._pixel_to_position(x, y)
        piece = self._chess._board.getPiece(clicked_pos)
        current_color = self._chess._currentPlayer.color

        if self._selected_pos is None:
            if piece and piece.color == current_color:
                self._selected_pos = clicked_pos
                self._valid_moves = self._get_valid_moves(clicked_pos)
        else:
            if clicked_pos in self._valid_moves:
                selected_piece = self._chess._board.getPiece(self._selected_pos)
                move = f"{str(selected_piece)}{self._selected_pos} {str(selected_piece)}{clicked_pos}"
                self._chess.updateBoard(move)
                self._chess.switchPlayer()
                self._selected_pos = None
                self._valid_moves = []
            elif piece and piece.color == current_color:
                self._selected_pos = clicked_pos
                self._valid_moves = self._get_valid_moves(clicked_pos)
            else:
                self._selected_pos = None
                self._valid_moves = []

    def run(self):
        """Lance la boucle principale du jeu."""
        clock = pygame.time.Clock()

        while True:
            # Vérifie fin de partie
            if self._chess.isCheckMate():
                pygame.time.wait(3000)
                pygame.quit()
                sys.exit()

            # Tour de l'IA
            if isinstance(self._chess._currentPlayer, AIPlayer):
                pygame.time.wait(500)
                move = self._chess._currentPlayer.askMove(self._chess._board)
                if move:
                    self._chess.updateBoard(move)
                    self._chess.switchPlayer()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self._chess.save()
                        print("Partie sauvegardée !")
                    if event.key == pygame.K_l:
                        self._chess.load()
                        print("Partie chargée !")

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not isinstance(self._chess._currentPlayer, AIPlayer):
                            self._handle_click(*event.pos)

            self._draw_board()
            self._draw_highlights()
            self._draw_pieces()
            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    ui = GameUI()
    ui.run()