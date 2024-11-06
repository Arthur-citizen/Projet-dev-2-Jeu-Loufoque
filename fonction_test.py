'''
import math
import pygame
import random
questions_rand = ["Pourquoi le ciel est bleu ?", "Pourquoi la Terre est-elle ronde ?", "Où est le Nord ?", "regarde la porte."]
réponse_rand = ["Parce qu'il serai rouge sinon", "Parce que tu crois qu'elle est ronde ?? Ferme le jeu si tu penses que oui!!!"]

def random_range(min=0, max=10):
    return random.uniform(min, max)
    
def rand_list(list):
    return random.choice(list)



# par la même occasion cela importe pygame.locals dans l'espace de nom de Pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
coordonee_block = [[30, 30],
            [100, 30],
            [170, 30],
            [240, 30],
            ]
liste_color = ["red", "blue", "green", "purple"]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # pygame.draw.circle(screen, "red", player_pos, 40)
    for position in coordonee_block:
            pygame.draw.rect(screen, random.choice(liste_color), pygame.Rect(position, (60, 60)),  2, 3)


    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
'''
'''
import tkinter as tk
import random

# Couleurs pour chaque type de case
couleurs = {
    "VIDE": "white",
    "NEUTRE": "blue",
    "JEU": "orange",
    "EVENT": "purple",
    "DEPART": "green",
    "ARRIVE": "red",
    "JOEUR": "yellow"
}

# Classe représentant chaque case du plateau
class Case:
    def __init__(self, type):
        self.type = type

# Classe représentant le joueur
class Joueur:
    def __init__(self, depart):
        self.pos = depart  # Position du joueur sur la liste des cases

    def deplacer(self, nb_cases, plateau):
        prochaine_position = self.pos + nb_cases
        if prochaine_position >= len(plateau.cases):
            print("Le joueur a atteint la fin!")
            self.pos = len(plateau.cases) - 1  # Position finale
        else:
            self.pos = prochaine_position

# Classe représentant le plateau de jeu
class Plateau:
    def __init__(self, nbCases):
        self.size = 10  # Taille réduite pour un affichage compact
        self.cases = self.createCase(nbCases)
        self.plat = self.fairePlateau()
        self.plat = self.clearMat(self.plat)
        self.joueur = Joueur(0)  # Initialiser le joueur à la case départ
        self.tailleCase = 30     # Taille graphique d'une case

    # Création des cases avec des types aléatoires
    def createCase(self, nbCase):
        cases = [Case("DEPART")]
        eventProb = 0.05
        miniProb = 0.1
        possiblilite = ["NEUTRE", "JEU", "EVENT"]
        probabilites = [1 - miniProb - eventProb, miniProb, eventProb]

        for i in range(nbCase - 2):
            type = random.choices(possiblilite, weights=probabilites, k=1)[0]
            cases.append(Case(type))
        
        cases.append(Case("ARRIVE"))
        return cases

    # Création du plateau de manière aléatoire
    def fairePlateau(self):
        plat = [[Case("VIDE") for _ in range(self.size)] for _ in range(self.size)]
        pos = (self.size // 2, self.size // 2)
        plat[pos[0]][pos[1]] = self.cases[0]  # Départ au centre du plateau
        ban = {pos}

        for cas in self.cases[1:]:
            nextPos = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
            random.shuffle(nextPos)
            for np in nextPos:
                if 0 <= np[0] < self.size and 0 <= np[1] < self.size and np not in ban:
                    plat[np[0]][np[1]] = cas
                    ban.add(np)
                    pos = np
                    break
        return plat

    # Nettoyage des lignes et colonnes vides
    def clearMat(self, plat):
        return plat  # Simplifié pour ce contexte

    # Méthode pour afficher le plateau et le joueur
    def afficher(self):
        # Initialiser la fenêtre
        root = tk.Tk()
        root.title("Plateau de jeu")
        
        # Création du canvas
        canvas = tk.Canvas(root, width=self.size * self.tailleCase, height=self.size * self.tailleCase)
        canvas.pack()

        # Dessin des cases
        for i in range(self.size):
            for j in range(self.size):
                couleur = couleurs[self.plat[i][j].type]
                x0, y0 = j * self.tailleCase, i * self.tailleCase
                x1, y1 = x0 + self.tailleCase, y0 + self.tailleCase
                canvas.create_rectangle(x0, y0, x1, y1, fill=couleur, outline="white")

        # Dessiner le joueur en forme de triangle
        self.joueur_triangle = self.dessiner_joueur(canvas)
        
        # Bouton pour déplacer le joueur
        btn = tk.Button(root, text="Lancer le dé et déplacer", command=lambda: self.deplacer_joueur(canvas))
        btn.pack()

        root.mainloop()

    # Fonction pour dessiner le joueur
    def dessiner_joueur(self, canvas):
        pos = self.trouver_position_case(self.joueur.pos)
        if pos:
            x, y = pos
            taille = self.tailleCase // 2
            return canvas.create_polygon(
                x, y - taille,
                x - taille, y + taille,
                x + taille, y + taille,
                fill=couleurs["JOEUR"]
            )

    # Trouver la position graphique d'une case
    def trouver_position_case(self, index):
        case_count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.plat[i][j].type != "VIDE":
                    if case_count == index:
                        x = j * self.tailleCase + self.tailleCase // 2
                        y = i * self.tailleCase + self.tailleCase // 2
                        return (x, y)
                    case_count += 1
        return None

    # Déplacer le joueur
    def deplacer_joueur(self, canvas):
        nb_cases = random.randint(1, 6)
        self.joueur.deplacer(nb_cases, self)
        nouvelle_position = self.trouver_position_case(self.joueur.pos)
        
        # Mettre à jour la position graphique du joueur
        if nouvelle_position:
            x, y = nouvelle_position
            taille = self.tailleCase // 2
            canvas.coords(self.joueur_triangle,
                x, y - taille,
                x - taille, y + taille,
                x + taille, y + taille
            )
        if self.joueur.pos == len(self.cases) - 1:
            print("Le joueur a atteint la fin du parcours !")

# Initialiser et afficher le plateau
t = Plateau(30)
t.afficher()
'''

