# L'importation de l’ensemble des éléments du paquet tkinter :
from tkinter import *
# Création d'une fenêtre avec la classe Tk :
fenetre = Tk()
porte = PhotoImage(file="image\porte_menu.png")
# Ajout d'un titre à la fenêtre principale :
fenetre.title("Jeu de plateau Loufoque")
titre = Label(fenetre, text = "Préparez vous pour un jeu renversant", background="#87CEEB", height=5, font=("Arial", 15), fg="green")

# La fonction à adapter pour lancer le jeu
def play():
    bouton1['text']='ABCDEFGHIJKLM'
# Le bouton
bouton1 = Button(fenetre, image=porte, bg="#87CEEB",highlightthickness= 0, border=0, activebackground="#87CEEB")
titre.pack()
bouton1.pack()
# Personnaliser la couleur de l'arrière-plan de la fenêtre principale :
fenetre.config(bg="#87CEEB") 
# Définir les dimensions par défaut la fenêtre principale :
fenetre.geometry("640x480")
# Affichage de la fenêtre créée :
fenetre.mainloop()
