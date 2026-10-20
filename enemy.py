import pygame
from entities.entity import Entity
from settings import *
import random

''' Module qui gère les ennemies qui apparaissent de manière aléatoires, le mouvement descendant et la suppression automatique pour libérer la mémoire'''
class Enemy(Entity):
    def __init__(self):
        # ennemie a pose X aléatoire en haut
        x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        y = -ENEMY_HEIGHT  # Juste au-dessus de l'écran
        super().__init__(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.num_img = random.randint(1, 3) #pour avoir une img random
        self.chemin = f"asset/img/ennemi{self.num_img}.png"
        self.image = pygame.image.load(self.chemin).convert_alpha() #convert_alpha pour transparence autour du sprite
        self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
        self.speed = ENEMY_SPEED

    def update(self):
        # L'ennemi descend
        self.rect.y += self.speed

        # S'il sort en bas  détruit
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()