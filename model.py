import random
import os

from pynput import keyboard
import tkinter as tk
from playsound import playsound  # playsound 1.2.2


class Case:
    def __init__(self, type):
        self.type = type  # Type de case : mini-jeu, départ, neutre, etc.
        self.position = None

    def __str__(self):  # Pour afficher en console la case avec print(Case)
        return f"{self.type}"


class Joueur:
    def __init__(self, depart):
        self.position = depart

    def deplacer(self, deplacement):
        pass


class Phrase:
    def __init__(self):
        self.phrase = [
            "J'aime les pommes",
            "Je roule en voiture",
            "Je suis dans le bus"
        ]

    def lancer(self):
        phrase = random.choice(self.phrase)
        print(f"Essaye donc d'écrire cette phrase dans l'autre sens pour voir : {phrase}")
        phrase_saisie = input("> ")
        if phrase_saisie == phrase[::-1]:
            print("Tu as réussi mais il suffisait de lire de droite à gauche, pas de quoi s'extasier. :|")
            return True
        else:
            print("Raté alors qu'il te suffisait de lire de droite à gauche...")
            return False


class Combinaison:
    def __init__(self):
        self.saisi = None
        self.reponse = None
        self.touches = ['↑ Haut', '↓ Bas', '← Gauche', '→ Droite']
        self.longueur = 15

    def gener_combinaison(self):
        return random.choices(self.touches, k=self.longueur)

    def lancer(self):
        self.reponse = self.gener_combinaison()
        self.saisi = []
        print(f"Essaye de faire cette séquence avec tes flèches directionnelles : {self.reponse}")

        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        try:
            if key == keyboard.Key.up:
                self.saisi.append('↑ Haut')
            elif key == keyboard.Key.down:
                self.saisi.append('↓ Bas')
            elif key == keyboard.Key.left:
                self.saisi.append('← Gauche')
            elif key == keyboard.Key.right:
                self.saisi.append('→ Droite')

            if len(self.saisi) == len(self.reponse):
                self.check()
                return False

        except AttributeError:
            pass

    def check(self):
        if self.saisi == self.reponse:
            print("Tu as réussi mais après t'avais la réponse devant les yeux, aussi...")
        else:
            print("Wow, même avec la réponse devant les yeux tu t'es trompé ? La honte... XD")
        return False


