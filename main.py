import pyxel as p
import random as r

allies = {"fregate": [], "destroyer": [], "porte-vaisseau": [], "sous-vaisseau": []} # Vaisseaux allie
ennemis = {"fregate": [], "destroyer": [], "porte-vaisseau": [], "sous-vaisseau": []} # Vaisseaux ennemis

class Vaisseau:
    """
    Classe pour tous les vaisseaux
    Chaque vaisseau fait partie d'une de 4 classes:
        Fregate; Destroyer; Porte-Vaisseau; Sous-Vaisseau
    Chaque vaisseau fait partie de l'equipe alliee (bleue) ou ennemie (rouge)
    Les vaisseaux on _ attributs:
        pv, int: Points de vie du vaisseau
        spd_atk, int: Temps entre chaques attaques
        str_atk, int: Les dégats infligés par les attaques
        aa, bool: True Si le vaisseau est capable d'attaquer les sous-vaisseaux
        cap, int: Si le vaisseau peut transporter des sous-vaisseaux, sinon égal à 0
    """

    def __init__(self, type, equipe, x, y):
        """
        Initialisation en fonction du type de vaisseau
        Les attributs peuvents être améliorés plus tard avec des crédits
        """
        self.equipe = equipe
        self.x = x
        self.y = y
        self.cible = None
        if type == "fregate":
            self.pv = 20
            self.spd_atk = 120 # Attaque toutes les 2 secondes
            self.str_atk = 3 # Les attaques font 1 dégats
            self.aa = False
            self.cap = 0
            self.coords = (0, 0, 32, 16) # Les coordonées dans le fichier pyxel

        if type == "destroyer":
            self.pv = 30
            self.spd_atk = 300 # Attaque toutes les 5 secondes
            self.str_atk = 5 # Les attaques font 2 dégats
            self.aa = True
            self.cap = 0
            self.coords = (0, 0, 32, 16) # Les coordonées dans le fichier pyxel

        if type == "porte-vaisseau":
            self.pv = 50
            self.spd_atk = 0 # N'attaque pas directement
            self.str_atk = 0
            self.aa = False
            self.cap = 3
            self.coords = (0, 0, 32, 16) # Les coordonées dans le fichier pyxel

        if type == "sous-vaisseau_bombardier":
            self.pv = 5
            self.spd_atk = 180 # Attaque toutes 3 les secondes
            self.str_atk = 2 # Les attaques font 2 dégats
            self.aa = True
            self.cap = 0
            self.coords = (0, 0, 32, 16) # Les coordonées dans le fichier pyxel

        if type == "sous-vaisseau_chasseur":
            self.pv = 5
            self.spd_atk = 30 # Attaque 2 fois par secondes
            self.str_atk = 1 # Les attaques font 1 dégats
            self.aa = False
            self.cap = 0
            self.coords = (0, 0, 32, 16) # Les coordonées dans le fichier pyxel


    def get_coords(self):
        return self.coords

    def get_cible(self):
        return self.cible

    def coule(self):
        """
        Fonction pour determiner si le vaisseau est detruit
        Renvoie True et remplace le vaisseau par un rectangle noir si le vaisseau n'a plus de pv
        Sinon renvoie False
        """
        if self.pv <= 0:
            p.rect(self.coords[0], self.coords[1], self.coords[2], self.coords[3], 0)
            return True
        return False

    def prends_degats(self, degats):
        self.pv -= degats
        self.coule()

    def attaquer(self, cible):
        cible.prends_degats(self.str_atk)

    def selection_cible(self):
        if self.equipe == "allies":
            if self.aa:
                i_tab = r.randint(0, 3)
                self.cible = r.choice(ennemis[i_tab])
            else:
                i_tab = r.randint(0, 2)
                self.cible = r.choice(ennemis[i_tab])

        if self.equipe == "ennemis":
            if self.aa:
                i_tab = r.randint(0, 3)
                self.cible = r.choice(ennemis[i_tab])
            else:
                i_tab = r.randint(0, 2)
                self.cible = r.choice(ennemis[i_tab])

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
        allies["fregate"].append(Vaisseau("fregate", "allies", 4, 236))
        ennemis["fregate"].append(Vaisseau("fregate", "allies", 4, 4))

        p.run(self.update, self.draw)

    def update(self):
        for tab in allies.values():
            for vais in tab:
                vais.selection_cible()

    def draw(self):
        p.cls(0)
        p.line(0, 127, 256, 127, 1)
        p.line(0, 128, 256, 128, 1)
        for tab in allies.values():
            for vais in tab:
                vais.draw_vais()
        for tab in ennemis.values():
            for vais in tab:
                vais.draw_vais()

App()