import pyxel as p
import random as r

allies = [] # Vaisseaux allie
ennemis = []# Vaisseaux ennemis


class UI:
    def __init__(self):
        self.credit = 0

    def get_credit(self):
        return self.credit

    def set_credit(self,val):
        self.credit =val

    def ajout(self):
        coules=[]
        for tab in ennemis.values():
            for vais in tab :
                if vais.coule(): 
                    coules.append(vais)
        for vais in coules:
            self.credit = self.credit - vais.get_pv()
            for tab in ennemis.values():
                for vaisseau in tab :
                    if vaisseau == vais:
                        tab.remove(vaisseau)

                            




class Vaisseau:
    """
    Classe pour tous les vaisseaux
    Chaque vaisseau fait partie d'une de 4 classes:
        Fregate; Destroyer; Porte-Vaisseau; Sous-Vaisseau
    Chaque vaisseau fait partie de l'equipe alliee (bleue) ou ennemie (rouge)
    Les vaisseaux on _ attributs:
        equipe, str: L'equipe auquelle le vaisseau appartient
        x, int: coordonee x dans la fenetre graphique
        y, int: coordonee y dans la fenetre graphique
        pv, int: Points de vie du vaisseau
        str_atk, int: Les dégats infligés par les attaques
        cap, int: Si le vaisseau peut transporter des sous-vaisseaux, sinon égal à 0
        coords, tuple: les coordonees du vaisseau dans le fichier pyxel
    """

    def __init__(self, type, equipe, x, y):
        """
        Initialisation en fonction du type de vaisseau
        Les attributs peuvents être améliorés plus tard avec des crédits
        """
        self.type = type
        self.equipe = equipe
        self.x = x
        self.y = y
        self.cible = self
        if type == "fregate":
            self.pv = 20
            self.str_atk = 2 # Les attaques font 1 dégats
            self.cap = 0
            self.coords = (0, 0, 32, 16) # Les coordonées dans le fichier pyxel

        if type == "destroyer":
            self.pv = 50
            self.str_atk = 5 # Les attaques font 2 dégats
            self.cap = 0
            self.coords = (0, 20, 56, 24) # Les coordonées dans le fichier pyxel

        if type == "porte-vaisseau":
            self.pv = 100
            self.str_atk = 1
            self.cap = 3
            self.coords = (0, 56, 64, 24) # Les coordonées dans le fichier pyxel

        if type == "sous-vaisseau_bombardier":
            self.pv = 5
            self.str_atk = 2 # Les attaques font 2 dégats
            self.cap = 0
            self.coords = (0, 0, 32, 16) # Les coordonées dans le fichier pyxel

        if type == "sous-vaisseau_chasseur":
            self.pv = 5
            self.str_atk = 1 # Les attaques font 1 dégats
            self.cap = 0
            self.coords = (0, 0, 32, 16) # Les coordonées dans le fichier pyxel


    def get_pv(self):
        return self.pv
    
    def set_pv(self,val):
        self.pv = val

    def get_coords(self):
        return (self.x, self.y)

    def get_cible(self):
        return self.cible

    def coule(self):
        """
        Fonction pour determiner si le vaisseau est detruit
        Renvoie True et remplace le vaisseau par un rectangle noir si le vaisseau n'a plus de pv
        Sinon renvoie False
        """
        if self.pv <= 0:
            p.rect(self.x, self.y, self.coords[2], self.coords[3], 0)
            return True
        return False

    def prends_degats(self, degats):
        self.pv -= degats
        self.coule()

    def attaquer(self):
        cible = self.selection_cible()
        if cible != None and not self.coule():
            p.line(self.x, self.y, cible.get_coords()[0], cible.get_coords()[1], 8)
            cible.prends_degats(self.str_atk)

    def selection_cible(self):
        if self.equipe == "allies" and not self.coule():
            i_tab = 0
            if i_tab >= len(ennemis):
                i_tab += 1
            else:
                return r.choice(ennemis)

        if self.equipe == "ennemis" and not self.coule():
            i_tab = 0
            if i_tab >= len(allies):
                i_tab += 1
            else:
                return r.choice(allies)

    def draw_vais(self):
        if self.equipe == "allies":
            p.blt(self.x, self.y, 0, self.coords[0], self.coords[1], self.coords[2], self.coords[3], 0)
        if self.equipe == "ennemis":
            p.blt(self.x, self.y, 1, self.coords[0], self.coords[1], self.coords[2], self.coords[3], 0)


class App:
    def __init__(self):
        p.init(width=256, height=256, title="Bataille Spatiale", fps=60)
        p.load("theme.pyxres")
        p.mouse(True)
        allies.append(Vaisseau("fregate", "allies", 4, 236))
        allies.append(Vaisseau("fregate", "allies", 40, 236))
        allies.append(Vaisseau("destroyer", "allies", 4, 206))
        ennemis.append(Vaisseau("fregate", "ennemis", 4, 4))
        ennemis.append(Vaisseau("destroyer", "ennemis", 4, 34))
        self.tour = 0
        self.menu = 0
        self.ecran = 0
        self.ecran_v = False

        p.run(self.update, self.draw)
    
        
    def ecran_acceuil(self):
        if self.ecran < 102 :
            self.ecran = self.ecran + 1 

        
        if p.btn(p.KEY_SPACE) :
            self.ecran_v = True
        if self.ecran_v == True:
             self.ecran = self.ecran + 1
        if self.ecran == 256:
            self.menu = 1


    def victoire(self):
        compteur_vais_a = 0
        compteur_pertes_a = 0
        for vais in allies:
            compteur_vais_a += 1
            if vais.coule():
                compteur_pertes_a += 1

        compteur_vais_e = 0
        compteur_pertes_e = 0
        for vais in ennemis:
            compteur_vais_e += 1
            if vais.coule():
                compteur_pertes_e += 1

        if compteur_pertes_a == compteur_vais_a or compteur_pertes_e == compteur_vais_e: 
            if compteur_pertes_a == compteur_vais_a:
                print("Les allies ont perdu la bataille")
            if compteur_pertes_e == compteur_vais_e:
                print("Les ennemis ont perdu la bataille")

    def update(self):
        if self.menu == 0 :
            self.ecran_acceuil()
        if self.menu ==1:
            self.victoire()

    def draw(self):
        if self.menu == 0:
            p.cls(0)
            p.blt(self.ecran, 50, 0 , 0 ,0 , 51 ,23)
            if self.ecran == 102:
                p.text(90, 80, "Appuyez sur espace", 7)
        if self.menu == 1:
            p.cls(0)
            p.line(0, 127, 256, 127, 1)
            p.line(0, 128, 256, 128, 1)
            if p.frame_count % 60 == 0:
                print("Tour n°", self.tour)
                self.tour += 1
                for vais in allies:
                    vais.attaquer()
                    vais.draw_vais()
                    vais.coule()
                for vais in ennemis:
                    vais.attaquer()
                    vais.draw_vais()
                    vais.coule()








App()