class LogicPlateau:
    def __init__(self, nombre_cases):
        self.taille_case = None
        self.plateau = None
        self.cases = None
        self.__couleurs = {
            "VIDE": "white",
            "NEUTRE": "blue",
            "JEU": "orange",
            "EVENT": "purple",
            "DEPART": "green",
            "ARRIVE": "red",
            "JOUEUR": "yellow"
        }
        self.__wav = ["/assets/musiques/emotional.wav",
                      "/assets/musiques/rise.wav",
                      "/assets/musiques/serenity.wav",
                      "/assets/musiques/oued.wav"]
        self.size = 50
        self.nombre_cases = nombre_cases
        self.create_cases()
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

    def update_pos_in_case(self):
        """
        La méthode va mettre a jour la position de chaque case

        PRE : -L'attribut Cases doit être non vide et être une liste d'objet Case
              -L'attribut Plateau doit être une liste de liste d'objet Case
        POST : Met a jour la postition de chaque case dans l'attribut Cases
        """
        case_precedente = None
        case_actuelle = self.trouve_depart()
        self.cases[0].position = case_actuelle
        for i in range(1, len(self.cases)):
            voisins = [
                (case_actuelle[0] + 1, case_actuelle[1]),
                (case_actuelle[0] - 1, case_actuelle[1]),
                (case_actuelle[0], case_actuelle[1] + 1),
                (case_actuelle[0], case_actuelle[1] - 1)
            ]
            for v in voisins:
                if 0 <= v[0] < len(self.plateau) and 0 <= v[1] < len(self.plateau[0]):
                    if self.plateau[v[0]][v[1]].type != "VIDE" and v != case_precedente:
                        self.cases[i].position = v
                        case_precedente = case_actuelle
                        case_actuelle = v
                        break

    def create_cases(self):
        """
        On fait en sorte d'avoir un certain nbCase de différent avec un type_case choisis aléatoirement, on commence
        toujours avec une case
        départ et fini par une case arrivé

        PRE : nbCase : int >= 0
        POST : - Creer l'attribut cases qui contient une liste d'object Case
        """
        self.cases = [Case("DEPART")]
        event_probabilite = 0.025
        mini_jeu_probabilite = 0.05
        possibilites = ["NEUTRE", "JEU", "EVENT"]
        probabilites = [1 - mini_jeu_probabilite - event_probabilite, mini_jeu_probabilite, event_probabilite]

        for i in range(self.nombre_cases + 2):
            type_case = random.choices(possibilites, weights=probabilites, k=1)[0]
            self.cases.append(Case(type_case))

            if type_case == "JEU":
                probabilites[1] = mini_jeu_probabilite
                probabilites[2] += event_probabilite

            elif type_case == "EVENT":
                probabilites[1] += mini_jeu_probabilite
                probabilites[2] = event_probabilite
            else:
                probabilites[1] += mini_jeu_probabilite
                probabilites[2] += event_probabilite

            probabilites[0] = 1 - probabilites[1] - probabilites[2]

        self.cases.append(Case("ARRIVE"))

    def clear_matrice(self):
        """
        Cette méthode sert a enlever toute les lignes/colones inutile pour que la taille du rectangle affiché soit le
         plus petit possible

        PRE : plat doit être une liste de liste de Case
        POST : Enleve les lignes et colones qui ne contiennent uniquement des cases de type vide.
        """
        return
        for i in range(len(self.plateau) - 1, -1, -1):
            if all(cell.type == "VIDE" for cell in self.plateau[i]):
                self.plateau.pop(i)
        for i in range(len(self.plateau[0]) - 1, -1, -1):
            temp = [self.plateau[j][i] for j in range(len(self.plateau))]
            if all(cell.type == "VIDE" for cell in temp):
                for j in range(len(self.plateau)):
                    self.plateau[j].pop(i)

    def trouve_depart(self):
        for i in range(len(self.plateau)):
            for j in range(len(self.plateau[i])):
                if self.plateau[i][j].type == "DEPART":
                    return i, j

    def faire_plateau(self):
        """
        On essaye de faire placer toute les cases de self.cases l'une a la suite de l'autre de facon aléatoire, une
        case peut
        toucher une seul autre case et elle doivent rester dans un carré de taille self.size
        PRE : - self.size doit être un int >=0
              - self.cases doit être une liste d'objet Case non vide

        POST : Place dans self.plateau une liste de liste d'Objet case formant un chemin de forme aléatoire
        RAISE : Si aucun placement n'est possible car un nombre trop élévé de case à placé, un erreur est déclanché
        """
        tentative = 0
        while tentative < 100:
            position = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            plateau = [[Case("VIDE") for _ in range(self.size)] for _ in range(self.size)]
            positions_occupees = {position}
            for case in self.cases:
                plateau[position[0]][position[1]] = case

                position_suivante = [
                    (position[0] + 1, position[1]),
                    (position[0] - 1, position[1]),
                    (position[0], position[1] + 1),
                    (position[0], position[1] - 1)
                ]
                random.shuffle(position_suivante)
                trouve = False
                while not trouve and len(position_suivante):
                    position_en_test = position_suivante.pop()
                    if (
                            position_en_test not in positions_occupees and (
                            0 <= position_en_test[0] < len(plateau)) and (
                            0 <= position_en_test[1] < len(plateau[0]))
                    ):
                        voisins = [
                            (position_en_test[0] + 1, position_en_test[1]),
                            (position_en_test[0] - 1, position_en_test[1]),
                            (position_en_test[0], position_en_test[1] + 1),
                            (position_en_test[0], position_en_test[1] - 1)
                        ]
                        ok = True
                        for v in voisins:
                            if 0 <= v[0] < len(plateau) and 0 <= v[1] < len(plateau[0]):
                                if not (plateau[v[0]][v[1]] == case or plateau[v[0]][v[1]].type == "VIDE"):
                                    ok = False
                                    break
                        if ok:
                            position = position_en_test
                            positions_occupees.add(position)
                            trouve = True
                if not trouve:
                    tentative += 1
            self.plateau = plateau
            return

    def lancer_de(self):
        """
        Cette fonction simule un lancé de dé à 6 côté, ensuite elle met le plateau de jeu à jour en fontion de la case
         sur où atterit le joueur.
        Elle renvoie le résultat du lancé de dé dans  le variable 'num'.
        PRE:
            - joueur.pos doit être un int
        POST:
            - le joueur avance de 1 à 6 cases
            - en fonction du type de case sur où le joueur fini un jeu, mini-jeu, rien ou la fin du jeu
            - 60% de chance d'avoir un défi si le joueur tombe sur une case défi
        """
        valeur = random.randint(1, 6)
        self.joueur.position += (valeur if (self.joueur.position + valeur) < len(self.cases) else len(
            self.cases) - 1 - self.joueur.position)


