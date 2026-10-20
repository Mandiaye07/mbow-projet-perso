import pygame
import sys
import random
from settings import *
from entities.player import Player
from entities.enemy import Enemy
from entities.bonus import Bonus
from entities.boss import Boss
from ui.menu import MainMenu
from ui.hud import HUD

""" fonction principal , il gère la boucle principal du jeu , les états (menu/jeu), la musique ,  l'apparition des ennemis, des bonus et du boss  et enfin les collisions """
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.image.load("asset/img/bg.jpg").convert() #chargement bg
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) #adaptation du bg 
    pygame.display.set_caption("Projet Rasko - V2 avec bonus et hud")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)  # Police pr score

    pygame.mixer.music.load("asset/audio/musique_fond.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.5)

    # État du jeu
    game_state = "menu"
    main_menu = MainMenu()
    hud = HUD()

    # Groupe sprites
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()  # grp pour tirs
    enemies = pygame.sprite.Group()  # Groupe pr ennemis
    bonuses = pygame.sprite.Group()  # < Groupe pr bonus
    boss_group = pygame.sprite.Group()  # grp boss
    boss_spawned = False
    # Création du joueur
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    all_sprites.add(player)

    # Variable de jeu
    score = 0
    last_enemy_spawn = 0  # Pour gére le temps d'apparition
    last_bonus_spawn = 0  # <-Timer pour bonus

    running = True
    while running:
        # Gestion des events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Si Menu
            if game_state == "menu":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = "playing"
                    # Reset variables
                    player.current_hp = player.max_hp
                    score = 0
                    enemies.empty()
                    bullets.empty()
                    bonuses.empty()  # <- Reset bonus
                    boss_group.empty()  # On supprime le boss s'il y en a un
                    boss_spawned = False

            # Si Jeu
            elif game_state == "playing":
                # Tirer avec ESPACE
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet = player.shoot()
                        if bullet:  # tir réussi (cooldown ok)
                            all_sprites.add(bullet)
                            bullets.add(bullet)

        # Logique
        if game_state == "menu":
            main_menu.draw(screen)

        elif game_state == "playing":
            now = pygame.time.get_ticks()

            #spawn boss
            if score >= 100 and not boss_spawned:
                boss = Boss()
                all_sprites.add(boss)
                boss_group.add(boss)
                boss_spawned = True

                # Spawn des ennemis normaux (Seulement si PAS de boss)
            if not boss_spawned:
                if now - last_enemy_spawn > ENEMY_SPAWN_RATE:
                    last_enemy_spawn = now
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)

            # Spawn des BONUS toutes les 20-30 sec)
            if now - last_bonus_spawn > random.randint(10000, 15000):
                last_bonus_spawn = now
                bonus = Bonus()
                all_sprites.add(bonus)
                bonuses.add(bonus)

            # Maj
            all_sprites.update()

            # Collisions Tirs -> Ennemis
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                score += 10  # Win 10 points
                # Collisions Tirs -> BOSS
            hits_boss = pygame.sprite.groupcollide(boss_group, bullets, False, True)
            for boss_hit in hits_boss:
                boss_hit.damage(10)
                if boss_hit.hp <= 0:
                    score += 1000
                    game_state = "menu"
                    boss_spawned = False

                # Boss touche Joueur
                if pygame.sprite.spritecollide(player, boss_group, False):
                    player.damage(5)

            # Collisions Joueur -> recup bonus
            hits_bonus = pygame.sprite.spritecollide(player, bonuses, True)
            for bonus in hits_bonus:
                if bonus.type == "health":
                    player.heal(30)  # Rend 30 PV
                elif bonus.type == "score":
                    score += 50  # Bonus de points

            # Ennemis touche Joueur (Degats)
            hits_player = pygame.sprite.spritecollide(player, enemies, True)  # True pour supprimer ennemi
            for hit in hits_player:
                player.damage(20)
                if player.current_hp <= 0:
                    game_state = "menu"  # Retour au menu

            # Dessin
            screen.blit(background, (0, 0)) # <-- AJOUTE CETTE LIGNE
            all_sprites.draw(screen)
            all_sprites.draw(screen)
            for boss in boss_group:
                boss.draw(screen)
            # affiche HUD (remplace ancien affichage score)
            hud.draw(screen, score, player)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()