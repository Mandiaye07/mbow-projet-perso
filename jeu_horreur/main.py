import pygame
import random
import math
import time

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Définition des couleurs
BLANC = (255, 255, 255)
VERT = (0, 255, 0)
NOIR = (0, 0, 0)
VIOLET = (148, 0, 211)
OR = (255, 215, 0)
son = pygame.mixer.Sound("static/screamer.wav")

# Classe pour afficher et gérer la barre de vie du joueur
#Codé par Mandiaye le 07/04 et testé par Mandiaye le 09/04
#Modifié par Mandiaye le 17/04
class BarreDeVie:
    #initialisation des variables
    def __init__(self, x, y, largeur, hauteur):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.vie_max = 10
        self.vie_actuelle = self.vie_max #on commence directement avec la vie max
        self.style = pygame.font.Font(None, 24) #le style d'écriture
        self.dernier_soin = 0
        self.dernier_degats = 0

    #méthode pour dessiner la barre et afficher son texte
    def draw(self, fenetre):
        texte = self.style.render("Vie:", True, BLANC)
        fenetre.blit(texte, (self.x, self.y - 20))
        pygame.draw.rect(fenetre, NOIR, (self.x, self.y, self.largeur, self.hauteur)) #on dessine un rectangle noir
        largeur_vie = (self.vie_actuelle / self.vie_max) * self.largeur
        pygame.draw.rect(fenetre, VERT, (self.x, self.y, largeur_vie, self.hauteur))#puis par dessus un rectangle vert dont sa taille depend de self.vie_actuelle

    #méthode pour gérer le soin
    def soigner(self, joueur_x, joueur_y):
        temps = pygame.time.get_ticks() #donne le temps actuel
        if 3770 <= joueur_x <= 3870 and 1355 <= joueur_y <= 1455: #regarde si les coordonnées du joueur sont au niveau de la plateforme qui illustre une borne de soin sur la map
            if temps - self.dernier_soin > 1000: #si le temps écoulé est supérieur à 1secondes on peut se resoigner
                self.vie_actuelle += 1
                if self.vie_actuelle >= self.vie_max: #on vérifie que la vie actuelle n'est pas supérieur à la vie max
                    self.vie_actuelle = self.vie_max
            self.dernier_soin = temps

    #méthode pour gérer les dégats 
    def degats(self, joueur_x, joueur_y, momie_x, momie_y):
        temps = pygame.time.get_ticks() #donne le temps actuel
        if momie_x-50 <= joueur_x <= momie_x+50 and momie_y-50 <= joueur_y <= momie_y+50: #regarde si les coordonnées du joueur sont a peu près au niveau de celles de la momie
            if temps - self.dernier_degats > 1000: #on vérifie le temps de maninère à prendre des dégats seulements toutes les secondes
                self.vie_actuelle -= 2
                if self.vie_actuelle <= 0: #on vérifie que la vie actuelle n'est pas inférieur à 0
                    self.vie_actuelle = 0
            self.dernier_degats = temps

