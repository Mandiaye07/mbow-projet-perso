import pygame
from settings import *

"""Dessine les élément de l'interface sur la suface de l'écran: 
 -la police de caractere
 -le score 
 - barre de vie """
class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 24, bold=True)

    def draw(self, screen, score, player):
        # Affichage score
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Barre de vie
        bar_width = 200
        bar_height = 20
        x = SCREEN_WIDTH - bar_width - 10
        y = 10

        #calcul pourcentage vie
        if player.max_hp > 0:
            hp_percent = player.current_hp / player.max_hp
        else:
            hp_percent = 0

        current_bar_width = int(bar_width * hp_percent)

        # Fond de la barre (Rouge)
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(screen, RED, bg_rect)

        # Vie restante (Vert)
        if current_bar_width > 0:
            fg_rect = pygame.Rect(x, y, current_bar_width, bar_height)
            pygame.draw.rect(screen, GREEN, fg_rect)

        # Contour
        pygame.draw.rect(screen, WHITE, bg_rect, 2)