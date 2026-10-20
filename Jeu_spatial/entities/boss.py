import pygame
from entities.entity import Entity
from settings import *

"""Entité qui possède une barre de vie propre , une plus grande taille et un mouvement latéral """
class Boss(Entity):
    def __init__(self):
        # Pose au centre haut
        x = SCREEN_WIDTH // 2 -50
        y = 45
        super().__init__(x, y, 150, 150)

        self.image = pygame.image.load("asset/img/ennemi1.png").convert_alpha() #convert_alpha pour transparence autour du sprite
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(topleft=(x, y))

        # Stats du boss
        self.hp = 100
        self.max_hp = 100
        self.speed = 3
        self.direction = 1  # 1 = droite, -1 = gauche

    def update(self):
        # Déplacement latéral
        self.rect.x += self.speed * self.direction

        # Rebondit sur les bords
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1

    def damage(self, amount):
        self.hp -= amount
        # change de couleur quand touché
        if self.hp <= 0:
            self.kill()

    def draw(self, screen):
        super().draw(screen)
        # barre de vie boss
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        if self.hp > 0:
            width_hp = int(self.rect.width * (self.hp / self.max_hp))
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, width_hp, 5))