# Classe pour afficher et gérer la barre de peur du joueur
#Codé par Mandiaye et Ruben le 09/04 et testé par Ruben le 09/04
#Modifié par Mandiaye le 17/04
class BarreDePeur:
    #initialisation des variables
    def __init__(self, x, y, largeur, hauteur):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.peur_max = 10
        self.peur_actuelle = 1
        self.font = pygame.font.Font(None, 24) #le style d'écriture
        self.derniere_angoisse = 0
        self.dernier_calme = 0

    #méthode pour afficher la barre et son texte
    def draw(self, fenetre):
        texte = self.font.render("Peur:", True, BLANC)
        fenetre.blit(texte, (self.x, self.y - 20))
        pygame.draw.rect(fenetre, NOIR, (self.x, self.y, self.largeur, self.hauteur)) #on commence par dessiner un rectangle noir
        largeur_peur = (self.peur_actuelle / self.peur_max) * self.largeur
        pygame.draw.rect(fenetre, VIOLET, (self.x, self.y, largeur_peur, self.hauteur))#puis on dessine par dessus un rectangle violet qui répresente la peur et dépend de la peur actuelle

    #méthode pour gérer la peur du joueur
    def angoisse(self, joueur_x, joueur_y, momie_x, momie_y):
        temps = pygame.time.get_ticks()
        if joueur_x-100 <= momie_x <= joueur_x+100 and joueur_y-100 <= momie_y <= joueur_y+100 :
            if temps - self.derniere_angoisse > 1000:
                self.peur_actuelle += 1
                if self.peur_actuelle >= self.peur_max:
                    self.peur_actuelle = self.peur_max
            self.derniere_angoisse = temps #prend le temps actuelle

    #méthode pour gérer la peur du joueur pour la diminuer
    def calme(self, joueur_x, joueur_y):
        temps = pygame.time.get_ticks()
        if 3770 <= joueur_x <= 3870 and 1355 <= joueur_y <= 1455: #vérifie la position du joueur
            if temps - self.dernier_calme > 1000: #et le temps
                self.peur_actuelle -= 1
                if self.peur_actuelle <= 1: #limite la peur à 1
                    self.peur_actuelle = 1
            self.dernier_calme = temps #prend le temps actuelle

