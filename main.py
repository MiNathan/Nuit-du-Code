import pyxel as p
import random as r

allies = [[], [], [], []] # Vaisseaux allie
ennemis = [[], [], [], []]# Vaisseaux ennemis


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
        self.cible = self
        if type == "fregate":
            self.pv = 20
            self.str_atk = 2 # Les attaques font 1 dégats
            self.cap = 0
            self.coords = (0, 0, 32, 16) # Les coordonées dans le fichier pyxel

        if type == "destroyer":
            self.pv = 30
            self.str_atk = 5 # Les attaques font 2 dégats
            self.cap = 0
            self.coords = (0, 20, 56, 24) # Les coordonées dans le fichier pyxel

        if type == "porte-vaisseau":
            self.pv = 50
            self.str_atk = 0
            self.cap = 3
            self.coords = (0, 0, 32, 16) # Les coordonées dans le fichier pyxel

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
        self.cible.prends_degats(self.str_atk)

    def selection_cible(self):
        if self.equipe == "allies" and not self.coule():
            i_tab = 0
            if ennemis[i_tab] == [] and i_tab < len(ennemis[i_tab]):
                i_tab += 1
            else:
                self.cible = r.choice(ennemis[i_tab])

        if self.equipe == "ennemis" and not self.coule():
            i_tab = 0
            if allies[i_tab] == [] and i_tab < len(allies[i_tab]):
                i_tab += 1
            else:
                self.cible = r.choice(allies[i_tab])

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
        allies[0].append(Vaisseau("fregate", "allies", 4, 236))
        allies[0].append(Vaisseau("fregate", "allies", 40, 236))
        allies[0].append(Vaisseau("destroyer", "allies", 4, 206))
        allies[0].append(Vaisseau("destroyer", "allies", 64, 206))
        ennemis[0].append(Vaisseau("fregate", "allies", 4, 4))
        ennemis[0].append(Vaisseau("fregate", "allies", 40, 4))

        p.run(self.update, self.draw)

    def victoire(self):
        compteur_vais_a = 0
        compteur_pertes_a = 0
        for tab in allies:
            for vais in tab:
                compteur_vais_a += 1
                if vais.coule():
                    compteur_pertes_a += 1
                print("allies:", (compteur_vais_a, compteur_pertes_a))

        compteur_vais_e = 0
        compteur_pertes_e = 0
        for tab in ennemis:
            for vais in tab:
                compteur_vais_e += 1
                if vais.coule():
                    compteur_pertes_e += 1
                print("ennemis:", (compteur_vais_e, compteur_pertes_e))

        if compteur_pertes_a == compteur_vais_a or compteur_pertes_e == compteur_vais_e: 
            if compteur_pertes_a == compteur_vais_a:
                print("Les ennemis ont gagné la bataille")
            if compteur_pertes_e == compteur_vais_e:
                print("Les allies ont gagné la bataille")
            p.quit()

    def update(self):
        for tab in allies:
            for vais in tab:
                if vais.get_cible().coule():
                    vais.selection_cible()
        if p.btnp(p.KEY_SPACE):
            for tab in allies:
                for vais in tab:
                    vais.attaquer(vais.get_cible)
            for tab in ennemis:
                for vais in tab:
                    vais.attaquer(vais.get_cible)
            self.victoire()

    def draw(self):
        p.cls(0)
        p.line(0, 127, 256, 127, 1)
        p.line(0, 128, 256, 128, 1)
        for tab in allies:
            for vais in tab:
                vais.draw_vais()
        for tab in ennemis:
            for vais in tab:
                vais.draw_vais()

App()