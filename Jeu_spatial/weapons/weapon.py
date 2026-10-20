import pygame


class Weapon:
    def __init__(self, owner):
        self.owner = owner  # Qui tire ?
        self.bullets = []  # Liste des balles prst

    def shoot(self):
        #pour créer une balle
        print("Pew pew !")  # Pour tester

    def update(self):
        # Update position balle
        pass