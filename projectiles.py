import pygame
from entities.entity import Entity
from settings import *


class Projectile(Entity):
    def __init__(self, x, y):
        # créer projet (x,y)
        super().__init__(x, y, BULLET_WIDTH, BULLET_HEIGHT)
        self.image = pygame.image.load("asset/img/projectile.png").convert_alpha() #convert_alpha pour transparence autour du sprite
        self.image = pygame.transform.scale(self.image, (BULLET_WIDTH, BULLET_HEIGHT))
        self.speed = BULLET_SPEED

    def update(self):
        # project monte
        self.rect.y -= self.speed

        # Si projectile sort de l'écran par le haut, on le détruit (bien pour la mémoire)
        if self.rect.bottom < 0:
            self.kill()