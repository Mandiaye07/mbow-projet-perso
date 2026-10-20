import pygame

""" Module mère qui gère tout les entités mobile du jeu
"""
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        #pour l'instant rectangle a mettre sprite ici après
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 255))  # rose
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0

    def update(self):
        # Méthode pr enfants
        pass

    def draw(self, screen):
        # draw image a pos
        screen.blit(self.image, self.rect)