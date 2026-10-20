import pygame
import random
from entities.entity import Entity
from settings import *

"""Représente les objets bonus qui tombe a l'écran.
2 types de bonus : 
- santé
- augmentation du score""" 
class Bonus(Entity):
    def __init__(self):
        # pos radnom en haut
        x = random.randint(0, SCREEN_WIDTH - 30)
        y = -30
        super().__init__(x, y, 30, 30)  # Carré de 30x30

        self.speed = 2  # fall moin vite que ennemies

        #choix type bonus (50% chacun)
        if random.random() > 0.5:
            self.type = "health"
            self.image.fill((0, 255, 255))  # Cyan pour la vie
        else:
            self.type = "score"
            self.image.fill((255, 255, 0))  # Jaune pour le score

    def update(self):
        self.rect.y += self.speed
        # Si sort de l'écran, on supprime
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()