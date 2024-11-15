import random
from playsound import playsound
import tkinter as tk

def lancer_mini_jeu_mp3(chemin_fichier_mp3, reponse_correcte):
    """
    joue un fichier MP3 et demande une réponse via une interface tkinter.
    
    :param
    - chemin_fichier_mp3 : str : chemin du fichier MP3 à jouer.
    - reponse_correcte : str : réponse attendue pour réussir le mini-jeu.
    
    return:
    - bool : True si la réponse est correcte, False sinon.
    """
    # Utilisation de playsound pour jouer le fichier MP3
    playsound(chemin_fichier_mp3)
    
    # Création d'une fenêtre tkinter pour demander la réponse
    def verifier_reponse():
        reponse = entry.get()
        if random.choice([True, False]):
            result_var.set("Réponse correcte!")
            rep = True
        else:
            result_var.set("Réponse incorrecte.")
            rep = False
        bouton.config(state=tk.DISABLED)  # Désactiver le bouton une fois la réponse donnée

    # Fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("Mini-jeu de musique")

    # Label avec une explication
    label = tk.Label(fenetre, text="Entrez votre réponse:")
    label.pack()

    # Zone de saisie pour la réponse
    entry = tk.Entry(fenetre)
    entry.pack()

    # Variable pour afficher le résultat
    result_var = tk.StringVar(fenetre)
    result_var.set("")  # Initialisation de la variable
    result_label = tk.Label(fenetre, textvariable=result_var)
    result_label.pack()

    # Bouton pour valider la réponse
    bouton = tk.Button(fenetre, text="Valider", command=verifier_reponse)
    bouton.pack()

    # Lancement de la fenêtre tkinter
    fenetre.mainloop()

    # Retourner si la réponse était correcte ou non
    return result_var.get() == "Réponse correcte!"

def random_mini_jeu_mp3(chemin_fichier_mp3):
    """
    Lancer le mini-jeu de manière aléatoire et déterminer si le mini-jeu est réussi.
    
    return:
    - bool : True si le mini-jeu est réussi, False sinon.
    """
    # Définir le chemin du fichier MP3 et la réponse correcte
    reponse_correcte = random.choice([True, False])
    
    # Lancer le mini-jeu et vérifier si la réponse est correcte
    return lancer_mini_jeu_mp3(chemin_fichier_mp3, reponse_correcte)