import tkinter as tk
import random
from mini_jeu_1 import random_mini_jeu_mp3

couleurs = {
    "VIDE": "white",
    "NEUTRE": "blue",
    "JEU": "orange",
    "EVENT": "purple",
    "DEPART": "green",
    "ARRIVE": "red",
    "JOEUR": "yellow"
}
#liste musique pour mini-jeu
mp3 = ["musique/emotional-piano.mp3",
       "musique/rise-of-legends.mp3",
       "musique/serenity.mp3",
       "musique/songs-of-the-oued.mp3"]
#test pour commit

class Case:
    def __init__(self, type):
        self.type = type  # Couleur par défaut de la case

    def __str__(self):
        return f"{self.type}"


class Joueur:
    def __init__(self, depart):
        self.pos = depart

    def deplacer(self, nb_cases, plateau):
        prochaine_position = self.pos + nb_cases
        if prochaine_position >= len(plateau.cases):
            print("Le joueur a atteint la fin!")
            self.pos = len(plateau.cases) - 1  #position finale
        else:
            self.pos = prochaine_position
            #vérifie si le joueur atterrit sur une case "JEU"
            if plateau.cases[self.pos].type == "JEU":
                print("Vous êtes sur une case de mini-jeu!")
                if random_mini_jeu_mp3(random.choice(mp3)):
                    print("Mini-jeu réussi !")
                else:
                    print("Mini-jeu échoué.")



class Plateau:
    def __init__(self, nbCases):
        self.size = 50
        self.cases = self.createCase(nbCases)
        self.plat = self.fairePlateau()
        self.plat = self.clearMat(self.plat)

    def createCase(self, nbCase):
        cases = [Case("DEPART")]
        eventProb = 0.05
        miniProb = 0.1
        possiblilite = ["NEUTRE", "JEU", "EVENT"]
        probabilites = [1 - miniProb - eventProb, miniProb, eventProb]

        for i in range(nbCase):
            type = random.choices(possiblilite, weights=probabilites, k=1)[0]
            cases.append(Case(type))
            if type == "JEU":
                probabilites[0], probabilites[1], probabilites[2] = 1 - miniProb - (
                            probabilites[2] + eventProb), miniProb, probabilites[2] + eventProb
            elif type == "EVENT":
                probabilites[0], probabilites[1], probabilites[2] = 1 - eventProb - (probabilites[1] + miniProb), \
                                                                    probabilites[1] + miniProb, eventProb
            else:
                probabilites[0] -= (miniProb + eventProb)
                probabilites[1] += miniProb
                probabilites[2] += eventProb

        cases.append(Case("ARRIVE"))
        return cases

    def clearMat(self, plat):
        # clear lignes de 0
        for i in range(len(plat) - 1, -1, -1):
            if all(cell.type == "VIDE" for cell in plat[i]):
                plat.pop(i)
        # clear colone de 0
        for i in range(len(plat[0]) - 1, -1, -1):
            temp = []
            for j in plat:
                temp.append(j[i])
            if all(cell.type == "VIDE" for cell in temp):
                for j in plat:
                    j.pop(i)
        return plat

    def fairePlateau(self):

        tentative = 100
        while tentative > 0:
            try:
                pos = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
                plat = [[Case("VIDE") for i in range(self.size)] for j in range(self.size)]
                ban = {pos}

                for cas in self.cases:
                    plat[pos[0]][pos[1]] = cas

                    nextPos = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
                    random.shuffle(nextPos)
                    find = False
                    while not find:
                        if len(nextPos) == 0:
                            break
                        tryy = nextPos.pop()

                        if len(plat) > tryy[0] >= 0 and len(plat) > tryy[1] >= 0 and tryy not in ban:
                            voisins = [(tryy[0] + 1, tryy[1]), (tryy[0] - 1, tryy[1]), (tryy[0], tryy[1] + 1),
                                       (tryy[0], tryy[1] - 1)]
                            ok = True
                            for v in voisins:
                                if not (plat[v[0]][v[1]] == cas or plat[v[0]][v[1]].type == "VIDE"):
                                    ok = False
                                    break

                            if ok:
                                pos = tryy
                                ban.add(pos)
                                find = True
                    if not find:
                        raise Exception("Pas de place")
                return (plat)
            except:
                tentative -= 1

    def afficher(self):
        root = tk.Tk()
        root.title("Plateau Interface")
        tailleCase = 30
        canvas_width = len(self.plat[0]) * tailleCase
        canvas_height = len(self.plat) * tailleCase
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        canvas.pack()

        for i in range(len(self.plat)):
            for j in range(len(self.plat[i])):
                couleur = couleurs[self.plat[i][j].type] if self.plat[i][j] else couleurs[self.plat[i][j]]
                x0, y0 = j * tailleCase, i * tailleCase
                x1, y1 = x0 + tailleCase, y0 + tailleCase
                canvas.create_rectangle(x0, y0, x1, y1, fill=couleur, outline=("black" if couleur != "white" else ""))

        root.mainloop()

    def __str__(self):
        if not self.plat:
            return 'prob'
        s = ""
        for row in self.plat:
            if s:
                s += " \n"
            for elem in row:
                if elem > 9:
                    s += str(elem) + " "
                else:
                    s += str(elem) + "  "
        return s


t = Plateau(30)
t.afficher()
random_mini_jeu_mp3(random.choice(mp3))
