import pyxel
import random
import time


class App:
    def __init__(self):
        pyxel.init(128, 128, "PYXEL1", 30)
        pyxel.load("my_ressource.pyxres")
        self.x = 60
        self.y = 100
        self.direction = None
        self.saut = False
        self.c_saut = 0
        self.sol = self.y + 8
        self.tirs = []
        self.tirs_ennemi = []
        self.g_tirs = []  # gros tirs
        self.g_charge = 0  # chrono de frames avant que les tirs chargés soient chargés
        self.epee = [False, 0]
        self.ennemis_niveau1 = []
        self.ennemis_niveau2 = []
        self.ennemis_niveau3 = []
        self.ennemis_niveau4 = []
        self.ennemis_niveau5 = []
        self.ennemis = [self.ennemis_niveau1, self.ennemis_niveau2, self.ennemis_niveau3, self.ennemis_niveau4, self.ennemis_niveau5]
        self.explosions = []
        self.g_explosions = []
        self.boum_ok = []
        self.heal = []
        self.vies = 10
        self.droite = True
        self.touche = False  # passe à True si le perso est touché, sert pour le draw
        self.zone = 1  # stocke le numéro du niveau
        # compteur d'ennemis morts // à réinitianliser à chaque changement de niveau normalement
        self.ennemi_ded = 0

        self.hell_niveau1 = [[112, 60], [100, 104]]

        self.niveau1 = [[0, 0, 108, 8, 5],  # bord Haut
                        [0, 8, 8, 120, 5],  # bord Gauche
                        [0, 120, 128, 128, 5],  # bord Bas
                        [120, 16, 128, 128, 5],  # bord droit
                        [0, 50, 16, 58, 5],
                        [68, 112, 128, 120, 5],
                        [40, 40, 120, 48, 5],
                        [30, 103, 46, 111, 5],
                        [50, 85, 120, 93, 5],
                        [28, 70, 50, 78, 5]]

        self.niveau2 = [[24, 0, 128, 8, 7],  # bord Haut
                        [-8, 16, 8, 110, 7],  # bord Gauche
                        [0, 120, 128, 128, 7],  # bord Bas
                        [120, 8, 128, 128, 7],  # bord droit
                        [50, 50, 80, 58, 7],
                        [40, 94, 100, 102, 7],
                        [8, 70, 16, 110, 7],
                        [70, 8, 90, 24, 7],
                        [104, 70, 120, 78, 7],
                        [30, 30, 100, 38, 7]]

        self.niveau3 = [[24, 0, 128, 8, 8],  # bord Haut
                        [0, 16, 8, 120, 8],  # bord Gauche
                        [0, 120, 128, 128, 8],  # bord Bas
                        [120, 8, 128, 112, 8],  # bord droit
                        [50, 8, 58, 58, 8],
                        [50, 100, 100, 108, 8],
                        [92, 84, 128, 92, 8],
                        [8, 32, 24, 40, 8],
                        [42, 50, 58, 58, 8],
                        [8, 72, 60, 80, 8],
                        [80, 50, 128, 58, 8]]

        self.niveau4 = [[0, 0, 108, 8, 10],  # bord Haut
                        [0, 8, 8, 120, 10],  # bord Gauche
                        [0, 120, 60, 128, 10],  # bord Bas
                        [76, 120, 128, 128, 10],  # bord Bas
                        [120, 16, 128, 128, 10],
                        [50, 100, 74, 108, 10],
                        [56, 8, 64, 32, 10],
                        [0, 56, 64, 64, 10],
                        [100, 80, 128, 88, 10],
                        [56, 64, 80, 72, 10],
                        [24, 32, 100, 40, 10]]

        self.niveau5 = [[0, 0, 128, 8, 11],  # bord Haut
                        [0, 8, 8, 32, 11],  # bord Gauche
                        [120, 8, 128, 128, 11],  # bord Gauche
                        [0, 48, 8, 128, 11],
                        [0, 120, 128, 128, 11],  # bord Bas
                        [120, 0, 128, 128, 11],
                        [60, 100, 76, 108, 11],
                        [0, 48, 40, 56, 11],
                        [70, 8, 90, 48, 11],
                        [60, 60, 120, 68, 11],
                        [100, 80, 128, 88, 11],
                        [8, 80, 32, 110, 11]]

        self.level = [self.niveau1, self.niveau2,
                      self.niveau3, self.niveau4, self.niveau5]
        self.numero_niveau = 2
        self.niveau = self.niveau3
        self.music = True
        if self.music == True:
            pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    # and self.x+2>collision[0] and self.y>collision[1] and self.x+2>collision[2] and self.y<collision[3] and self.x+2>collision[4] and self.y>collision[5] and self.x+2>collision[6] and self.y<collision[7]

    def epee_creation(self):
        """
        self.epee est une liste qui contient un booléen (qui nous dit si l'épée doit apparaître) et d'un compteur de
        frame
        quand KEY_W est pressée, self.epee = True
        quand self.epee[0] = True, le compteur augmente
        quand le compteur atteint 5 frame, il est réinitialisé est self.epee[0] = False
        """

        if pyxel.btnr(pyxel.KEY_W):
            self.epee[0] = True
        if self.epee[0] == True:
            self.epee[1] += 1

        if self.epee[1] >= 5:
            self.epee[1] = 0
            self.epee[0] = False

    def test_collision(self, x_augmentation=0, y_augmentation=0):

        d = 0

        for collision in self.niveau:
            if abs(collision[1] - collision[3]) == 8:
                d = 1

            if collision[0] <= self.x <= collision[2] and collision[3] == self.y + y_augmentation:
                y_augmentation = 0

            if collision[0] <= self.x <= collision[2] and collision[1] == self.y + y_augmentation + 8:
                y_augmentation = 0

            elif collision[1] <= self.y and self.y + 8 <= collision[3] and collision[
                2] == self.x and self.x + x_augmentation < collision[2]:
                x_augmentation = 0

            elif collision[1] <= self.y and self.y + 8 <= collision[3] and collision[
                0] == self.x + 8 and self.x + 8 + x_augmentation > collision[0]:
                x_augmentation = 0

        self.x += x_augmentation
        self.y += y_augmentation

        # passage 1 -> 2
        if self.x >= 128 and self.y < 16 and self.numero_niveau == 0:
            self.x = 0
            self.y = 100
            self.numero_niveau += 1
            self.saut = False
            self.ennemi_ded = 0

        # passage 2 -> 1
        elif self.x <= -8 and self.y >= 112 and self.numero_niveau == 1:
            self.x = 120
            self.y = 8
            self.numero_niveau -= 1
            self.saut = False
            self.ennemi_ded = 0

        # passage 2 -> 3
        elif self.x <= -8 and self.y <= 10 and self.numero_niveau == 1:
            self.x = 120
            self.y = 100
            self.numero_niveau += 1
            self.saut = False
            self.ennemi_ded = 0

        # passage 3 -> 2
        elif self.x >= 128 and self.y >= 128 and self.numero_niveau == 2:
            self.x = 0
            self.y = 8
            self.numero_niveau -= 1
            self.saut = False
            self.ennemi_ded = 0

        # passage 3 -> 4
        elif self.x < -8 and self.y <= 10 and self.numero_niveau == 2:
            self.x = 54
            self.y = 100
            self.numero_niveau += 1
            self.saut = False
            self.ennemi_ded = 0

        # passage 4 -> 3
        elif 60 <= self.x <= 76 and self.y >= 128 and self.numero_niveau == 3:
            self.x = 0
            self.y = 0
            self.numero_niveau -= 1
            self.saut = False
            self.ennemi_ded = 0

        # passage 4 -> 5
        elif self.x >= 128 and self.y >= 10 and self.numero_niveau == 3:
            self.x = 0
            self.y = 30
            self.numero_niveau += 1
            self.saut = False
            self.ennemi_ded = 0

        # passage 5 -> 4
        elif self.x < -8 and self.y >= 30 and self.numero_niveau == 4:
            self.x = 120
            self.y = 8
            self.numero_niveau -= 1
            self.saut = False
            self.ennemi_ded = 0

        self.niveau = self.level[self.numero_niveau]

    def deplacement(self):

        ok_saut = False

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = "right"
            self.droite = True
            self.test_collision(2, 0)

        if pyxel.btn(pyxel.KEY_LEFT):
            self.direction = "left"
            self.droite = False
            self.test_collision(-2, 0)

        if pyxel.btn(pyxel.KEY_UP):
            self.direction = "up"
            self.haut = True
            self.test_collision(0, -1)

        if pyxel.btn(pyxel.KEY_SPACE) and self.y == self.sol:

            for collision in self.niveau:
                if self.y + 8 == collision[1] and collision[0] <= self.x + 8 and self.x <= collision[2]:
                    ok_saut = True

        if ok_saut == True:
            self.saut = True

        if pyxel.btnp(pyxel.KEY_UP, 1, 1):
            self.haut = True

        if not pyxel.btnp(pyxel.KEY_UP, 1, 1):
            self.haut = False

    def sauter(self, saut, sol):
        """
        :param saut: booléen (True quand KEY_SPACE est pressée)
        :param sol: int (ordonnée du dernier sol touché au moment du saut)
        Si saut = True, si l'ordonnée du cube est inférieure à (au dessus de) 25 pixel au dessus de l'ordonnée du
        dernier sol touché: l'ordonnée diminue (le cube monte)
        Si le cube dépasse de 25 pyxel le sol à partir duquel il a sauté, on appelle la fonction self.faut_descendre()
        """

        if saut == True:
            if self.y > self.sol - 25:
                self.y -= 3
            else:
                self.faut_descendre()

    def faut_descendre(self):
        """
        quand appelée, incrémente un compteur de frame (self.c_saut)
        quand 3 frames sont écoulées, self.saut = False et le compteur est réinitialisé
        """

        self.c_saut += 1
        if self.c_saut == 3:
            self.saut = False
            self.c_saut = 0

    def descente(self, saut):
        """
        saut: booléen (nous dit si le saut est fini ou pas)
        ok passe à False si on ne peut plus descendre (test de collision avec les coordonnées de toutes les plateformes
        avec un bon gros for
        si il y a collision, on met a jour self.sol (avec l'ordonnée du nouveau dernier sol touché) et ok devient False
        si ok est toujours True et si on est au dessus du plus bas sol, on continue la descente et l'ordonnée augmente
        (le cube descend)
        si on tombe au plus bas, on met à jour self.sol à 90 (ordonnée du plus bas sol qui n'est pas une plateforme, t'as
        bien suivi)
        """

        ok = True
        if saut == False:
            for i in range(3):
                for collision in self.niveau:
                    if collision[0] <= self.x <= collision[2] and collision[1] == self.y + 8 or collision[
                        0] <= self.x + 8 <= collision[2] and collision[1] == self.y + 8:
                        self.sol = collision[1] - 8
                        ok = False

                if ok == True:
                    self.y += 1

    def tirs_creation(self):
        """
        sel.tirs (lst) contient des listes contenant [absisce tir, ordonnée tir, bool droite, bool haut, ???keskejaifoutu]
        si KEY_SHIFT est pressée, on ajoute une liste à la liste self.tirs (toute les 7 frames seulement)
        """

        if pyxel.btnp(pyxel.KEY_SHIFT, 7, 7):

            if self.haut == True:
                self.tirs.append(
                    [self.x + 4, self.y, self.droite, self.haut, False])
            elif self.droite == True:
                self.tirs.append(
                    [self.x + 8, self.y + 4, self.droite, self.haut, False])
            else:
                self.tirs.append(
                    [self.x - 4, self.y + 4, self.droite, self.haut, False])

    def tirs_deplacement(self):
        """
        diminue l'ordonnée de tir si tir[3] = True (enlève tir si self.
        sinon et si tir[2] = True : augmente l'abscisse de tir
        sinon : diminue l'abscisse de tir
        si le tir dépasse l'écran, le tir est enlevé de self.tir
        idem avec g_tir
        """
        for tir in self.tirs:
            if tir[3] == True:
                self.tirs_collision(tir, 0, -2)
                if tir[1] <= 8:
                    self.tirs.remove(tir)
            elif tir[2] == False:
                self.tirs_collision(tir, -2, 0)
                if tir[0] > 120:
                    self.tirs.remove(tir)
            else:
                self.tirs_collision(tir, 2, 0)
                if tir[0] < 0:
                    self.tirs.remove(tir)

        for g in self.g_tirs:
            if g[3] == True:
                g[1] -= 2
                if g[1] <= 0:
                    self.g_tirs.remove(g)
            elif g[2] == False:
                g[0] -= 2
                if g[0] >= 128:
                    self.g_tirs.remove(g)
            else:
                g[0] += 2
                if g[0] <= 0:
                    self.g_tirs.remove(g)

    def tirs_ennemis_deplacement(self):
        """
        comme pour les déplacements des tirs mais avec la liste de tirs_ennemis
        """
        for tir in self.tirs_ennemi:
            if tir[2]==False:
                tir[0] -= 2
                if tir[0] > 128:
                    self.tirs_ennemi.remove(tir)
            elif tir[2]==True:
                tir[0] += 2
                if tir[0] < 0:
                    self.tirs_ennemi.remove(tir)

    def tirs_collision(self, tir, x_augmentation, y_augmentation):
        for collision in self.niveau:
            if abs(collision[1] - collision[3]) == 8:
                d = 1

            if collision[0] <= tir[0] <= collision[2] and collision[3] == tir[1] + y_augmentation:
                y_augmentation = 0
                self.tirs.remove(tir)

            if collision[0] <= tir[0] <= collision[2] and collision[1] == tir[1] + y_augmentation + 8:
                y_augmentation = 0
                self.tirs.remove(tir)

            elif collision[1] <= tir[1] and tir[1] + 8 <= collision[3] and collision[2] == tir[0] and tir[
                0] + x_augmentation <= collision[2]:
                x_augmentation = 0
                self.tirs.remove(tir)

            elif collision[1] <= tir[1] and tir[1] <= collision[3] and collision[0] == tir[0] + 8 and tir[
                0] + 8 + x_augmentation >= collision[0]:
                x_augmentation = 0
                self.tirs.remove(tir)

        tir[0] += x_augmentation
        tir[1] += y_augmentation

    def gros_tirs_creation(self):
        """ajout dans self.g_tirs des tirs chargés
        """

        if pyxel.btnp(pyxel.KEY_X, 1, 1):
            self.g_charge += 1
        if self.g_charge == 15:
            self.g_charge = 0
            if self.haut == True:
                self.g_tirs.append(
                    [self.x + 4, self.y - 2, self.droite, self.haut, False])
            elif self.droite == True:
                self.g_tirs.append(
                    [self.x + 8, self.y + 4, self.droite, self.haut, False])
            else:
                self.g_tirs.append(
                    [self.x - 4, self.y + 4, self.droite, self.haut, False])

        if pyxel.btnr(pyxel.KEY_X):
            self.g_charge = 0

    def mort_ennemi(self):
        for i in range(len(self.ennemis)):
            for ennemi in self.ennemis[i]:
                if ennemi[2] <= 0:
                    self.explosion_creation(ennemi)
                    self.ennemis[i].remove(ennemi)
                    self.ennemi_ded +=1

    def collisions_tirs(self):
        """
        c'est compliqué
        .
        .
        .
        (des test de collision, on baisse les point de vie du mob, si ils tombent à 0 on l'enlève de self.ennemis
        et on appelle les fonctions qui font des explosions, on enlève le tir de la liste...
        dans le cas des tirs g, on met juste à jour self.boum_ok avec les coordonnées du tir qui va générer l'explosion)
        """
        ok_epee = False
        for i in range(len(self.ennemis)):
            for ennemi in self.ennemis[i]:
                ennemi[4] = False
            for g in self.g_tirs:
                for ennemi in self.ennemis[i]:
                    if g[3] == False:
                        if ennemi[0] <= g[0] + 12 and ennemi[0] >= g[0] and ennemi[1] >= g[1] - 8 and ennemi[1] <= g[1]:
                            self.boum_ok.append([g[0], g[1]])
                            if g in self.g_tirs:
                                self.g_tirs.remove(g)

                    elif g[3] == True:
                        if ennemi[0] <= g[0] and ennemi[0] + 7 >= g[0] and ennemi[1] + 8 >= g[1] and ennemi[1] <= g[
                            1] - 4:
                            self.boum_ok.append([g[0], g[1]])
                            if g in self.g_tirs:
                                self.g_tirs.remove(g)

            for tir in self.tirs:
                for ennemi in self.ennemis[i]:
                    ennemi[4] = False
                    if tir[3] == False:
                        if ennemi[0] <= tir[0] + 12 and ennemi[0] >= tir[0] and ennemi[1] >= tir[1] - 8 and ennemi[1] <= \
                                tir[1]:
                            ennemi[2] -= 1
                            ennemi[4] = True
                            if tir in self.tirs:
                                self.tirs.remove(tir)

                    elif tir[3] == True:
                        if ennemi[0] <= tir[0] and ennemi[0] + 7 >= tir[0] and ennemi[1] + 8 >= tir[1] and ennemi[1] <= \
                                tir[
                                    1] - 4:
                            ennemi[2] -= 1
                            ennemi[4] = True
                            if tir in self.tirs:
                                self.tirs.remove(tir)

            for ennemi in self.ennemis[i]:

                if self.epee[1] != 0:
                    if self.haut == True:
                        if ennemi[0] >= self.x - 7 and ennemi[0] <= self.x + 14 and ennemi[1] >= self.y - 20 and ennemi[
                            1] <= self.y - 8:
                            ok_epee = True
                            if ennemi[9] == 0:
                                ennemi[2] -= 1
                                ennemi[4] = True

                    elif self.droite == False:
                        if ennemi[0] >= self.x - 16 and ennemi[0] <= self.x and ennemi[1] >= self.y - 5 and ennemi[
                            1] <= self.y + 13:
                            ok_epee = True
                            if ennemi[9] == 0:
                                ennemi[2] -= 3
                                ennemi[4] = True

                    else:
                        if ennemi[0] >= self.x and ennemi[0] <= self.x + 16 and ennemi[1] >= self.y - 5 and ennemi[
                            1] <= self.y + 13:
                            ok_epee = True
                            if ennemi[9] == 0:
                                ennemi[2] -= 3
                                ennemi[4] = True
                if ok_epee == True:
                    ennemi[9] += 1
                else:
                    ennemi[9] = 0

    def collision_tirs_ennemis(self):
        for tir in self.tirs_ennemi:
            if self.x <= tir[0] + 4 and self.x >= tir[0] -4 and self.y >= tir[1] - 8 and self.y <= tir[1]:
                self.vies -= 1
                self.touche = True
                if tir in self.tirs_ennemi:
                    self.tirs_ennemi.remove(tir)

    def collisions_perso(self):
        self.touche = False

        for i in range(len(self.ennemis)):
            for ennemi in self.ennemis[i]:
                if self.y <= ennemi[1] + 8 and self.y >= ennemi[1] - 8 and self.x <= ennemi[0] + 8 and self.x + 8 >= ennemi[0]:
                    if self.epee[1] > 15 or self.epee[1] == 0:
                        self.ennemis[i].remove(ennemi)
                        self.vies -= 1
                        self.ennemi_ded += 1
                        self.touche = True

        for h in self.heal:
            if self.y <= h[1] + 8 and self.y >= h[1] - 8 and self.x <= h[0] + 8 and self.x + 8 >= h[0]:
                self.heal.remove(h)
                self.vies += 1

    def explosion_creation(self, ennemi):
        """
        boum
        """
        self.explosions.append([ennemi[0] + 4, ennemi[1], 0])
        self.ennemi_ded += 1

    def g_explosion_creation(self, ennemi):
        """
        boum
        """
        self.g_explosions.append([ennemi[0] + 4, ennemi[1], 0])

    def g_explosion_deplacement(self):
        """
        boum
        """
        for explosion in self.explosions:
            explosion[2] += 1
            if explosion[2] >= 12:
                self.explosions.remove(explosion)

    def explosion_deplacement(self):
        """
        boum
        """
        for g_exp in self.g_explosions:
            g_exp[2] += 1
            if g_exp[2] >= 20:
                self.g_explosions.remove(g_exp)

    def ennemi_deplacement(self):

        for ennemi in self.ennemis[self.numero_niveau]:
            dep_en = Deplacement_ennemi(ennemi, self.x, self.y, self.niveau1)
            if dep_en.deplacement_horizontal() != None:
                ennemi[0] = dep_en.deplacement_horizontal()[0]
            ennemi[1] = dep_en.deplacement_vertical()
            if dep_en.deplacement_horizontal() != None:
                if dep_en.deplacement_horizontal()[1] == True:
                    attaque = Attaques_ennemi(ennemi, self.x, self.y)
                    tir_temp = attaque.tirs_crea()
                    if tir_temp != None:
                        self.tirs_ennemi.append(tir_temp)

    def creation_ennemi(self):

        if self.numero_niveau == 0 and len(self.ennemis[self.numero_niveau]) + self.ennemi_ded <= 2:
            en1 = Ennemi(112, 104, 4, 30, 92, 112, False, "foot")
            en2 = Ennemi(112, 77, 4, 30, 92, 112, False, "shoot ")
            self.ennemis_niveau1.append(en1.ennemis_creation())
            self.ennemis_niveau1.append(en2.ennemis_creation())

        if self.numero_niveau == 1 and  len(self.ennemis[self.numero_niveau]) + self.ennemi_ded<= 2:
            en1 = Ennemi(112, 108, 4, 30, 0, 112, False, "shooter")
            self.ennemis_niveau2.append(en1.ennemis_creation())

        if self.numero_niveau == 3 and  len(self.ennemis[self.numero_niveau]) + self.ennemi_ded<= 2:
            en1 = Ennemi(8, 40, 4, 30, 92, 112, True, "shooter")
            self.ennemis_niveau4.append(en1.ennemis_creation())

    def boum(self):
        """
        si self.boum_ok contient des coordonnées de tir à l'origine d'une explosion :
        parcours de la liste self.ennemis (avec un bon gros while et un indice i qui incrémente quand on vire pas des
        éléments de la liste
        test de collision avec une box de 34 pixel de côté autour du tir
        si l'ennemi est dedans, on l'enlève de la liste et on appelle les fonctions d'explosion
        """
        i = 0
        if self.boum_ok != []:
            while i < len(self.ennemis[self.numero_niveau]):
                if self.ennemis[self.numero_niveau][i][0] >= self.boum_ok[0][0] - 15 and self.ennemis[self.numero_niveau][i][0] <= self.boum_ok[0][0] + 15 and \
                        self.ennemis[self.numero_niveau][i][1] \
                        <= self.boum_ok[0][1] + 15 and self.ennemis[self.numero_niveau][i][1] >= self.boum_ok[0][1] - 15:
                    self.ennemis[self.numero_niveau][i][2] -= 3
                    self.ennemis[self.numero_niveau][i][4] = True
                    if self.ennemis[self.numero_niveau][i][2] != 0:
                        i += 1
                else:
                    i += 1
        self.boum_ok = []

    def update(self):

        self.deplacement()
        self.sauter(self.saut, self.sol)
        self.descente(self.saut)
        self.tirs_creation()
        self.tirs_deplacement()
        self.epee_creation()
        self.gros_tirs_creation()
        self.collisions_tirs()
        self.collision_tirs_ennemis()
        self.collisions_perso()
        self.explosion_deplacement()
        self.g_explosion_deplacement()  # à encore créer
        self.creation_ennemi()
        self.ennemi_deplacement()
        self.tirs_ennemis_deplacement()
        self.mort_ennemi()
        self.boum()

    def draw(self):

        pyxel.cls(0)
        # draw box
        for col in self.niveau:
            pyxel.rect(col[0], col[1], abs(col[0] - col[2]),
                       abs(col[1] - col[3]), col[4])

        # draw tir
        for tir in self.tirs:
            if tir[3] == False:
                pyxel.rect(tir[0], tir[1], 4, 1, 10)
            else:
                pyxel.rect(tir[0], tir[1] - 2, 1, 4, 10)

        # draw tirs ennemi
        for tir in self.tirs_ennemi:
            if self.tirs_ennemi != None:
                pyxel.rect(tir[0], tir[1], 4, 1, 12)

        # draw tirs chargés
        for g in self.g_tirs:
            if g[3] == False:
                pyxel.rect(g[0], g[1], 4, 1, 11)
            else:
                pyxel.rect(g[0], g[1] - 2, 1, 4, 11)

        # draw epee
        if self.epee[1] != 0:
            if self.haut == True:
                pyxel.rect(self.x + 3, self.y - 10, 2, 10, 9)

            elif self.droite == True:
                pyxel.rect(self.x + 8, self.y + 3, 8, 2, 9)
            else:
                pyxel.rect(self.x - 8, self.y + 3, 8, 2, 9)

        # draw perso
        if self.touche == False:
            pyxel.rect(self.x, self.y, 8, 8, 9)
        else:
            pyxel.rect(self.x, self.y, 8, 8, 8)

        # draw mobs

        for ennemi in self.ennemis[self.numero_niveau]:
            if ennemi[4] == False:
                pyxel.rect(ennemi[0], ennemi[1], 8, 8, 14)
            elif ennemi[4] == True:
                pyxel.rect(ennemi[0], ennemi[1], 8, 8, 11)

                    # draw explosion
        for explosion in self.explosions:
            pyxel.circb(explosion[0] + 4, explosion[1] + 4,
                        2 * (explosion[2] // 4), 8 + explosion[2] % 3)


class Ennemi:
    def __init__(self, absc, ordo, pv, range, trajet_droite, trajet_gauche, direction, type):
        """
        prend en paramètre les coordonnées, la vie et la range de l'ennemi à créer
        """
        self.absc = absc
        self.ordo = ordo
        self.pv = pv
        self.range = range
        self.trajd = trajet_droite
        self.trajg = trajet_gauche
        self.dir = direction
        self.type = type

    def ennemis_creation(self):
        """
        :return: [abscisse, ordonnée, pv, range, touché ou pas]
        ajoute la liste à la liste d'ennemis de app
        le False correspond à si l'ennemi est touché
        le 0 à la fin correspond aux frames d'invincibilité du mob (incrémente quand touché par l'épée)
        """
        return [self.absc, self.ordo, self.pv, self.range, False, self.trajd, self.trajg, self.dir, self.type, 0]


class Deplacement_ennemi:

    def __init__(self, ennemi, x, y, collisions):
        """
        prend en paramètre l'ennemi à déplacer, les coordonnées du joueur et la liste des collisions avec l'environnement
        """
        self.ennemi = ennemi
        self.x = x
        self.y = y
        self.collisions = collisions

    def agro(self):
        """
        si l'abscisse du joueur rentre dans la range de l'ennemi (self.ennemi[0] + self.ennemi[3]), l'ennemi se
        déplace vers lui (test de collisions pour voir s'il rencontre un obstacle)
        ok=0 veut dire pas de deplacements
        ok=1 veut dire droite
        ok=2 veut dire gauche
        """
        ok = 0
        if self.x > (self.ennemi[0] - self.ennemi[3]) and self.x + 8 < self.ennemi[0] and self.y > self.ennemi[1] - 12 and self.y < self.ennemi[1] + 20:
            ok = 2
            for col in self.collisions:
                if self.ennemi[0] == col[2] and self.ennemi[1] + 8 > col[3] and self.ennemi[1] < col[1]:
                    ok = 0
        elif self.x < (self.ennemi[0] + 8 + self.ennemi[3]) and self.x > self.ennemi[0] + 8 and self.y > self.ennemi[1] - 12 and self.y < self.ennemi[1] + 20:
            ok = 1
            for col in self.collisions:
                if self.ennemi[0] + 8 == col[0] and self.ennemi[1] + 8 >= col[3] and self.ennemi[1] <= col[1] and \
                        self.ennemi[7] == False:
                    ok = 0

        return ok

    def deplacement_horizontal(self):
        """
        return: la nouvelle abscisse de l'ennemi
        """
        ok = self.agro()
        if ok == 0:
            return self.deplacement_horizontal_defaut(), False
        if self.ennemi[8] == "foot":
            if ok == 2:
                return self.ennemi[0] - 1, False
            elif ok == 1:
                return self.ennemi[0] + 1, False
        elif self.ennemi[8] == "shooter":
            return self.ennemi[0], True

    def deplacement_horizontal_defaut(self):
        """ self.ennemi[7] = True veut dire que la direction de l'ennemi est la droite
        """

        if self.ennemi[0] == self.ennemi[5]:
            self.ennemi[7] = True
        elif self.ennemi[0] == self.ennemi[6]:
            self.ennemi[7] = False

        for col in self.collisions:
            # test collision à droite
            if self.ennemi[0] + 8 == col[0] and self.ennemi[1] + 8 >= col[3] and self.ennemi[1] <= col[1] and \
                    self.ennemi[7] == False:
                return self.ennemi[0]
            # test collision à gauche
            if self.ennemi[0] == col[2] and self.ennemi[1] + 8 > col[3] and self.ennemi[1] < col[1] and self.ennemi[
                7] == True:
                return self.ennemi[0]

        if pyxel.frame_count % 5 == 0:
            if self.ennemi[0] < self.ennemi[6] and self.ennemi[7] == True:
                return self.ennemi[0] + 1
            elif self.ennemi[0] > self.ennemi[5] and self.ennemi[7] == False:
                return self.ennemi[0] - 1
            elif self.ennemi[0] > self.ennemi[6]:
                return self.ennemi[0] - 1
            elif self.ennemi[0] < self.ennemi[5]:
                return self.ennemi[0] + 1
        else:
            return self.ennemi[0]

    def deplacement_vertical(self):
        """parcours de toutes les boîtes de collision avec for et test de collision
        si l'ennemi n'est sur aucune boîte de collision, on le fait descendre
        :return: la nouvelle ordonnée de l'ennemi"""

        ok = True
        for col in self.collisions:
            if self.ennemi[0] >= col[0] - 8 and self.ennemi[0] <= col[2] and self.ennemi[1] + 8 == col[1]:
                ok = False

        if ok == True and self.ennemi[1] + 1 <= 120:
            return self.ennemi[1] + 1
        else:
            return self.ennemi[1]


class Attaques_ennemi:
    def __init__(self, ennemi, x, y):
        self.ennemi = ennemi
        self.x = x
        self.y = y

    def direction_tirs(self):
        """
        self.ennemi[7] = False : l'ennemi est à gauche
        self.ennemi[7] = True : l'ennemi est à droite
        """
        if self.x > (self.ennemi[0] - self.ennemi[3]) and self.x + 8 < self.ennemi[0] and self.y > self.ennemi[1] - 12 and self.y < self.ennemi[1] + 20:
            self.ennemi[7]=False
        elif self.x < (self.ennemi[0] + 8 + self.ennemi[3]) and self.x > self.ennemi[0] + 8 and self.y > self.ennemi[1] - 12 and self.y < self.ennemi[1] + 20:
            self.ennemi[7]=True

    def tirs_crea(self):
        self.direction_tirs()
        if pyxel.frame_count % 10== 0:
            if self.ennemi[7]==True:
                return [self.ennemi[0] + 8, self.ennemi[1] + 4, self.ennemi[7], False, False]
            elif self.ennemi[7]==False:
                return [self.ennemi[0] - 4, self.ennemi[1] + 4, self.ennemi[7], False, False]


App()
