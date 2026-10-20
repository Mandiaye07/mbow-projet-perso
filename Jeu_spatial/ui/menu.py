import pygame
from settings import *
"""Gère l'affiche du menu principal au lancement du jeu """
class MainMenu:
    def __init__(self):
        self.font_title = pygame.font.SysFont("Arial", 50, bold=True)
        self.font_text = pygame.font.SysFont("Arial", 30)

    def draw(self, screen):
        screen.fill(BLACK) # Fond noir

        # Titre
        title = self.font_title.render("PROJET RASKO", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        screen.blit(title, title_rect)

        # Instruction
        text = self.font_text.render("Appuyez sur ENTREE pour jouer", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text, text_rect)