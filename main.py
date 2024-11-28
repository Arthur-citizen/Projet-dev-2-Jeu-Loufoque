import tkinter as tk
import random
from pynput import keyboard
from PIL import Image, ImageTk
import os
from playsound import playsound #playsound 1.2.2



#liste musique pour mini-jeu
wav = ["emotional.wav",
       "rise.wav",
       "serenity.wav",
       "oued.wav"]
class Case:

    def __init__(self, type):
        self.type = type  # Type de case : mini-jeu, départ, neutre, etc.
        self.position = None

    def __str__(self):  # Pour afficher en console la case avec print(Case)
        return f"{self.type}"


class Joueur:
    def __init__(self, depart):
        self.pos = depart

    def deplacer(self):
        pass


class Phrase:
    def __init__(self):
        self.phrase = ["J'aime les pommes", "Je roule en voiture", "Je suis dans le bus"]

    def lancer(self):
        phrase = random.choice(self.phrase)
        print("Essaye donc d'écrire cette phrase dans l'autre sens pour voir : ", phrase)
        phraseSaisi = input("> ")
        if phraseSaisi == phrase[::-1]:
            print("Tu as réussi mais il suffisait de lire de droite à gauche, pas de quoi s'extasier. :|")
            return True
        else:
            print(f"Raté alors qu'il te suffisait de lire de droite à gauche...")
            return False


class Combi:
    def __init__(self):
        self.touches = ['↑ Haut', '↓ Bas', '← Gauche', '→ Droite']
        self.longCombi = 15

    def generCombi(self):
        return random.choices(self.touches, k=self.longCombi)

    def lancer(self):
        self.res = self.generCombi()
        self.saisi = []
        print("Essaye de faire cette séquence avec tes flèches directionnelles, pour voir :  ", self.res)
        with keyboard.Listener(on_press=self.onPress) as listener:
            listener.join()

    def onPress(self, key):
        try:
            if key == keyboard.Key.up:
                self.saisi.append('↑ Haut')
            elif key == keyboard.Key.down:
                self.saisi.append('↓ Bas')
            elif key == keyboard.Key.left:
                self.saisi.append('← Gauche')
            elif key == keyboard.Key.right:
                self.saisi.append('→ Droite')

            if len(self.saisi) == len(self.res):
                self.check()
                return False

        except AttributeError:
            pass

    def check(self):
        if self.saisi == self.res:
            print("Tu as réussi mais après t'avais la réponse devant les yeux, aussi...")
        else:
            print("Wow, même avec la réponse devant les yeux tu t'es trompé ? La honte... XD")
        return False

class Mini_jeu_musical:
    def __init__(self, chemin_fichier_wav):
        if not chemin_fichier_wav:
            raise ValueError("La liste des fichiers wav est vide.")
        #self.chemin_fichier_wav = chemin_fichier_wav
        self.chemin_fichier_wav = chemin_fichier_wav
        self.chemin_fichier = None
        self.result_wav = None
        self.fenetre_wav = None
        self.bouton_wav = None
        self.entry_wav = None
        self.reponse_correcte = None
        
    def reponse_random(self):
        '''
        - écrit si la réponse est bonne ou pas dans la fenêtre tkinker
        - rend le boutton innacessible après l'avoir pressé
        - ferme la fenêtre après 2 sec suivant la pression du boutton
        PRE: 
            - La méthode est appelée dans un contexte où `self.reponse_correcte` est défini comme un booléen.
        POST: 
            - Le texte affiché dans `self.result_wav` reflète l'état de `self.reponse_correcte`.
            - Le bouton est désactivé.
            - La fenêtre est détruite après 2 secondes.
        '''
        if self.reponse_correcte:
            self.result_wav.set("Réponse correcte!")
            print("Réponse correcte!")
        else:
            self.result_wav.set("Réponse incorrecte")
            print("Réponse incorrecte!")
        self.bouton_wav.config(state=tk.DISABLED) #désactive le bouton après validation
        self.fenetre_wav.after(2000, self.fenetre_wav.destroy) #ferme la fenêtre après 2 sec
        
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

        self.chemin_fichier = random.choice(self.chemin_fichier_wav) #un fichier aléatoire
        print(self.chemin_fichier)
        print(self.chemin_fichier_wav)
        if not os.path.exists(self.chemin_fichier):
            raise FileNotFoundError(f"Fichier WAV introuvable : {self.chemin_fichier}")
        
        self.reponse_correcte = random.choice([True, False])
        #joue le fichier wav
        print("Quelle titre te vient en tête ?")
        try:
            print(f"Lecture du fichier : HAHA tu pensais avoir la réponse comme ça ??!!!")
            playsound(self.chemin_fichier)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier wav : {e}")
            print("Est-ce que la librairie playsound 1.2.2 est bine installé")
        try:
            self.fenetre_wav = tk.Tk()            
            self.fenetre_wav.title("Mini-jeu de musique")

            #explication
            self.label_wav = tk.Label(self.fenetre_wav, text="Entrez votre réponse:")
            
            #champ de saisie
            self.entry_wav = tk.Entry(self.fenetre_wav)
            
            #variable affiche résultat
            self.result_wav = tk.StringVar(self.fenetre_wav)
            self.result_wav.set("")
            self.result_label_wav = tk.Label(self.fenetre_wav, textvariable=self.result_wav)
            
            #bouton pour valider
            self.bouton_wav = tk.Button(self.fenetre_wav, text="Valider", command=self.reponse_random)
            
            self.label_wav.pack()
            self.entry_wav.pack()
            self.result_label_wav.pack()
            self.bouton_wav.pack()

            self.fenetre_wav.mainloop()
        except:
            print("Erreur pour la création de la fenêtre de réponse")

