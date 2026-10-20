import pygame
from entities.entity import Entity
from weapons.projectiles import Projectile
from settings import *

""" Représente le vaisseau controler par le joueur.
cette classe gere les deplacement du vaisseau ,le systeme de santé et le cooldown des tirs """
class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = pygame.image.load("asset/img/player.png").convert_alpha() #convert_alpha pour transparence autour du sprite
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT)) #redim
        self.speed = PLAYER_SPEED

        # Vie (Ajout pour le HUD)
        self.max_hp = 100
        self.current_hp = 100

         #Cooldown
        self.last_shot_time = 0
        self.shoot_delay = 250  # Délai en ms entre deux tirs

    def damage(self, amount):
        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0

    def heal(self, amount):
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
       
    def shoot(self):
        # vérifier le temps actuel
        now = pygame.time.get_ticks()
        # Si le temps écoulé depuis dernier tir est suffisant
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now
            # créer project au centre du player
            bullet_x = self.rect.centerx - BULLET_WIDTH // 2
            bullet_y = self.rect.top
            return Projectile(bullet_x, bullet_y)
        return None

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # garde joueur dans écran
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT

    def update(self):
        self.move()