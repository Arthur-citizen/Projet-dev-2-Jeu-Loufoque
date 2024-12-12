from tkinter import *  # Importe toutes les fonctions et classes du module tkinter pour créer des interfaces graphiques
from PIL import Image, ImageTk  # Importe les classes Image et ImageTk du module PIL (Python Imaging Library) pour gérer les images

# Fonction pour animer le GIF
def update_gif(frame_index):
    global gif_frames  # Déclare que gif_frames est une variable globale
    frame = gif_frames[frame_index]  # Sélectionne le cadre du GIF selon l'index passé en paramètre
    background_label.configure(image=frame)  # Met à jour l'image affichée sur le label pour le cadre actuel
    frame_index = (frame_index + 1) % len(gif_frames)  # Passe au cadre suivant, et boucle au début si nécessaire
    fenetre.after(100, update_gif, frame_index)  # Relance la fonction après 100 ms (ajuster la vitesse de l'animation)

# Création de la fenêtre principale
fenetre = Tk()  # Crée une instance de la fenêtre principale de l'interface graphique

# Chargement du GIF animé avec Pillow
gif = Image.open("image/bg.gif")  # Remplacer par le chemin d'accès à votre GIF animé
gif_frames = []  # Liste vide pour stocker les cadres du GIF

# Récupérer tous les cadres du GIF
for i in range(gif.n_frames):  # Boucle pour parcourir tous les cadres du GIF
    gif.seek(i)  # Se déplace vers le i-ème cadre
    frame = ImageTk.PhotoImage(gif.copy())  # Crée un objet PhotoImage à partir du cadre actuel
    gif_frames.append(frame)  # Ajoute le cadre à la liste gif_frames

# Création d'un Label pour afficher le GIF en arrière-plan
background_label = Label(fenetre, image=gif_frames[0])  # Le premier cadre est affiché au départ
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place le label pour qu'il remplisse toute la fenêtre

# Ajout d'autres widgets (composants d'interface)
porte = PhotoImage(file="image/porte_menu.png")  # Charge une image pour un bouton
titre = Label(fenetre, text="Préparez vous pour un jeu renversant", background="black", font=("Arial", 15), fg="green")  # Titre principal
titre1 = Label(fenetre, text="Ouvrez la porte", width=14, background="black", font=("Arial", 15), fg="green")  # Sous-titre

# Fonction à exécuter lors du clic sur le bouton
def play():
    bouton['text'] = 'ABCDEFGHIJKLM'  # Change le texte du bouton

# Création d'un bouton avec l'image "porte_menu.png"
bouton = Button(fenetre, image=porte, bg="black", highlightthickness=0, border=0, activebackground="black")
titre.pack()  # Ajoute le titre à la fenêtre
titre1.pack()  # Ajoute le sous-titre à la fenêtre
bouton.pack()  # Ajoute le bouton à la fenêtre

# Définition des propriétés de la fenêtre principale
fenetre.title("Jeu de plateau Loufoque")  # Titre de la fenêtre
fenetre.geometry("540x540")  # Dimensions de la fenêtre (largeur x hauteur)

# Démarre l'animation du GIF en appelant la fonction update_gif avec l'index 0 (premier cadre)
update_gif(0)

# Démarre la boucle principale de l'interface graphique (attend les interactions de l'utilisateur)
fenetre.mainloop()
