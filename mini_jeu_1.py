import random
from playsound import playsound
import tkinter as tk
import os

mp3 = ["emotional.wav",
       "rise.wav",
       "serenity.wav",
       "oued.wav"]
choix = random.choice(mp3)
print(choix)

playsound(choix)



def lancer_mini_jeu_mp3():
    """
    #Joue un fichier MP3 et demande une réponse via une interface tkinter.
    """
    # Construction du chemin complet vers le fichier MP3
    chemin_base = os.path.dirname(__file__)
    chemin_fichier = os.path.join(chemin_base, random.choice(mp3))
    
    # Vérification de l'existence du fichier avant de le jouer
    if not os.path.exists(chemin_fichier):
        print(f"Erreur: Le fichier {chemin_fichier} n'existe pas.")
        return
    
    print(f"Lecture du fichier: {chemin_fichier}")
    try:
        playsound(chemin_fichier)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        return

    # Choisir une réponse correcte aléatoire
    reponse_correcte = random.choice([True, False])
    
    # Création d'une fenêtre tkinter pour demander la réponse
    def verifier_reponse(reponse_correcte):
        reponse = entry.get()
        if reponse_correcte:
            result_var.set("Réponse correcte!")
            rep = True
        else:
            result_var.set("Réponse incorrecte.")
            rep = False
        bouton.config(state=tk.DISABLED)  # Désactiver le bouton une fois la réponse donnée

    fenetre = tk.Tk()
    fenetre.title("Mini-jeu de musique")

    # Explication
    label = tk.Label(fenetre, text="Entrez votre réponse:")
    
    # Champ de saisie
    entry = tk.Entry(fenetre)
    
    # Variable pour afficher le résultat
    result_var = tk.StringVar(fenetre)
    result_var.set("")  # Initialisation de la variable
    result_label = tk.Label(fenetre, textvariable=result_var)
    
    # Bouton pour valider la réponse
    bouton = tk.Button(fenetre, text="Valider", command=lambda: verifier_reponse(reponse_correcte))
    
    # Positionner les éléments dans la fenêtre
    label.pack()
    entry.pack()
    result_label.pack()
    bouton.pack()

    fenetre.mainloop()

# Lancer le mini-jeu
lancer_mini_jeu_mp3()