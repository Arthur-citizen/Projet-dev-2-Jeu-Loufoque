import random

import tkinter as tk
from PIL import Image, ImageTk

from model import Joueur, Combinaison, Phrase, MiniJeuMusical, Case


class Menu:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.geometry("540x540")
        self.fenetre.title("Jeu de plateau Loufoque")

        # Charger le GIF comme fond
        self.gif = Image.open("assets/images/bg.gif")
        self.gif_frames = []
        # stock les images du gif dans une liste "self.gif_frames = []"
        for i in range(self.gif.n_frames):
            self.gif.seek(i)
            frame = ImageTk.PhotoImage(self.gif.copy())
            self.gif_frames.append(frame)
        # set la première image du gif
        self.background_label = tk.Label(self.fenetre, image=self.gif_frames[0])
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # anime du GIF
        self.current_frame = 0
        self.animate_gif()

        # crée les titres
        self.titre = tk.Label(
            self.fenetre,
            text="Préparez-vous pour un jeu renversant",
            background="black",
            font=("Arial", 15),
            fg="green"
        )
        self.titre1 = tk.Label(
            self.fenetre,
            text="Ouvrez la porte",
            background="black",
            font=("Arial", 15),
            fg="green",
            width=14
        )
        # positionner les titres
        self.titre.place(relx=0.5, rely=0.13, anchor=tk.CENTER)  # 13% en hauteur depuis le heut de la fenêtre
        self.titre1.place(relx=0.5, rely=0.18, anchor=tk.CENTER)  # 18% du haut de la fenêtre

        self.porte = tk.PhotoImage(file="assets/images/porte_menu.png")  # charge la porte
        self.bouton_start = tk.Button(
            self.fenetre,
            image=self.porte,
            command=self.start_game,
            bg="black",
            highlightthickness=0,
            border=0,
            activebackground="black"
        )
        # place le boutton
        self.bouton_start.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # fais une rotation dans la liste "gif_frames = []" avec 25ms d'interval entre chaque image
    def animate_gif(self):
        """
        - la fonction utiilise le GIF bg.gif, sépare toutes les images composants le GIF dans une liste
        - fais défiler la liste d'image avec un intervalle de 25 millisecondes entre chaque image
        PRE:
            - l'initialisation de la liste self.gif_frames c'est passé correctement
            - self.current_frame à bien été initialisé dans le init
        POST:
            - except: erreur dans l'éxécution de la fonction animate_gif
        """
        try:
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.background_label.configure(image=self.gif_frames[self.current_frame])
            self.fenetre.after(25, self.animate_gif)
        except:
            print("erreur fonction anime_gif")

    def start_game(self):
        # fermer le menu
        self.fenetre.destroy()

        # Lance le plateau
        plateau = Plateau(60)
        plateau.afficher()

    def afficher(self):
        self.fenetre.mainloop()