class Menu:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.geometry("540x540")
        self.fenetre.title("Jeu de plateau Loufoque")

        # Charger le GIF comme fond
        self.gif = Image.open("image/bg.gif")
        self.gif_frames = []
        #stock les images du gif dans une liste "self.gif_frames = []"
        for i in range(self.gif.n_frames):
            self.gif.seek(i)
            frame = ImageTk.PhotoImage(self.gif.copy())
            self.gif_frames.append(frame)
        #set la première image du gif
        self.background_label = tk.Label(self.fenetre, image=self.gif_frames[0])
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        #anime du GIF
        self.current_frame = 0
        self.animate_gif()

        #crée les titres
        self.titre = tk.Label(
            self.fenetre, 
            text="Préparez vous pour un jeu renversant", 
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
        #positionner les titres
        self.titre.place(relx=0.5, rely=0.13, anchor=tk.CENTER) # 13% en hauteur depuis le heut de la fenêtre 
        self.titre1.place(relx=0.5, rely=0.18, anchor=tk.CENTER) # 18% du haut de la fenêtre

        #bouton pour lancer le jeu
        self.porte = tk.PhotoImage(file="image/porte_menu.png") #charge la porte
        self.bouton_start = tk.Button(
            self.fenetre, 
            image=self.porte, 
            command=self.start_game, 
            bg="black", 
            highlightthickness=0, 
            border=0, 
            activebackground="black"
        )
        #place le bouton
        self.bouton_start.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    #fais une rotation dans la liste "gif_frames = []" avec 25ms d'interval entre chaque image
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
        #fermer le menu
        self.fenetre.destroy()

        #Lance le plateau
        plateau = Plateau(60)
        plateau.afficher()
    #lance la boucle principale
    def afficher(self):
        self.fenetre.mainloop()


class Plateau:
    def __init__(self, nbCases):
        self.__couleurs = {   # Sert pour la couleur des cases
                            "VIDE": "white",
                            "NEUTRE": "blue",
                            "JEU": "orange",
                            "EVENT": "purple",
                            "DEPART": "green",
                            "ARRIVE": "red",
                            "JOUEUR": "yellow"
                        }
        self.size = 50    # dimension du carré dans lequel on va essayer de placer les cases
        self.nbCases = nbCases
        self.create_cases()   # On créé un certain nombre (nbcases) de Case
        self.largeurFenetre,self.hauteurFenetre = 800,600
        self.fairePlateau()
        self.clear_matrice()
        self.joueur = Joueur(0)
        self.update_pos_in_case()
        pays=[]
        for letter in range(ord('a'), ord('z') + 1):
            pays.append(f"Essaye de trouver un pays dont la première lettre est '{chr(letter)}'. :)")
        self.defi = ["Fais 5 pompes, histoire de te décoller le derrière de ta chaise. :-)", "Voyons comme tu t'en sors pour réciter l'alphabet à l'envers sans faute ! Allez, on t'écoute ! ;D",pays, "Allez, compte jusque 100 le plus vite possible !" , "Allez, bouge un peu et tiens en équilibre sur une jambe pendant dix secondes. Je suis sympa, je te laisse choisir laquelle. ';-)" ]



        self.jeu = [Phrase(),Combi(),Mini_jeu_musical(wav)]
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
        previous=None
        act = self.trouveDepart()
        self.cases[0].position = act
        for i in range(1,len(self.cases)):

            voisins = [(act[0] + 1, act[1]), (act[0] - 1, act[1]), (act[0], act[1] + 1), (act[0], act[1] - 1)]
            for v in voisins:
                if 0 <= v[0] < len(self.plateau) and 0 <= v[1] < len(self.plateau[0]) and self.plateau[v[0]][v[1]].type != "VIDE" and v != previous:
                    self.cases[i].position = v
                    previous=act
                    act=v
                    break


    def create_cases(self):
        """
        On fait en sorte d'avoir un certain nbCase de différent avec un type choisis aléatoirement, on commence toujours avec une case
        départ et fini par une case arrivé

        PRE : nbCase : int >= 0
        POST : - Creer l'attribut cases qui contient une liste d'object Case
        """
        self.cases = [Case("DEPART")]
        eventProb = 0.025
        miniProb = 0.05
        possiblilite = ["NEUTRE", "JEU", "EVENT"]
        probabilites = [1 - miniProb - eventProb, miniProb, eventProb]  #probabilité associé au différente possibilié, il faudrait en faire un dictionnaire

        for i in range(self.nbCases+2):
            type = random.choices(possiblilite, weights=probabilites, k=1)[0]  # choisis un type de cases alléatoirement en fonction des probabilité
            self.cases.append(Case(type))
            if type == "JEU":
                probabilites[0], probabilites[1], probabilites[2] = 1 - miniProb - (                # Ca caluc les prob, si un type est choisis ça met ses prob
                            probabilites[2] + eventProb), miniProb, probabilites[2] + eventProb            #par default sinon àa rajoute ses prob par defaut a sa prob actuel
            elif type == "EVENT":
                probabilites[0], probabilites[1], probabilites[2] = 1 - eventProb - (probabilites[1] + miniProb), \
                                                                    probabilites[1] + miniProb, eventProb
            else:
                probabilites[0] -= (miniProb + eventProb)
                probabilites[1] += miniProb
                probabilites[2] += eventProb


        self.cases.append(Case("ARRIVE"))

    def clear_matrice(self):
        """
        Cette méthode sert a enlever toute les lignes/colones inutile pour que la taille du rectangle affiché soit le plus petit possible

        PRE : plat doit être une liste de liste de Case
        POST : Enleve les lignes et colones qui ne contiennent uniquement des cases de type vide.
        """

        for i in range(len(self.plateau) - 1, -1, -1):    # clear lignes de case vide
            if all(cell.type == "VIDE" for cell in self.plateau[i]):
                self.plateau.pop(i)
        for i in range(len(self.plateau[0]) - 1, -1, -1):         # clear colone de case vide
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
                    return (i,j)
    def fairePlateau(self):
        """
        On essaye de faire placer toute les cases de self.cases l'une a la suite de l'autre de facon aléatoire, une case peut
        toucher une seul autre case et elle doivent rester dans un carré de taille self.size
        PRE : - self.size doit être un int >=0
              - self.cases doit être une liste d'objet Case non vide

        POST : Place dans self.plateau une liste de liste d'Objet case formant un chemin de forme aléatoire
        RAISE : Si aucun placement n'est possible car un nombre trop élévé de case à placé, un erreur est déclanché
        """
        temp = 0 # mettre un .time() pour avoir 220 sec de charge ou moins, on essaye {tentative} fois avec une taille de plateau et apres on augmente la taille

        while temp < 100000:
            tentative = 0
            while tentative < 100:
                try:
                    pos = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))   #position de la case depart
                    plat = [[Case("VIDE") for i in range(self.size)] for j in range(self.size)]      #on remplit le plateau de cases vide
                    ban = {pos}    #stok les positions utilisé
                    for cas in self.cases:
                        plat[pos[0]][pos[1]] = cas

                        nextPos = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)] # postions des cases dans les 4 directions
                        random.shuffle(nextPos) #change ordre
                        find = False   # nouvelle position trouvé ?
                        while not find and len(nextPos):
                            tryy = nextPos.pop() #on prend une pose pour essayer

                            if tryy not in ban and len(plat) > tryy[0] >= 0 and len(plat) > tryy[1] >= 0 :   # on regarde si la case est déja utilisé ou si elle n'est pas dans les limites
                                voisins = [(tryy[0] + 1, tryy[1]), (tryy[0] - 1, tryy[1]), (tryy[0], tryy[1] + 1),
                                           (tryy[0], tryy[1] - 1)]  # voisin de la case a essayer
                                ok = True   # est ce que tout les voisins sont vides ? (sauf celle de la case précédente car il doit y avoir un poitn d'accrochen entre 2 cases
                                for v in voisins:
                                    if 0 <= v[0] < len(plat) and 0 <= v[1] < len(plat[0]):
                                        if not (plat[v[0]][v[1]] == cas or plat[v[0]][v[1]].type == "VIDE"): # si un des voisins n'est pas vide
                                            ok = False
                                            break

                                if ok:
                                    pos = tryy
                                    ban.add(pos)
                                    find = True
                        if not find:
                            raise PlacementError("Pas de place")
                    self.plateau = plat
                    return
                except PlacementError:
                    tentative += 1
            temp +=1
            self.size +=5
    def lancerDe(self):
        """
        Cette fonction simule un lancé de dé à 6 côté, ensuite elle met le plateau de jeu à jour en fontion de la case sur où atterit le joueur. 
        Elle renvoie le résultat du lancé de dé dans  le variable 'num'.
        :return: 
        - num : int : entre 1 et 6
        """
        #try:
        if(1):
            num= random.randint(1,6)
            self.joueur.pos += (num if (self.joueur.pos + num) < len(self.cases) else len(self.cases)-1-self.joueur.pos)
            self.afficherPlateau()

            if self.cases[self.joueur.pos].type == "JEU" :
                self.root.update_idletasks()

                random.choice(self.jeu).lancer()

            elif self.cases[self.joueur.pos].type == "EVENT":
                self.fairePlateau()
                self.clear_matrice()
                self.update_pos_in_case()
                self.tailleCase=self.calculateCaseSize()
                self.afficherPlateau()
            elif self.cases[self.joueur.pos].type == "ARRIVE":
                print("win gg")
                self.root.quit()

            else:
                if random.randint(1,10) >4:
                    t=(random.choice(self.defi))
                    if type(t)== list:
                        t=random.choice(t)
                    print(t)
            return num
        #except:
            #print("Erreur fonction lancerDe")

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
                x0, y0 = j * self.tailleCase, i * self.tailleCase  # coins haut gauche
                x1, y1 = x0 + self.tailleCase, y0 + self.tailleCase # coins bat droite
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=couleur, outline=("black" if couleur != "white" else ""))

        joueurY = self.cases[self.joueur.pos].position[0] * self.tailleCase + self.tailleCase // 2
        joueurX = self.cases[self.joueur.pos].position[1] * self.tailleCase + self.tailleCase // 2
        self.canvas.create_oval(joueurX - self.tailleCase // 4, joueurY - self.tailleCase // 4, joueurX + self.tailleCase // 4, joueurY + self.tailleCase // 4, fill=self.__couleurs["JOUEUR"])

    def calculateCaseSize(self):

        return min(self.hauteurFenetre // len(self.plateau),self.largeurFenetre // len(self.plateau[0]))


    def afficher(self):
        """
        Cette fonction initialise l'affichage du plateau de jeu
        - crée un canvas pour le plateau de jeu
        - ajoute le bouton de lancé de dé
        - affiche le tableau initial
        - démarre la boucle principal avec mainloop()

        :return: None
        """
        self.root = tk.Tk()
        self.root.title("Plateau Interface")


        self.tailleCase = self.calculateCaseSize()


        self.canvas = tk.Canvas(self.root, width=self.largeurFenetre, height=self.hauteurFenetre)
        self.canvas.pack()

        boutonDe = tk.Button(self.root, text="Lancer le dé", command=self.lancerDe)
        boutonDe.pack()
        self.afficherPlateau()

        self.root.mainloop()

    def __str__(self):
        """
        affichage du plateau en consoel si besoins print(Plateau)
        :return:
        """
        res='['
        for ligne in self.plateau:
            temp='['
            for case in ligne:
                temp+= case.type + ","
            temp +=']\n'
            res += temp + ','

        return res+']'
class PlacementError(Exception):
    pass

# Point d'entrée du programme
if __name__ == "__main__":
    menu = Menu()
    menu.afficher()
