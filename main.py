import pyxel, random, time


class App:
    def __init__(self):
        pyxel.init(128, 128, "PYXEL1", 30)
        self.x = 60
        self.y = 100
        self.direction=None
        self.saut = False
        self.c_saut = 0
        self.sol=self.y
        self.collisions = [[[0, 112], [128, 112], [128, 128], [0, 128]]]
        self.tirs = []
        self.epee = [False, 0]
        self.ennemis = []
        self.collisions = [[[0, 90], [128, 90], [128, 128], [0, 128]]]
        self.explosions = []
        self.g_explosions = []
        self.heal = []
        self.vies = 10
        self.droite = True
        
        
        #             x1,y1,x2,y2,nom du bloc
        self.niveau1=[[0,0,112,8,1],#bord Haut
                      [0,8,8,128,2],#bord Gauche
                      [8,120,128,128,3],#bord Bas
                      [120,16,128,128,4],#bord droit
                      [70,8,94,16,5],
                      [0,58,40,60,6],
                      [68,112,128,120,7],
                      [80,60,100,68,8],
                      [30,103,46,111,9],
                      [50,85,120,93,8],
                      [28,70,50,74,6]]
        

        pyxel.run(self.update, self.draw)
        
    #and self.x+2>collision[0] and self.y>collision[1] and self.x+2>collision[2] and self.y<collision[3] and self.x+2>collision[4] and self.y>collision[5] and self.x+2>collision[6] and self.y<collision[7]    
            
                
            
                
    def test_collision(self,x_augmentation=0,y_augmentation=0):
        
        for collision in self.niveau1 : 
            
            
            
                       
            if collision[0]<=self.x<=collision[2] and collision[3]==self.y+y_augmentation:
                y_augmentation=0
                
            if collision[0]<=self.x<=collision[2] and collision[1]==self.y+y_augmentation+8:
                y_augmentation=0
                
            elif collision[1]<=self.y<=collision[3] and collision[2]==self.x+x_augmentation or  collision[1]<=self.y+8<=collision[3] and collision[2]==self.x+x_augmentation  :
                x_augmentation=0
                
            elif collision[1]<=self.y<=collision[3] and collision[0]==self.x+x_augmentation+8 or collision[1]<=self.y+8<=collision[3] and collision[2]==self.x+x_augmentation:
                x_augmentation=0
                        
            
                
        self.x+=x_augmentation
        self.y+=y_augmentation
            


    def deplacement(self):
                
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction="right" 
            self.droite=True  
            self.test_collision(1,0) 
               
            
            
        if pyxel.btn(pyxel.KEY_LEFT) :
            self.direction="left"
            self.droite=False
            self.test_collision(-1,0) 
            
        """   
        if pyxel.btn(pyxel.KEY_UP) :
            self.direction="up"
            self.haut=True
            self.test_collision(0,-1) 
           
        if pyxel.btn(pyxel.KEY_DOWN) :
            self.haut=False
            self.direction="down"
            self.test_collision(0,1) 
        """   
        if pyxel.btnr(pyxel.KEY_SPACE):
            
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
            for collision in self.niveau1:
                if collision[0]<=self.x<=collision[2] and collision[1]==self.y+9 or collision[0]<=self.x+8<=collision[2] and collision[1]==self.y+9:
                    self.sol = collision[1]
                    ok = False
            if ok == True and self.y < 112:
                self.y += 3
        if self.y == 112:
            self.sol = 120
            
    def tirs_creation(self):
        """
        sel.tirs (lst) contient des listes contenant [absisce tir, ordonnée tir, bool droite, bool haut, ???keskejaifoutu]
        si KEY_SHIFT est pressée, on ajoute une liste à la liste self.tirs (toute les 7 frames seulement)
        """

        if pyxel.btnp(pyxel.KEY_SHIFT, 7, 7):
            if self.droite == True:
                self.tirs.append([self.x + 8, self.y + 4, self.droite, False])
            else:
                self.tirs.append([self.x - 4, self.y + 4, self.droite, False])

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

        
    

    

    def update(self):

        
        self.deplacement()
        
        self.sauter(self.saut, self.sol)
        self.descente(self.saut)
        self.tirs_creation()
        self.tirs_deplacement()
        
        
        
        

    def draw(self):
        """
                      [0,0,110,10,"haut"],#bord Haut
                      [10,10,10,130,"gauche"],#bord Gauche
                      [10,110,130,110,"bas"],#bord Bas
                      [120,10,130,130,"droite"],#bord droit
                      [70,10,90,20,"1"],
                      [0,50,30,60,"4"],
                      [70,110,130,120,"9"]
                      ]
        """
        pyxel.cls(0)
        #draw box
        for col in self.niveau1:
            pyxel.rect(col[0], col[1], abs(col[0]-col[2]), abs(col[1]-col[3]), col[4]) 
            
        #draw tir    
        for tir in self.tirs:
                if tir[3] == False:
                    pyxel.rect(tir[0], tir[1], 4, 1, 10)
                else:
                    pyxel.rect(tir[0], tir[1] - 2, 1, 4, 10)
            
        
        

        #draw mob
        pyxel.rect(self.x, self.y, 8, 8, 9)
            

        

        



App()