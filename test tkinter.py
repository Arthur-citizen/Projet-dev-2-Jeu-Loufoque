import tkinter as tk
import random
couleurs = {   #sert pour la couleur des cases
    "VIDE": "white",
    "NEUTRE": "blue",
    "JEU": "orange",
    "EVENT": "purple",
    "DEPART": "green",
    "ARRIVE": "red",
    "JOUEUR": "yellow"

}

class Case:
    def __init__(self, type):
        self.type = type  # Met le type de cases mini jeu,depart , neutre, ....
        self.position= None

    def __str__(self):     # pour afficher en console la case avec print(Case)
        return f"{self.type}"


class Joueur:
    def __init__(self, depart):
        self.pos = depart

    def deplacer(self):
        pass


class Plateau:
    def __init__(self, nbCases):
        self.size = 50    # dimension du carré dans lequel on va essayer de placer les cases
        self.cases = self.createCases(nbCases)   # On créé un certain nombre (nbcases) de Case
        self.plat = self.fairePlateau()
        self.plat = self.clearMat(self.plat)
        self.joueur = Joueur(0)
        self.putPosInCase()
        print(self.joueur.pos)
        print(self.cases[0].position)
        print(self.cases[len(self.cases)-1].position)
    def putPosInCase(self):
        prec=None
        act = self.trouveDepart()
        self.cases[0].position = act
        for i in range(1,len(self.cases)):

            voisins = [(act[0] + 1, act[1]), (act[0] - 1, act[1]), (act[0], act[1] + 1), (act[0], act[1] - 1)]
            for v in voisins:
                if 0 <= v[0] < len(self.plat) and 0 <= v[1] < len(self.plat[0]) and self.plat[v[0]][v[1]].type != "VIDE" and v != prec:
                    self.cases[i].position = v
                    prec=act
                    act=v
                    break


    def createCases(self, nbCase):
        """
        On fait en sorte d'avoir un certain nbCase de différent type choisis aléatoirement on commence toujours avec une case
        départ et fini par une case arrivé
        :param nbCase:
        :return: List(Case)
        """
        cases = [Case("DEPART")]
        eventProb = 0.025
        miniProb = 0.05
        possiblilite = ["NEUTRE", "JEU", "EVENT"]
        probabilites = [1 - miniProb - eventProb, miniProb, eventProb]  #probabilité associé au différente possibilié, il faudrait en faire un dictionnaire

        for i in range(nbCase):
            type = random.choices(possiblilite, weights=probabilites, k=1)[0]  # choisis un type de cases alléatoirement en fonction des probabilité
            cases.append(Case(type))
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



        cases.append(Case("ARRIVE"))
        return cases

    def clearMat(self, plat):
        """
        Comme le plateau est généré aléatoirement il se peu, par exemple, que le plateau soit coller a gauche de la fenetre
        cette fonction sert a enlever toute les lignes/colones inutile pour que la taille du rectangle/carré afficher soit le plus petit necessaire

        :param plat:
        :return:
        """

        for i in range(len(plat) - 1, -1, -1):    # clear lignes de case vide
            if all(cell.type == "VIDE" for cell in plat[i]):
                plat.pop(i)
        for i in range(len(plat[0]) - 1, -1, -1):         # clear colone de case vide
            temp = []
            for j in plat:
                temp.append(j[i])
            if all(cell.type == "VIDE" for cell in temp):
                for j in plat:
                    j.pop(i)
        return plat


    def trouveDepart(self):
        for i in range(len(self.plat)):
            for j in range(len(self.plat[i])):
                if self.plat[i][j].type == "DEPART":
                    return (i,j)
    def fairePlateau(self):
        """
        On essaye de faire placer toute les cases de self.cases l'une a la suite de l'autre de facon aléatoire, une case peut
        toucher une seul autre case et elle doivent rester dans un carré de taille self.size
        :return:
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
                                    if not (plat[v[0]][v[1]] == cas or plat[v[0]][v[1]].type == "VIDE"): # si un des voisins n'est pas vide
                                        ok = False
                                        break

                                if ok:
                                    pos = tryy
                                    ban.add(pos)
                                    find = True
                        if not find:
                            raise Exception("Pas de place")
                    print(self.size,tentative)

                    return (plat)
                except:
                    tentative += 1
            temp +=1
            self.size +=5
    def lancerDe(self):
        num= random.randint(1,6)
        self.joueur.pos += (num if (self.joueur.pos + num) < len(self.cases) else len(self.cases)-self.joueur.pos)
        self.afficherPlateau()
        return num

    def afficherPlateau(self):
        self.canvas.delete('all')
        for i in range(len(self.plat)):
            for j in range(len(self.plat[i])):
                couleur = couleurs[self.plat[i][j].type]
                x0, y0 = j * self.tailleCase, i * self.tailleCase  # coins haut gauche
                x1, y1 = x0 + self.tailleCase, y0 + self.tailleCase # coins bat droite
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=couleur, outline=("black" if couleur != "white" else ""))

        joueurY = self.cases[self.joueur.pos].position[0] * self.tailleCase + self.tailleCase // 2
        joueurX = self.cases[self.joueur.pos].position[1] * self.tailleCase + self.tailleCase // 2
        self.canvas.create_oval(joueurX - self.tailleCase // 4, joueurY - self.tailleCase // 4, joueurX + self.tailleCase // 4, joueurY + self.tailleCase // 4, fill=couleurs["JOUEUR"])
    def afficher(self):
        self.root = tk.Tk()
        self.root.title("Plateau Interface")
        hauteurFenetre = 600
        largeurFenetre = 800

        self.tailleCase = min(hauteurFenetre // len(self.plat),largeurFenetre // len(self.plat[0])) #pour avoir des cases carres

        self.canvas = tk.Canvas(self.root, width=largeurFenetre, height=hauteurFenetre)
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
        for ligne in self.plat:
            temp='['
            for case in ligne:
                temp+= case.type + ","
            temp +=']\n'
            res += temp + ','

        return res+']'

t = Plateau(60)
t.afficher()