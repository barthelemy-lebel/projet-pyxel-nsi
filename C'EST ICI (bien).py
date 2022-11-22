import pyxel, random, time


class App:
    def __init__(self):
        pyxel.init(128, 128, "PYXEL1", 30)
        self.x = 60
        self.y = 90
        self.tirs = []
        self.epee = [False, 0]
        self.ennemis = []
        self.collisions = [[[0, 90], [128, 90], [128, 128], [0, 128]]]
        self.explosions = []
        self.g_explosions = []
        self.heal = []
        self.vies = 10
        self.saut = False
        self.c_saut = 0
        self.c_sec = 0
        self.c_ennemis = 60
        self.sol = 90 #récupère l'ordonnée du dernier sol touché
        self.chrono = 0
        self.c_m = 0
        self.g_charge = 0
        self.g_tirs = []
        self.droite = True
        self.haut = False
        self.boum_ok = []
        self.zone = 1
        self.ennemi_ded = 0

        pyxel.run(self.update, self.draw)

    def deplacement(self):
        """
        si le cube reste dans l'écran, fait varier l'abscisse si on presse KEY_RIGHT ou KEY_LEFT et adapte
        le booléen self.droite
        si l'ordonnée du cube est égale à celle du dernier sol touché (self.sol), KEY_SPACE adapte le booléen self.saut
        KEY_UP adapte le booléen self.haut. Si elle n'est pas pressée, self.haut prend la valeur False
        """

        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < 120:
            self.x += 2
            self.droite = True
        if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
            self.x += -2
            self.droite = False
        if pyxel.btn(pyxel.KEY_SPACE) and self.y == self.sol:
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
            for col in self.collisions:
                if self.y + 8 == col[1] and self.x >= col[0] - 7 and self.x <= col[0] + 17:
                    self.sol = col[1] - 8
                    ok = False
            if ok == True and self.y < 90:
                self.y += 3
        if self.y == 90:
            self.sol = 90

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

    def gros_tirs_creation(self):

        if pyxel.btnp(pyxel.KEY_X, 1, 1):
            self.g_charge += 1
        if self.g_charge == 15:
            self.g_charge = 0
            if self.haut == True:
                self.g_tirs.append([self.x + 4, self.y - 2, self.droite, self.haut, False])
            elif self.droite == True:
                self.g_tirs.append([self.x + 8, self.y + 4, self.droite, self.haut, False])
            else:
                self.g_tirs.append([self.x - 4, self.y + 4, self.droite, self.haut, False])

        if pyxel.btnr(pyxel.KEY_X):
            self.g_charge = 0

    def tirs_creation(self):
        """
        sel.tirs (lst) contient des listes contenant [absisce tir, ordonnée tir, bool droite, bool haut, ???keskejaifoutu]
        si KEY_SHIFT est pressée, on ajoute une liste à la liste self.tirs (toute les 7 frames seulement)
        """

        if pyxel.btnp(pyxel.KEY_SHIFT, 7, 7):
            if self.haut == True:
                self.tirs.append([self.x + 4, self.y, self.droite, self.haut, False])
            elif self.droite == True:
                self.tirs.append([self.x + 8, self.y + 4, self.droite, self.haut, False])
            else:
                self.tirs.append([self.x - 4, self.y + 4, self.droite, self.haut, False])

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
                tir[1] -= 2
                if tir[1] <= 0:
                    self.tirs.remove(tir)
            elif tir[2] == False:
                tir[0] -= 2
                if tir[0] > 128:
                    self.tirs.remove(tir)
            else:
                tir[0] += 2
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

    def heal_deplacement(self):
        # moins utile pour l'instant
        """for h in self.heal:
            h[0] += 1
            if h[0] > pyxel.width:
                self.heal.remove(h)"""

    def compte_a_rebours(self):
        # moins utile pour l'instant
        """self.c_ennemis -= 1
        if self.c_ennemis == -1:
            self.c_ennemis = 60"""

    def compte_tout_court(self):
        """
        self.chrono gère les frames
        self.c_sec gère les secondes (augmente toute les 30 frames en réinitialisant self.chrono)
        self.c_m gère les minutes (augmente toute les 60 secondes en réinitialisant self.c_sec)
        """
        self.chrono += 1

        if self.chrono == 30:
            self.c_sec += 1
            self.chrono = 0

        if self.c_sec == 60:
            self.c_sec = 0
            self.c_m += 1

    def boum(self):
        """
        si self.boum_ok contient aucune coordonnée de tir à l'origine d'une explosion :
        parcours de la liste self.ennemis (avec un bon gros while et un indice i qui incrémente quand on vire pas des
        éléments de la liste
        test de collision avec une box de 34 pixel de côté autour du tir
        si l'ennemi est dedans, on l'enlève de la liste et on appelle les fonctions d'explosion
        """

        i = 0
        if self.boum_ok != []:

            while i < len(self.ennemis):
                if self.ennemis[i][0] >= self.boum_ok[0][0] - 15 and self.ennemis[i][0] <= self.boum_ok[0][0] + 15 and self.ennemis[i][1] \
                        <= self.boum_ok[0][1] + 15 and self.ennemis[i][1] >= self.boum_ok[0][1] - 15:
                    self.g_explosion_creation(self.ennemis[i])
                    self.explosion_creation(self.ennemis[i])
                    self.ennemis.remove(self.ennemis[i])

                else:
                    i += 1

        self.boum_ok = []


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
        for g in self.g_tirs:
            for ennemi in self.ennemis:
                if g[3] == False:
                    if ennemi[0] <= g[0] + 12 and ennemi[0] >= g[0] and ennemi[1] >= g[1] - 8 and ennemi[1] <= g[1]:
                        self.boum_ok.append([g[0], g[1]])
                        if g in self.g_tirs:
                            self.g_tirs.remove(g)

                elif g[3] == True:
                    if ennemi[0] <= g[0] and ennemi[0] + 7 >= g[0] and ennemi[1] + 8 >= g[1] and ennemi[1] <= g[1] - 4:
                        self.boum_ok.append([g[0], g[1]])
                        if g in self.g_tirs:
                            self.g_tirs.remove(g)

        for tir in self.tirs:
            for ennemi in self.ennemis:
                ennemi[4] = False
                if tir[3] == False:
                    if ennemi[0] <= tir[0] + 12 and ennemi[0] >= tir[0] and ennemi[1] >= tir[1] - 8 and ennemi[1] <= \
                            tir[1]:
                        ennemi[2] -= 1
                        ennemi[4] = True
                        if tir in self.tirs:
                            self.tirs.remove(tir)
                        if ennemi[2] == 0:
                            if ennemi in self.ennemis:
                                ennemi[4] = True
                                self.ennemis.remove(ennemi)
                                self.explosion_creation(ennemi)

                elif tir[3] == True:
                    if ennemi[0] <= tir[0] and ennemi[0] + 7 >= tir[0] and ennemi[1] + 8 >= tir[1] and ennemi[1] <= tir[
                        1] - 4:
                        ennemi[2] -= 1
                        ennemi[4] = True
                        if tir in self.tirs:
                            self.tirs.remove(tir)
                        if ennemi[2] == 0:
                            if ennemi in self.ennemis:
                                ennemi[4] = True
                                self.ennemis.remove(ennemi)
                                self.explosion_creation(ennemi)

        for ennemi in self.ennemis:

            if self.epee[1] != 0:
                if self.haut == True:
                    if ennemi[0] >= self.x - 7 and ennemi[0] <= self.x + 14 and ennemi[1] >= self.y - 20 and ennemi[
                        1] <= self.y - 8:
                        if ennemi in self.ennemis:
                            ennemi[4] = True
                            self.ennemis.remove(ennemi)
                            self.explosion_creation(ennemi)

                elif self.droite == False:
                    if ennemi[0] >= self.x - 16 and ennemi[0] <= self.x and ennemi[1] >= self.y - 5 and ennemi[
                        1] <= self.y + 13:
                        if ennemi in self.ennemis:
                            ennemi[4] = True
                            self.ennemis.remove(ennemi)
                            self.explosion_creation(ennemi)

                else:
                    if ennemi[0] >= self.x and ennemi[0] <= self.x + 16 and ennemi[1] >= self.y - 5 and ennemi[
                        1] <= self.y + 13:
                        if ennemi in self.ennemis:
                            self.ennemis.remove(ennemi)
                            self.explosion_creation(ennemi)

    def collisions_vaisseau(self):

        for ennemi in self.ennemis:
            if self.y <= ennemi[1] + 8 and self.y >= ennemi[1] - 8 and self.x <= ennemi[0] + 8 and self.x + 8 >= ennemi[
                0]:
                if self.epee[1] > 15 or self.epee[1] == 0:
                    self.ennemis.remove(ennemi)
                    self.vies -= 1
                    self.ennemi_ded += 1

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

    def creation_ennemi(self):

        if self.zone == 1 and self.ennemi_ded == 0 and len(self.ennemis) < 2:
            en1 = Ennemi(0, 90, 4, 30, 0, 20, True)
            en2 = Ennemi(120, 90, 4, 30, 100, 120, False)
            self.ennemis.append(en1.ennemis_creation())
            self.ennemis.append(en2.ennemis_creation())

    def ennemi_deplacement(self):
        for ennemi in self.ennemis:

            dep_en = Deplacement_ennemi(ennemi, self.x, self.y, self.collisions)

            ennemi[0] = dep_en.deplacement_horizontal()
            ennemi[1] = dep_en.deplacement_vertical()

    def restart(self):
        """
        réinitialise tout le bordel quand self.vies tombe à 0
        """
        if self.vies == 0:
            if pyxel.btnr(pyxel.KEY_F):
                self.x = 60
                self.y = 90
                self.tirs = []
                self.epee = [False, 0]
                self.ennemis = []
                self.plateformes = []
                self.explosions = []
                self.g_explosions = []
                self.heal = []
                self.vies = 10
                self.saut = False
                self.c_saut = 0
                self.c_sec = 0
                self.c_ennemis = 60
                self.sol = 90
                self.chrono = 0
                self.c_m = 0
                self.g_charge = 0
                self.g_tirs = []
                self.droite = True
                self.haut = False
                self.boum_ok = []

    def update(self):

        self.creation_ennemi()
        self.ennemi_deplacement()
        self.deplacement()
        self.sauter(self.saut, self.sol)
        self.descente(self.saut)
        self.tirs_creation()
        self.tirs_deplacement()
        self.collisions_tirs()
        self.collisions_vaisseau()
        self.restart()
        self.explosion_deplacement()
        self.compte_a_rebours()
        self.compte_tout_court()
        self.epee_creation()
        self.heal_deplacement()
        self.gros_tirs_creation()
        self.boum()
        self.g_explosion_deplacement()

    def draw(self):

        pyxel.cls(0)

        if self.vies > 0:
            pyxel.rect(self.x, self.y, 8, 8, 9)
            pyxel.text(5, 5, 'VIES:' + str(self.vies), 7)
            if self.c_sec < 10:
                pyxel.text(105, 5, str(self.c_m) + ":0" + str(self.c_sec), 7)
            else:
                pyxel.text(105, 5, str(self.c_m) + ":" + str(self.c_sec), 7)
            for tir in self.tirs:
                if tir[3] == False:
                    pyxel.rect(tir[0], tir[1], 4, 1, 10)
                else:
                    pyxel.rect(tir[0], tir[1] - 2, 1, 4, 10)
            for g in self.g_tirs:
                if g[3] == False:
                    pyxel.rect(g[0], g[1], 4, 1, 11)
                else:
                    pyxel.rect(g[0], g[1] - 2, 1, 4, 11)

            for ennemi in self.ennemis:
                if ennemi[4] == False:
                    pyxel.rect(ennemi[0], ennemi[1], 8, 8, 14)
                elif ennemi[3] == True:
                    pyxel.rect(ennemi[0], ennemi[1], 8, 8, 11)
            for h in self.heal:
                pyxel.rect(h[0], h[1], 8, 8, 6)
            for explosion in self.explosions:
                pyxel.circb(explosion[0] + 4, explosion[1] + 4, 2 * (explosion[2] // 4), 8 + explosion[2] % 3)

            if self.epee[1] != 0:
                if self.haut == True:
                    pyxel.rect(self.x + 3, self.y - 10, 2, 10, 9)

                elif self.droite == True:
                    pyxel.rect(self.x + 8, self.y + 3, 8, 2, 9)
                else:
                    pyxel.rect(self.x - 8, self.y + 3, 8, 2, 9)
            for col in self.collisions:
                pyxel.rect(col[0][0], col[0][1] + 8, abs(col[0][0]-col[1][0]), abs(col[0][1]-col[2][1]), 5)

        else:
            pyxel.text(50, 64, 'GAME OVER', 7)
            pyxel.text(29, 94, 'PRESS F TO RESTART', 7)

class Ennemi:
    def __init__(self, absc, ordo, pv, range, trajet_droite, trajet_gauche, direction):
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
    def ennemis_creation(self):
        """
        :return: [abscisse, ordonnée, pv, range, touché ou pas]
        ajoute la liste à la liste d'ennemis de app
        """
        return [self.absc, self.ordo, self.pv, self.range, False, self.trajd, self.trajg, self.dir]

class Deplacement_ennemi:

    def __init__(self, ennemi, x, y, collisions):
        """
        prend en paramètre l'ennemi à déplacer, les coordonnées du joueur et la liste des collisions avec l'environnement
        """
        self.ennemi = ennemi
        self.x = x
        self.y = y
        self.collisions = collisions

    def deplacement_horizontal(self):
        """
        si l'abscisse du joueur rentre dans la range de l'ennemi (self.ennemi[0] + self.ennemi[3]), l'ennemi se
        déplace vers lui (test de collisions pour voir s'il rencontre un obstacle)

        :return: la nouvelle abscisse de l'ennemi
        """
        ok = 0

        if self.x >= (self.ennemi[0] - self.ennemi[3]) and self.x + 8 <= self.ennemi[0]:
            ok = 2
            for col in self.collisions:
                if self.ennemi[0]-1 == col[2][0] and self.ennemi[1]+8 > col[0][1] and self.ennemi[1] < col[2][1]:
                    ok = 0

        elif self.x <= (self.ennemi[0] + 8 + self.ennemi[3]) and self.x >= self.ennemi[0] + 8:

            ok = 1
            for col in self.collisions:
                if self.ennemi[0]+1 == col[0][0] and self.ennemi[1]+8 > col[0][1] and self.ennemi[1] < col[2][1]:
                        ok = 0

        if ok == 0:
            return self.deplacement_horizontal_defaut()
        elif ok == 1:
            return self.ennemi[0]+1
        else:
            return self.ennemi[0]-1

    def deplacement_horizontal_defaut(self):
        if self.ennemi[0] == self.ennemi[5]:
            self.ennemi[7] = True
        elif self.ennemi[0] == self.ennemi[6]:
            self.ennemi[7] = False

        if pyxel.frame_count % 5 == 0:
            if self.ennemi[0] < self.ennemi[6] and self.ennemi[7] == True:
                return self.ennemi[0]+1
            elif self.ennemi[0] > self.ennemi[5] and self.ennemi[7] == False:
                return self.ennemi[0]-1
            elif self.ennemi[0] > self.ennemi[6]:
                return self.ennemi[0]-1
            elif self.ennemi[0] < self.ennemi[5]:
                return self.ennemi[0]+1
        else:
            return self.ennemi[0]



    def deplacement_vertical(self):
        """
        parcours de toutes les boîtes de collision avec for et test de collision
        si l'ennemi n'est sur aucune boîte de collision, on le fait descendre
        :return: la nouvelle ordonnée de l'ennemi
        """
        ok = True
        for col in self.collisions :
            if self.ennemi[0] >= col[0][0] - 8 and self.ennemi[0] <= col[2][0] and self.ennemi[1] + 8 == col[0][1] :
                ok = False

        if ok == True and self.ennemi[1]+1 <= 90:
            return self.ennemi[1] + 1
        else:
            return self.ennemi[1]


App()

