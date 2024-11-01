import tkinter as tk
import random
couleurs = {
    "VIDE": "white",
    "NEUTRE": "blue",
    "JEU": "orange",
    "EVENT": "purple",
    "DEPART": "green",
    "ARRIVE": "red",
    "JOEUR": "yellow"

}


class Case:
    def __init__(self, type):
        self.type = type  # Couleur par défaut de la case

    def __str__(self):
        return f"{self.type}"


class Joueur:
    def __init__(self, depart):
        self.pos = depart

    def deplacer(self):
        pass


class Plateau:
    def __init__(self, nbCases):
        self.size = 50
        self.cases = self.createCase(nbCases)
        self.plat = self.fairePlateau()
        self.plat = self.clearMat(self.plat)

    def createCase(self, nbCase):
        cases = [Case("DEPART")]
        eventProb = 0.05
        miniProb = 0.1
        possiblilite = ["NEUTRE", "JEU", "EVENT"]
        probabilites = [1 - miniProb - eventProb, miniProb, eventProb]

        for i in range(nbCase):
            type = random.choices(possiblilite, weights=probabilites, k=1)[0]
            cases.append(Case(type))
            if type == "JEU":
                probabilites[0], probabilites[1], probabilites[2] = 1 - miniProb - (
                            probabilites[2] + eventProb), miniProb, probabilites[2] + eventProb
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
        # clear lignes de 0
        for i in range(len(plat) - 1, -1, -1):
            if all(cell.type == "VIDE" for cell in plat[i]):
                plat.pop(i)
        # clear colone de 0
        for i in range(len(plat[0]) - 1, -1, -1):
            temp = []
            for j in plat:
                temp.append(j[i])
            if all(cell.type == "VIDE" for cell in temp):
                for j in plat:
                    j.pop(i)
        return plat

    def fairePlateau(self):

        tentative = 100
        while tentative > 0:
            try:
                pos = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
                plat = [[Case("VIDE") for i in range(self.size)] for j in range(self.size)]
                ban = {pos}

                for cas in self.cases:
                    plat[pos[0]][pos[1]] = cas

                    nextPos = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
                    random.shuffle(nextPos)
                    find = False
                    while not find:
                        if len(nextPos) == 0:
                            break
                        tryy = nextPos.pop()

                        if len(plat) > tryy[0] >= 0 and len(plat) > tryy[1] >= 0 and tryy not in ban:
                            voisins = [(tryy[0] + 1, tryy[1]), (tryy[0] - 1, tryy[1]), (tryy[0], tryy[1] + 1),
                                       (tryy[0], tryy[1] - 1)]
                            ok = True
                            for v in voisins:
                                if not (plat[v[0]][v[1]] == cas or plat[v[0]][v[1]].type == "VIDE"):
                                    ok = False
                                    break

                            if ok:
                                pos = tryy
                                ban.add(pos)
                                find = True
                    if not find:
                        raise Exception("Pas de place")
                return (plat)
            except:
                tentative -= 1

    def afficher(self):
        root = tk.Tk()
        root.title("Plateau Interface")
        tailleCase = 30
        canvas_width = len(self.plat[0]) * tailleCase
        canvas_height = len(self.plat) * tailleCase
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        canvas.pack()

        for i in range(len(self.plat)):
            for j in range(len(self.plat[i])):
                couleur = couleurs[self.plat[i][j].type] if self.plat[i][j] else couleurs[self.plat[i][j]]
                x0, y0 = j * tailleCase, i * tailleCase
                x1, y1 = x0 + tailleCase, y0 + tailleCase
                canvas.create_rectangle(x0, y0, x1, y1, fill=couleur, outline=("black" if couleur != "white" else ""))

        root.mainloop()

    def __str__(self):
        if not self.plat:
            return 'prob'
        s = ""
        for row in self.plat:
            if s:
                s += " \n"
            for elem in row:
                if elem > 9:
                    s += str(elem) + " "
                else:
                    s += str(elem) + "  "
        return s


t = Plateau(30)
t.afficher()