class MiniJeuMusical:
    def __init__(self, chemin_fichier_wav):
        self.result_label_wav = None
        self.label_wav = None
        for i in range(len(chemin_fichier_wav)):
            chemin_fichier_wav[i] = "asset/musiques/" + chemin_fichier_wav[i]

        if not chemin_fichier_wav:
            raise ValueError("La liste des fichiers wav est vide.")
        # self.chemin_fichier_wav = chemin_fichier_wav
        self.chemin_fichier_wav = chemin_fichier_wav
        self.chemin_fichier = None
        self.result_wav = None
        self.fenetre_wav = None
        self.bouton_wav = None
        self.entry_wav = None
        self.reponse_correcte = None

    def reponse_random(self):
        """
        - écrit si la réponse est bonne ou pas dans la fenêtre tkinker
        - rend le boutton innacessible après l'avoir pressé
        - ferme la fenêtre après 2 sec suivant la pression du boutton
        PRE:
            - La méthode est appelée dans un contexte où `self.reponse_correcte` est défini comme un booléen.
        POST:
            - Le texte affiché dans `self.result_wav` reflète l'état de `self.reponse_correcte`.
            - Le bouton est désactivé.
            - La fenêtre est détruite après 2 secondes.
        """
        if self.reponse_correcte:
            self.result_wav.set("Réponse correcte!")
            print("Réponse correcte!")
        else:
            self.result_wav.set("Réponse incorrecte")
            print("Réponse incorrecte!")
        self.bouton_wav.config(state=tk.DISABLED)  # désactive le bouton après validation
        self.fenetre_wav.after(2000, self.fenetre_wav.destroy)  # ferme la fenêtre après 2 sec

    def lancer(self):
        """
        - lance le mini-jeu
        - vérifie si les fichiers .wav existes
        - joue un fichier .wav choisi au hasard dans la liste wav
        - crée une fenêtre pour donner la réponse la réussite de ce mini-jeu est défini par une fonction random
        PRE:
            - la bibliothèque playsound est installée
        POST:
            - raise : FileNotFoundError: pas trouvé les fichier .wav
            - Exception : erreur de lecture de fichier .wav
            - except : erreur lors de la création de la fenêtre de réponse
        """

        self.chemin_fichier = random.choice(self.chemin_fichier_wav)  # un fichier aléatoire
        print(self.chemin_fichier)
        print(self.chemin_fichier_wav)
        if not os.path.exists(self.chemin_fichier):
            raise FileNotFoundError(f"Fichier WAV introuvable : {self.chemin_fichier}")

        self.reponse_correcte = random.choice([True, False])
        # joue le fichier wav
        print("Quelle titre te vient en tête ?")
        try:
            print("Lecture du fichier : HAHA tu pensais avoir la réponse comme ça ??!!!")
            playsound(self.chemin_fichier)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier wav : {e}")
            print("Est-ce que la librairie playsound 1.2.2 est bine installé")
        try:
            self.fenetre_wav = tk.Tk()
            self.fenetre_wav.title("Mini-jeu de musique")

            # explication
            self.label_wav = tk.Label(self.fenetre_wav, text="Entrez votre réponse:")

            # champ de saisie
            self.entry_wav = tk.Entry(self.fenetre_wav)

            # variable affiche résultat
            self.result_wav = tk.StringVar(self.fenetre_wav)
            self.result_wav.set("")
            self.result_label_wav = tk.Label(self.fenetre_wav, textvariable=self.result_wav)

            # bouton pour valider
            self.bouton_wav = tk.Button(self.fenetre_wav, text="Valider", command=self.reponse_random)

            self.label_wav.pack()
            self.entry_wav.pack()
            self.result_label_wav.pack()
            self.bouton_wav.pack()

            self.fenetre_wav.mainloop()
        except:
            print("Erreur pour la création de la fenêtre de réponse")