#Classe pour afficher et gérer les momies
#Codé par Mandiaye le 05/05 et testé par Mandiaye le 05/05
#Modifié par Mandiaye le 12/05
class Momie:
    #initialisation des variables
    def __init__(self, x, y, largeur, hauteur):
        self.image_normale = pygame.image.load("static/momie.png").convert_alpha()
        self.image_normale = pygame.transform.scale(self.image_normale, (largeur + 100, hauteur + 100))
        #L'image est de base assombrie
        self.image_sombre = self.image_normale.copy()
        sombre_surface = pygame.Surface(self.image_sombre.get_size(), pygame.SRCALPHA)
        sombre_surface.fill((0, 0, 0, 180))  # Transparence pour effet d'obscurité
        self.image_sombre.blit(sombre_surface, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.rect_momie = self.image_normale.get_rect(topleft=(x, y))
        self.vitesse = 3
        self.mouvement_x = 0
        self.mouvement_y = 0

    #méthode pour gérer le déplacement de la momie
    def deplacer(self, mouvement_x, mouvement_y, fond_largeur, fond_hauteur):
        self.rect_momie.x += mouvement_x
        self.rect_momie.y += mouvement_y
        self.rect_momie.clamp_ip(pygame.Rect(0, 0, fond_largeur, fond_hauteur))

    #méthode pour gérer si la momie est assombrie ou non
    def get_image_visible(self, joueur_centre, rayon): #donné par chatgpt prompt = "Comment faire pour que la momie soit visible que quand elle est dans le rayon de vision du joueur"
        momie_centre = self.rect_momie.center
        dx = momie_centre[0] - joueur_centre[0]
        dy = momie_centre[1] - joueur_centre[1]
        distance = (dx**2 + dy**2) ** 0.5
        if distance <= rayon:
            return self.image_normale
        else:
            return self.image_sombre


#Classe pour afficher et gérer le joueur
#Codé par Sacha le 02/04 et testé par Mandiaye et Sacha le 02/04
#Modifié par Sacha le 21/04 et par Mandiaye le 30/04 
class Joueur:
    #initialisation des variables
    def __init__(self, x, y, largeur, hauteur):
        self.image = pygame.image.load("static/alien.png").convert_alpha() #pour charger l'image
        self.image = pygame.transform.scale(self.image, (largeur + 50, hauteur + 50))  #pour redimensionner l'image
        self.rect_joueur = self.image.get_rect(topleft=(x, y)) #on dessine un rectangle en dessous de l'image qui represente le joueur
        self.vitesse = 8
        self.vivant = True

    #méthode pour gérer les collsions entre le joueur et les murs
    def mur(self, x, y, carte_collision):
        # On prend la couleur du pixel à cette position
        couleur = carte_collision.get_at((x, y))
        if couleur == (255, 102, 196): #et on vérifie si la couleur est rose
            return True
        return False
        
    #méthode pour gérer le déplacement du joueur
    #en fonction des touches joues le joueur se deplace ou non 
    def deplacer(self, touches, fond_largeur, fond_hauteur, carte_collision):
        dx = dy = 0
        # Déplacement en fonction des touches
        if touches[pygame.K_LEFT]:
            dx = -self.vitesse
        if touches[pygame.K_RIGHT]:
            dx = self.vitesse
        if touches[pygame.K_UP]:
            dy = -self.vitesse
        if touches[pygame.K_DOWN]:
           dy = self.vitesse

        #on regarde la nouvelle position du joueur
        test_x = self.rect_joueur.x + dx + self.rect_joueur.width // 2
        test_y = self.rect_joueur.y + dy + self.rect_joueur.height

        #si elle ne touche pas un mur le joueur peut se déplacer dans la direction 
        if not self.mur(test_x, test_y, carte_collision):
            self.rect_joueur.x += dx
            self.rect_joueur.y += dy
        self.rect_joueur.clamp_ip(pygame.Rect(0, 0, fond_largeur, fond_hauteur)) #chatgpt prompt = "permet de ne pas sortir de la map"


#Classe pour afficher et gérer les reliques
#Codé par Sacha le 12/05 et testé par Mandiaye et Sacha le 12/05
#Modifié par Sacha le 14/05
class Relique:
    #initialisation des variables
    def __init__(self, carte_collision, reliques_existantes):
        self.largeur = 30
        self.hauteur = 30
        self.carte_collision = carte_collision
        self.reliques_existantes = reliques_existantes
        self.active = True
        self.rect_relique = self.trouver_position(carte_collision)

    #méthode pour gérer la position de la relique
    def trouver_position(self, carte_collision):
        """Trouve une position valide pour la relique, loin des murs et autres reliques.
        """
        position_valide = False
        while not position_valide:
            #Choisit une position aléatoire sur la carte
            x = random.randint(0, self.carte_collision.get_width() - self.largeur)
            y = random.randint(0, self.carte_collision.get_height() - self.hauteur)
            #Vérifie si la position est loin des murs
            if not self.mur(x + self.largeur // 2, y + self.hauteur // 2, carte_collision):
                #Calcule le centre de la nouvelle relique
                centre_nouveau = (x + self.largeur // 2, y + self.hauteur // 2)
                position_valide = True
                #Vérifie la distance avec chaque relique existante
                for relique in self.reliques_existantes:
                    if relique.active:
                        #On calcule la distance entre la nouvelle relique et la relique existante aide de chat gpt prompt = "Comment faire en sorte que les reliques soient éloignées"
                        centre_relique = (relique.rect_relique.x + relique.largeur // 2, relique.rect_relique.y + relique.hauteur // 2)
                        distance = math.sqrt((centre_nouveau[0] - centre_relique[0])**2 + (centre_nouveau[1] - centre_relique[1])**2)
                        if distance < 500:
                            position_valide = False
                if position_valide:
                    return pygame.Rect(x, y, self.largeur, self.hauteur)

    #méthode pour gérer les murs et collision
    def mur(self, x, y, carte_collision):
        #Regarde la couleur du pixel à la position donnée
        couleur = carte_collision.get_at((x, y))
        if couleur == (255, 102, 196):
            return True
        return False
        

    #méthode pour dessiner les reliques
    def draw(self, ecran, camera, joueur_centre, rayon):
        if self.active:
            centre_relique = (self.rect_relique.x + self.largeur // 2, self.rect_relique.y + self.hauteur // 2)
            distance = math.sqrt((centre_relique[0] - joueur_centre[0])**2 + (centre_relique[1] - joueur_centre[1])**2)#
            if distance <= rayon:
                pygame.draw.rect(ecran, OR, self.rect_relique.move(-camera.x, -camera.y)) #on dessine un rectangle doré

    #méthode pour voir si le joueur est au niveau de la relique
    def collision(self, rect_joueur):
        if self.active and self.rect_relique.colliderect(rect_joueur):
            self.active = False
            return True
        return False

#Classe pour afficher et gérer le jeu
#Codé par Mandiaye et Sacha  le 10/05 et testé par Sacha le 10/05
#Modifié par Sacha le 21/04 Ruben le 11/05
class Jeu:
    #initialisation des variables
    def __init__(self):
        self.largeur, self.hauteur = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.ecran = pygame.display.set_mode((self.largeur, self.hauteur), pygame.FULLSCREEN)
        pygame.display.set_caption("L'asile de l'oubli")
        #on charge la map de collision et la normal
        self.fond = pygame.image.load("static/MAPFinal.png").convert()
        self.carte_collision = pygame.image.load("static/MAP collision.png").convert()
        self.fond_largeur, self.fond_hauteur = self.fond.get_size()
        #on crée les différents momies et le joueur
        self.joueur = Joueur(3775, 1150, 50, 50)
        self.momie1 = Momie(3500, 680, 50, 50)
        self.momie2 = Momie(2650, 1000, 50, 50)
        self.momie3 = Momie(5750, 1000, 50, 50)
        self.momie4 = Momie(6650, 1375, 50, 50)
        self.momie5 = Momie(3000, 2200, 50, 50)
        self.momie6 = Momie(4575, 1350, 50, 50)
        self.etape_m3 = 1 #numéro d'étape de la momie 3
        self.depart_x3 = 5750 #coordonnées de départ de la momie 3
        self.depart_y3 = 1000
        self.etape_m4 = 1 #numéro d'étape de la momie 4
        self.depart_x4 = 6650 #coordonnées de départ de la momie 4
        self.depart_y4 = 1375
        self.etape_m5 = 1 #numéro d'étape de la momie 5
        self.depart_x5 = 3000 #coordonnées de départ de la momie 5
        self.depart_y5 = 2200
        self.camera = pygame.Rect(0, 0, self.largeur, self.hauteur) #pour la caméra qui suit le joueur
        self.horloge = pygame.time.Clock()
        #on crée les 2 barres
        self.barre_de_vie = BarreDeVie(20, 40, 180, 30)
        self.barre_de_peur = BarreDePeur(20, 90, 180, 30)
        self.reliques = [] #on fait un tableau pour les reliques
        for i in range(5):
            relique = Relique(self.carte_collision, self.reliques)
            self.reliques.append(relique)
        self.reliques_trouvees = 0 #le nb de reliques trouvées
        self.police = pygame.font.Font(None, 36)
        self.victoire = False
        #Les images en fonction des différents fin
        self.image_victoire = pygame.image.load("static/victoire.png").convert()
        self.image_mort = pygame.image.load("static/mort.png").convert()
        self.image_screamer = pygame.image.load("static/screamer.png").convert()
        self.image_screamer1 = pygame.image.load("static/screamer1.png").convert()
        self.image_screamer1 = pygame.transform.scale(self.image_screamer1, self.ecran.get_size())
        self.image_screamer2 = pygame.image.load("static/screamer2.png").convert()
        self.image_screamer2 = pygame.transform.scale(self.image_screamer2, self.ecran.get_size())
        self.image_screamer3 = pygame.image.load("static/screamer3.jpg").convert()
        self.image_screamer3 = pygame.transform.scale(self.image_screamer3, self.ecran.get_size())
        self.image_screamer4 = pygame.image.load("static/screamer4.jpg").convert()
        self.image_screamer4 = pygame.transform.scale(self.image_screamer4, self.ecran.get_size())
        self.temps_screamer = 0
        self.temps_screamer1 = None
        self.temps_screamer2 = None
        self.temps_screamer3 = None
        self.temps_screamer4 = None
        self.afficher_screamer = False
        self.afficher_screamer1 = False
        self.afficher_screamer2 = False
        self.afficher_screamer3 = False
        self.afficher_screamer4 = False
        self.pas_joue_screamer1 = True
        self.pas_joue_screamer2 = True
        self.pas_joue_screamer3 = True
        self.pas_joue_screamer4 = True

    #méthode pour faire tourner le jeu
    def run(self):
        running = True
        rayon_joueur = 325
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not self.afficher_screamer and not self.victoire and self.barre_de_vie.vie_actuelle > 0: #si aucune des fins le joueur peut se déplacer
                touches = pygame.key.get_pressed()
                self.joueur.deplacer(touches, self.fond_largeur, self.fond_hauteur, self.carte_collision)

                #Mouvement momie 1
                if self.momie1.rect_momie.x <= 3000 or self.momie1.rect_momie.x >= 3900: #mouvements définis en dehors de la class car ils sont tous différents
                    self.momie1.vitesse *= -1 
                self.momie1.mouvement_x = self.momie1.vitesse
                self.momie1.deplacer(self.momie1.mouvement_x, self.momie1.mouvement_y, self.fond_largeur, self.fond_hauteur)

                #Mouvement momie 2
                if self.momie2.rect_momie.y <= 999 or self.momie2.rect_momie.y >= 1850:
                    self.momie2.vitesse *= -1
                self.momie2.mouvement_y = self.momie2.vitesse 
                self.momie2.deplacer(self.momie2.mouvement_x, self.momie2.mouvement_y, self.fond_largeur, self.fond_hauteur)

                #Mouvement momie 3
                #on utilise une série de conditions pour que la momie se déplace
                if self.etape_m3 == 1:
                    if self.momie3.rect_momie.y < self.depart_y3 + 200:
                        self.momie3.mouvement_y = self.momie3.vitesse
                        self.momie3.mouvement_x = 0
                        
                    else:
                        self.momie3.mouvement_y = 0
                        self.etape_m3 = 2 #on passe à l'étape 2

                elif self.etape_m3 == 2:
                    if self.momie3.rect_momie.x < self.depart_x3 + 275:
                        self.momie3.mouvement_x = self.momie3.vitesse
                        self.momie3.mouvement_y = 0
                    else:
                        self.momie3.mouvement_x = 0
                        self.etape_m3 = 3 #on passe à l'étape 3

                elif self.etape_m3 == 3:
                    if self.momie3.rect_momie.y < self.depart_y3 + 375:
                        self.momie3.mouvement_y = self.momie3.vitesse
                        self.momie3.mouvement_x = 0
                    else:
                        self.momie3.mouvement_y = 0
                        self.etape_m3 = 4 #on passe à l'étape 4

                elif self.etape_m3 == 4:
                    if self.momie3.rect_momie.x < self.depart_x3 + 900:
                        self.momie3.mouvement_x = self.momie3.vitesse
                        self.momie3.mouvement_y = 0
                    else:
                        self.momie3.mouvement_x = 0
                        self.etape_m3 = 5 #on passe à l'étape 5

                elif self.etape_m3 == 5:
                    self.momie3.rect_momie.x = self.depart_x3
                    self.momie3.rect_momie.y = self.depart_y3
                    self.etape_m3 = 1 #on retourne à l'étape 1
                self.momie3.deplacer(self.momie3.mouvement_x, self.momie3.mouvement_y, self.fond_largeur, self.fond_hauteur)

                #Mouvement momie 4
                #on utilise une série de conditions pour que la momie se déplace
                if self.etape_m4 == 1:
                    if self.momie4.rect_momie.x > self.depart_x4 - 625:
                        self.momie4.mouvement_x = -self.momie4.vitesse
                        self.momie4.mouvement_y = 0
                    else:
                        self.momie4.rect_momie.x = self.depart_x4 - 625
                        self.momie4.mouvement_x = 0
                        self.etape_m4 = 2 #on passe à l'étape 2

                elif self.etape_m4 == 2:
                    if self.momie4.rect_momie.y < self.depart_y4 + 190:
                        self.momie4.mouvement_y = self.momie4.vitesse
                        self.momie4.mouvement_x = 0
                    else:
                        self.momie4.rect_momie.y = self.depart_y4 + 190
                        self.momie4.mouvement_y = 0
                        self.etape_m4 = 3 #on passe à l'étape 3

                elif self.etape_m4 == 3:
                    if self.momie4.rect_momie.x > self.depart_x4 - 900:
                        self.momie4.mouvement_x = -self.momie4.vitesse
                        self.momie4.mouvement_y = 0 #on passe à l'étape 4
                    else:
                        self.momie4.rect_momie.x = self.depart_x4 - 900
                        self.momie4.mouvement_x = 0
                        self.etape_m4 = 4

                elif self.etape_m4 == 4:
                    if self.momie4.rect_momie.y < self.depart_y4 + 600:
                        self.momie4.mouvement_y = self.momie4.vitesse
                        self.momie4.mouvement_x = 0
                    else:
                        self.momie4.rect_momie.y = self.depart_y4 + 600
                        self.momie4.mouvement_y = 0
                        self.etape_m4 = 5 #on passe à l'étape 5

                elif self.etape_m4 == 5:
                    self.momie4.rect_momie.x = self.depart_x4
                    self.momie4.rect_momie.y = self.depart_y4
                    self.etape_m4 = 1 #on retourne à l'étape 1
                self.momie4.deplacer(self.momie4.mouvement_x, self.momie4.mouvement_y, self.fond_largeur, self.fond_hauteur)


                #Mouvement momie 5
                #on utilise une série de conditions pour que la momie se déplace
                if self.etape_m5 == 1:
                    if self.momie5.rect_momie.x < self.depart_x5 + 220:
                        self.momie5.mouvement_x = self.momie5.vitesse
                        self.momie5.mouvement_y = 0
                    else:
                        self.momie5.rect_momie.x = self.depart_x5 + 220
                        self.momie5.mouvement_x = 0
                        self.etape_m5 = 2 #on passe à l'étape 2

                elif self.etape_m5 == 2:
                    if self.momie5.rect_momie.y < self.depart_y5 + 320:
                        self.momie5.mouvement_y = self.momie5.vitesse
                        self.momie5.mouvement_x = 0
                    else:
                        self.momie5.rect_momie.y = self.depart_y5 + 320
                        self.momie5.mouvement_y = 0
                        self.etape_m5 = 3 #on passe à l'étape 3

                elif self.etape_m5 == 3:
                    if self.momie5.rect_momie.x < self.depart_x5 + 1000:
                        self.momie5.mouvement_x = self.momie5.vitesse
                        self.momie5.mouvement_y = 0
                    else:
                        self.momie5.rect_momie.x = self.depart_x5 + 1000
                        self.momie5.mouvement_x = 0
                        self.etape_m5 = 4 #on passe à l'étape 5

                elif self.etape_m5 == 4:
                    self.momie5.rect_momie.x = self.depart_x5
                    self.momie5.rect_momie.y = self.depart_y5
                    self.etape_m5 = 1 #on retourne à l'étape 1
                self.momie5.deplacer(self.momie5.mouvement_x, self.momie5.mouvement_y, self.fond_largeur, self.fond_hauteur)


                #Mouvement momie 6
                if self.momie6.rect_momie.y <= 1349 or self.momie6.rect_momie.y >= 1800:
                    self.momie6.vitesse *= -1
                self.momie6.mouvement_y = self.momie6.vitesse 
                self.momie6.deplacer(self.momie6.mouvement_x, self.momie6.mouvement_y, self.fond_largeur, self.fond_hauteur)


                self.barre_de_vie.soigner(self.joueur.rect_joueur.x, self.joueur.rect_joueur.y)
                self.barre_de_peur.calme(self.joueur.rect_joueur.x, self.joueur.rect_joueur.y)
                #on utilise une boucle dans un tableau pour vérifier toutes les momies en même temps 
                for momie in [self.momie1, self.momie2, self.momie3, self.momie4, self.momie5, self.momie6]:
                    self.barre_de_vie.degats(self.joueur.rect_joueur.x, self.joueur.rect_joueur.y, momie.rect_momie.x, momie.rect_momie.y) #on vérifie pour les dégats
                    self.barre_de_peur.angoisse(self.joueur.rect_joueur.x, self.joueur.rect_joueur.y, momie.rect_momie.x, momie.rect_momie.y) #on vérifie pour la peur
                
                #on parcourt le tableau reliques pour voir si le joueur les a récupérés
                for relique in self.reliques:
                    if relique.collision(self.joueur.rect_joueur):
                        self.reliques_trouvees += 1
                        if self.reliques_trouvees == 5:
                            self.victoire = True

                #pour afficher le screamer
                if self.barre_de_peur.peur_actuelle >= self.barre_de_peur.peur_max:
                    self.afficher_screamer = True
                    self.temps_screamer = pygame.time.get_ticks()

            self.camera.x = self.joueur.rect_joueur.centerx - self.largeur // 2 #la pos x de la caméra
            self.camera.y = self.joueur.rect_joueur.centery - self.hauteur // 2 #la pos y de la caméra
            self.camera.clamp_ip(pygame.Rect(0, 0, self.fond_largeur, self.fond_hauteur))
            self.ecran.fill(BLANC)
            self.ecran.blit(self.fond, (-self.camera.x, -self.camera.y))

            #Centre du joueur pour le rayon
            centre_joueur_absolu = self.joueur.rect_joueur.center

            #Affichage des momies
            image_momie1 = self.momie1.get_image_visible(centre_joueur_absolu, rayon_joueur)
            self.ecran.blit(image_momie1, self.momie1.rect_momie.move(-self.camera.x, -self.camera.y))

            image_momie2 = self.momie2.get_image_visible(centre_joueur_absolu, rayon_joueur)
            self.ecran.blit(image_momie2, self.momie2.rect_momie.move(-self.camera.x, -self.camera.y))

            image_momie3 = self.momie3.get_image_visible(centre_joueur_absolu, rayon_joueur)
            self.ecran.blit(image_momie3, self.momie3.rect_momie.move(-self.camera.x, -self.camera.y))

            image_momie4 = self.momie4.get_image_visible(centre_joueur_absolu, rayon_joueur)
            self.ecran.blit(image_momie4, self.momie4.rect_momie.move(-self.camera.x, -self.camera.y))

            image_momie5 = self.momie5.get_image_visible(centre_joueur_absolu, rayon_joueur)
            self.ecran.blit(image_momie5, self.momie5.rect_momie.move(-self.camera.x, -self.camera.y))

            image_momie6 = self.momie6.get_image_visible(centre_joueur_absolu, rayon_joueur)
            self.ecran.blit(image_momie6, self.momie6.rect_momie.move(-self.camera.x, -self.camera.y))


            #on parcourt le tableau pour afficher les reliques
            for relique in self.reliques:
                relique.draw(self.ecran, self.camera, centre_joueur_absolu, rayon_joueur)

            #on crée une zone d'ombre sur la map
            ombre = pygame.Surface((self.largeur, self.hauteur), pygame.SRCALPHA)
            ombre.fill((0, 0, 0, 200))
            #pour avoir le centre du joueur
            centre_joueur = (
                self.joueur.rect_joueur.centerx - self.camera.x,
                self.joueur.rect_joueur.centery - self.camera.y
            )
            pygame.draw.circle(ombre, (0, 0, 0, 0), centre_joueur, rayon_joueur)
            self.ecran.blit(ombre, (0, 0))

            #pour afficher le joueur
            self.ecran.blit(self.joueur.image, self.joueur.rect_joueur.move(-self.camera.x, -self.camera.y))

            #pour afficher le compteur de reliques trouvés
            texte_reliques = self.police.render(f"Reliques: {self.reliques_trouvees}/5", True, BLANC)
            self.ecran.blit(texte_reliques, (1100, 20))

            #affichage des barres de vie et peur
            self.barre_de_vie.draw(self.ecran)
            self.barre_de_peur.draw(self.ecran)

            #print(self.joueur.rect_joueur.x, self.joueur.rect_joueur.y)
            if 2150 <= self.joueur.rect_joueur.x <= 2250 and 1550 <= self.joueur.rect_joueur.y <= 1650:
               self.afficher_screamer1 = True

            if 4900 <= self.joueur.rect_joueur.x <= 5000 and 1600 <= self.joueur.rect_joueur.y <= 1700:
               self.afficher_screamer2 = True

            if 5400 <= self.joueur.rect_joueur.x <= 5500 and 1250 <= self.joueur.rect_joueur.y <= 1350:
               self.afficher_screamer3 = True
            
            if 5200 <= self.joueur.rect_joueur.x <= 5300 and 2450 <= self.joueur.rect_joueur.y <= 2550:
               self.afficher_screamer4 = True

            if self.afficher_screamer1 and self.pas_joue_screamer1:
                if self.temps_screamer1 is None:
                    self.temps_screamer1 = pygame.time.get_ticks()
                    son.play()
                    pygame.mixer.music.stop()
                self.ecran.blit(self.image_screamer1, (0, 0))
                if pygame.time.get_ticks() - self.temps_screamer1 > 3000:
                    self.afficher_screamer1 = False
                    self.pas_joue_screamer1 = False
                    self.temps_screamer1 = None

            if self.afficher_screamer2 and self.pas_joue_screamer2:
                if self.temps_screamer2 is None:
                    self.temps_screamer2 = pygame.time.get_ticks()
                    son.play()
                    pygame.mixer.music.stop()
                self.ecran.blit(self.image_screamer2, (0, 0))
                if pygame.time.get_ticks() - self.temps_screamer2 > 3000:
                    self.afficher_screamer2 = False
                    self.pas_joue_screamer2 = False
                    self.temps_screamer2 = None 

            if self.afficher_screamer3 and self.pas_joue_screamer3:
                if self.temps_screamer3 is None:
                    self.temps_screamer3 = pygame.time.get_ticks()
                    son.play()
                    pygame.mixer.music.stop()
                self.ecran.blit(self.image_screamer3, (0, 0))
                if pygame.time.get_ticks() - self.temps_screamer3 > 3000:
                    self.afficher_screamer3 = False
                    self.pas_joue_screamer3 = False
                    self.temps_screamer3 = None 

            if self.afficher_screamer4 and self.pas_joue_screamer4:
                if self.temps_screamer4 is None:
                    self.temps_screamer4 = pygame.time.get_ticks()
                    son.play()
                    pygame.mixer.music.stop()
                self.ecran.blit(self.image_screamer4, (0, 0))
                if pygame.time.get_ticks() - self.temps_screamer4 > 3000:
                    self.afficher_screamer4 = False
                    self.pas_joue_screamer4 = False
                    self.temps_screamer4 = None 

            #série de conditions pour savoir quelles images afficher
            if self.victoire:
                victoire = pygame.transform.scale(self.image_victoire, (self.largeur, self.hauteur))
                self.ecran.blit(victoire, (0, 0))
            elif self.barre_de_vie.vie_actuelle == 0:
                mort = pygame.transform.scale(self.image_mort, (self.largeur, self.hauteur))
                self.ecran.blit(mort, (0, 0))
            elif self.afficher_screamer:
                screamer = pygame.transform.scale(self.image_screamer, (self.largeur, self.hauteur))
                self.ecran.blit(screamer, (0, 0))
                son.play()
                if pygame.time.get_ticks() - self.temps_screamer > 3000:
                    self.afficher_screamer = False
                    pygame.mixer.music.stop()
                    self.barre_de_peur.peur_actuelle = 1

            #mettre à jour
            pygame.display.update()
            #limiter à 60fps
            self.horloge.tick(60)

        pygame.quit()

#pour lancer le jeu
if __name__ == "__main__":
    jeu = Jeu()
    jeu.run()