import random

import tkinter as tk
from PIL import Image, ImageTk

from model import LogicPlateau


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
        plateau = LogicPlateau(60)
        gui = GUIPlateau(plateau)
        gui.afficher()

    def afficher(self):
        self.fenetre.mainloop()


class GUIPlateau:
    def __init__(self, model):
        self.model = model
        self.root = tk.Tk()
        self.root.title("Plateau Interface")
        self.largeur_fenetre, self.hauteur_fenetre = 800, 600
        self.taille_case = self.calculer_taille_case()
        self.canvas = tk.Canvas(self.root, width=self.largeur_fenetre, height=self.hauteur_fenetre)
        self.canvas.pack()

        bouton_de = tk.Button(self.root, text="Lancer le dé", command=self.lancer_de)
        bouton_de.pack()

    def afficher_plateau(self):
        """
        Cette méthode affiche avec un interface graphique le plateau de jeu et le joueur

        PRE :  -self.plateau doit être une liste de liste d'objet Case
               -self.cases doit être une liste d'objet Case
               -self.joueur doit être un Objet Joueur

        POST : Le plateau est afficher sur le canevas
        """
        self.canvas.delete('all')
        for i in range(len(self.model.plateau)):
            for j in range(len(self.model.plateau[i])):
                couleur = self.model.couleurs[self.model.plateau[i][j].type]
                x0, y0 = j * self.taille_case, i * self.taille_case
                x1, y1 = x0 + self.taille_case, y0 + self.taille_case
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=couleur,
                                             outline=("black" if couleur != "white" else ""))
        joueur_pos_y = (self.model.cases[self.model.joueur.position].position[0] * self.taille_case + (
                        self.taille_case // 2))
        joueur_pos_x = (self.model.cases[self.model.joueur.position].position[1] * self.taille_case + (
                        self.taille_case // 2))
        self.canvas.create_oval(joueur_pos_x - self.taille_case // 4, joueur_pos_y - self.taille_case // 4,
                                joueur_pos_x + self.taille_case // 4, joueur_pos_y + self.taille_case // 4,
                                fill=self.model.couleurs["JOUEUR"])

    def lancer_de(self):
        self.model.lancer_de()
        # Mettez à jour le modèle en fonction du résultat
        self.afficher_plateau()

        if self.model.cases[self.model.joueur.position].type == "JEU":
            self.root.update_idletasks()

            random.choice(self.model.jeu).lancer()

        elif self.model.cases[self.model.joueur.position].type == "EVENT":
            self.model.faire_plateau()
            self.model.clear_matrice()
            self.model.update_pos_in_case()
            self.taille_case = self.calculer_taille_case()
            self.afficher_plateau()
        elif self.model.cases[self.model.joueur.position].type == "ARRIVE":
            print("win gg")
            self.root.quit()

        else:
            if random.randint(1, 10) > 4:
                t = (random.choice(self.model.defi))
                if type(t) is list:
                    t = random.choice(t)
                print(t)

    def calculer_taille_case(self):
        """
        Calcule la taille des cases
        """
        return min(self.hauteur_fenetre // len(self.model.plateau), self.largeur_fenetre // len(self.model.plateau[0]))

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
        :return:
        """
        self.afficher_plateau()
        self.root.mainloop()
