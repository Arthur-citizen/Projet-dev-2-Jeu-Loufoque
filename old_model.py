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