class Plateau:
    def __init__(self, nombre_cases):
        self.__couleurs = {  # Sert pour la couleur des cases
            "VIDE": "white",
            "NEUTRE": "blue",
            "JEU": "orange",
            "EVENT": "purple",
            "DEPART": "green",
            "ARRIVE": "red",
            "JOUEUR": "yellow"
        }
        self.__wav = ["emotional.wav",
                      "rise.wav",
                      "serenity.wav",
                      "oued.wav"]
        self.size = 50  # dimension du carré dans lequel on va essayer de placer les cases
        self.nombre_cases = nombre_cases
        self.create_cases()  # On créé un certain nombre (nbcases) de Case
        self.largeur_fenetre, self.hauteur_fenetre = 800, 600
        self.faire_plateau()
        self.clear_matrice()
        self.joueur = Joueur(0)
        self.update_pos_in_case()
        pays = []

        for letter in range(ord('a'), ord('z') + 1):
            pays.append(f"Essaye de trouver un pays dont la première lettre est '{chr(letter)}'. :)")
        self.defi = ["Fais 5 pompes, histoire de te décoller le derrière de ta chaise. :-)",
                     "Voyons comme tu t'en sors pour réciter l'alphabet à l'envers sans faute ! Allez,on t'écoute ! ;D",
                     pays, "Allez, compte jusque 100 le plus vite possible !",
                     "Allez, bouge un peu et tiens en équilibre sur une jambe pendant dix secondes. Je suis sympa, je "
                     "te laisse choisir laquelle. ';-)"]

        self.jeu = [Phrase(), Combinaison(), MiniJeuMusical(self.__wav)]

    @property
    def couleurs(self):
        return self.__couleurs

    @property
    def wav(self):
        return self.wav

    def update_pos_in_case(self):
        """
        La méthode va mettre a jour la position de chaque case

        PRE : -L'attribut Cases doit être non vide et être une liste d'objet Case
              -L'attribut Plateau doit être une liste de liste d'objet Case
        POST : Met a jour la postition de chaque case dans l'attribut Cases
        """
        previous = None
        act = self.trouveDepart()
        self.cases[0].position = act
        for i in range(1, len(self.cases)):

            voisins = [(act[0] + 1, act[1]), (act[0] - 1, act[1]), (act[0], act[1] + 1), (act[0], act[1] - 1)]
            for v in voisins:
                if 0 <= v[0] < len(self.plateau) and 0 <= v[1] < len(self.plateau[0]) and self.plateau[v[0]][
                    v[1]].type != "VIDE" and v != previous:
                    self.cases[i].position = v
                    previous = act
                    act = v
                    break

    def create_cases(self):
        """
        On fait en sorte d'avoir un certain nbCase de différent avec un type choisis aléatoirement, on commence
        toujours avec une case
        départ et fini par une case arrivé

        PRE : nbCase : int >= 0
        POST : - Creer l'attribut cases qui contient une liste d'object Case
        """
        self.cases = [Case("DEPART")]
        eventProb = 0.025
        miniProb = 0.05
        possiblilite = ["NEUTRE", "JEU", "EVENT"]
        # probabilité associé au différente possibilié, il faudrait en faire un dictionnaire
        probabilites = [1 - miniProb - eventProb, miniProb, eventProb]

        for i in range(self.nombre_cases + 2):
            # choisis un type de cases alléatoirement en fonction des probabilité
            type = random.choices(possiblilite, weights=probabilites, k=1)[0]
            self.cases.append(Case(type))

            if type == "JEU":
                probabilites[1] = miniProb
                probabilites[2] += eventProb

            elif type == "EVENT":
                probabilites[1] += miniProb
                probabilites[2] = eventProb
            else:
                probabilites[1] += miniProb
                probabilites[2] += eventProb

            probabilites[0] = 1 - probabilites[1] - probabilites[2]

        self.cases.append(Case("ARRIVE"))

    def clear_matrice(self):
        """
        Cette méthode sert a enlever toute les lignes/colones inutile pour que la taille du rectangle affiché soit le plus petit possible

        PRE : plat doit être une liste de liste de Case
        POST : Enleve les lignes et colones qui ne contiennent uniquement des cases de type vide.
        """

        for i in range(len(self.plateau) - 1, -1, -1):  # clear lignes de case vide
            if all(cell.type == "VIDE" for cell in self.plateau[i]):
                self.plateau.pop(i)
        for i in range(len(self.plateau[0]) - 1, -1, -1):  # clear colone de case vide
            temp = []
            for j in self.plateau:
                temp.append(j[i])
            if all(cell.type == "VIDE" for cell in temp):
                for j in self.plateau:
                    j.pop(i)

    def trouveDepart(self):
        for i in range(len(self.plateau)):
            for j in range(len(self.plateau[i])):
                if self.plateau[i][j].type == "DEPART":
                    return (i, j)

    def faire_plateau(self):
        """
        On essaye de faire placer toute les cases de self.cases l'une a la suite de l'autre de facon aléatoire, une case peut
        toucher une seul autre case et elle doivent rester dans un carré de taille self.size
        PRE : - self.size doit être un int >=0
              - self.cases doit être une liste d'objet Case non vide

        POST : Place dans self.plateau une liste de liste d'Objet case formant un chemin de forme aléatoire
        RAISE : Si aucun placement n'est possible car un nombre trop élévé de case à placé, un erreur est déclanché
        """
        temp = 0  # mettre un .time() pour avoir 220 sec de charge ou moins, on essaye {tentative} fois avec une taille de plateau et apres on augmente la taille

        while temp < 100000:
            tentative = 0
            while tentative < 100:
                position = (
                    random.randint(0, self.size - 1), random.randint(0, self.size - 1))  # position de la case depart
                plat = [[Case("VIDE") for i in range(self.size)] for j in
                        range(self.size)]  # on remplit le plateau de cases vide
                ban = {position}  # stok les positions utilisé
                for cas in self.cases:
                    print(cas)
                    plat[position[0]][position[1]] = cas

                    nextPos = [(position[0] + 1, position[1]), (position[0] - 1, position[1]),
                               (position[0], position[1] + 1),
                               (position[0], position[1] - 1)]  # postions des cases dans les 4 directions
                    random.shuffle(nextPos)  # change ordre
                    find = False  # nouvelle position trouvé ?
                    while not find and len(nextPos):
                        tryy = nextPos.pop()  # on prend une pose pour essayer

                        if tryy not in ban and len(plat) > tryy[0] >= 0 and len(plat) > tryy[
                            1] >= 0:  # on regarde si la case est déja utilisé ou si elle n'est pas dans les limites
                            voisins = [(tryy[0] + 1, tryy[1]), (tryy[0] - 1, tryy[1]), (tryy[0], tryy[1] + 1),
                                       (tryy[0], tryy[1] - 1)]  # voisin de la case a essayer
                            ok = True  # est ce que tout les voisins sont vides ? (sauf celle de la case précédente car il doit y avoir un poitn d'accrochen entre 2 cases
                            for v in voisins:
                                if 0 <= v[0] < len(plat) and 0 <= v[1] < len(plat[0]):
                                    if not (plat[v[0]][v[1]] == cas or plat[v[0]][
                                        v[1]].type == "VIDE"):  # si un des voisins n'est pas vide
                                        ok = False
                                        break

                            if ok:
                                position = tryy
                                ban.add(position)
                                find = True
                    if not find:
                        tentative += 1
                self.plateau = plat
                return

            temp += 1
            self.size += 5

    def lancerDe(self):
        """
        Cette fonction simule un lancé de dé à 6 côté, ensuite elle met le plateau de jeu à jour en fontion de la case sur où atterit le joueur.
        Elle renvoie le résultat du lancé de dé dans  le variable 'num'.
        PRE:
            - joueur.pos doit être un int
        POST:
            - le joueur avance de 1 à 6 cases
            - en fonction du type de case sur où le joueur fini un jeu, mini-jeu, rien ou la fin du jeu
            - 60% de chance d'avoir un défi si le joueur tombe sur une case défi


        """
        num = random.randint(1, 6)
        self.joueur.position += (
            num if (self.joueur.position + num) < len(self.cases) else len(self.cases) - 1 - self.joueur.position)
        self.afficherPlateau()

        if self.cases[self.joueur.position].type == "JEU":
            self.root.update_idletasks()

            random.choice(self.jeu).lancer()

        elif self.cases[self.joueur.position].type == "EVENT":
            self.faire_plateau()
            self.clear_matrice()
            self.update_pos_in_case()
            self.taille_case = self.calculer_taille_case()
            self.afficherPlateau()
        elif self.cases[self.joueur.position].type == "ARRIVE":
            print("win gg")
            self.root.quit()

        else:
            if random.randint(1, 10) > 4:
                t = (random.choice(self.defi))
                if type(t) == list:
                    t = random.choice(t)
                print(t)

    def afficherPlateau(self):
        """
        Cette méthode affiche avec un interface graphique le plateau de jeu et le joueur

        PRE :  -self.plateau doit être une liste de liste d'objet Case
               -self.cases doit être une liste d'objet Case
               -self.joueur doit être un Objet Joueur

        POST : Le plateau est afficher sur le canevas

        """

        self.canvas.delete('all')
        for i in range(len(self.plateau)):
            for j in range(len(self.plateau[i])):
                couleur = self.__couleurs[self.plateau[i][j].type]
                x0, y0 = j * self.taille_case, i * self.taille_case  # coins haut gauche
                x1, y1 = x0 + self.taille_case, y0 + self.taille_case  # coins bat droite
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=couleur,
                                             outline=("black" if couleur != "white" else ""))

        joueurY = self.cases[self.joueur.position].position[0] * self.taille_case + self.taille_case // 2
        joueurX = self.cases[self.joueur.position].position[1] * self.taille_case + self.taille_case // 2
        self.canvas.create_oval(joueurX - self.taille_case // 4, joueurY - self.taille_case // 4,
                                joueurX + self.taille_case // 4, joueurY + self.taille_case // 4,
                                fill=self.__couleurs["JOUEUR"])

    def calculer_taille_case(self):

        return min(self.hauteur_fenetre // len(self.plateau), self.largeur_fenetre // len(self.plateau[0]))

    def afficher(self):
        """
        Cette fonction initialise l'affichage du plateau de jeu


        PRE:
            - largeur_Fenetre et hauteur_fenetre doivent être un int
        POST:
            - crée un canvas pour le plateau de jeu
            - ajoute le bouton de lancé de dé
            - affiche le tableau initial
            - démarre la boucle principal avec mainloop()
        """
        self.root = tk.Tk()
        self.root.title("Plateau Interface")

        self.taille_case = self.calculer_taille_case()

        self.canvas = tk.Canvas(self.root, width=self.largeur_fenetre, height=self.hauteur_fenetre)
        self.canvas.pack()

        bouton_De = tk.Button(self.root, text="Lancer le dé", command=self.lancerDe)
        bouton_De.pack()
        self.afficherPlateau()

        self.root.mainloop()

    def __str__(self):
        """
        affichage du plateau en consoel si besoins print(Plateau)
        :return:
        """
        res = '['
        for ligne in self.plateau:
            temp = '['
            for case in ligne:
                temp += case.type + ","
            temp += ']\n'
            res += temp + ','

        return res + ']'
