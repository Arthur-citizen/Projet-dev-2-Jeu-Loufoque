import unittest
from unittest.mock import MagicMock, ANY
import random
from main import Plateau, Case, Joueur


class TestGameMethods(unittest.TestCase):

    def setUp(self):
        """Initialisation des objets nécessaires avant chaque test"""
        self.nb_cases = 5
        self.plateau = Plateau(self.nb_cases)
        self.plateau.canvas = MagicMock()  # Mock du canvas pour éviter d'ouvrir une vraie fenêtre

    def test_update_pos_in_case_normal(self):
        """Cas normal : Les positions des cases sont mises à jour correctement."""
        self.plateau.cases = [Case("NEUTRE") for _ in range(5)]
        self.plateau.plateau = [[Case("VIDE") for _ in range(10)] for _ in range(10)]
        self.plateau.plateau[0][0] = Case("DEPART")
        self.plateau.plateau[0][1] = Case("NEUTRE")
        self.plateau.plateau[0][2] = Case("ARRIVE")

        self.plateau.update_pos_in_case()
        positions = [case.position for case in self.plateau.cases]
        self.assertEqual(positions, [(0, 0), (0, 1), (0, 2)], "Les positions ne correspondent pas.")

    def test_update_pos_in_case_error(self):
        """Cas d'erreur : Plateau vide."""
        self.plateau.cases = [Case("NEUTRE")]
        self.plateau.plateau = []

        with self.assertRaises(Exception, msg="Une erreur aurait dû être levée pour un plateau vide."):
            self.plateau.update_pos_in_case()

    def test_create_cases_normal(self):
        """Cas normal : Création de 5 cases + DEPART et ARRIVE."""
        self.plateau.nombre_cases = 5
        self.plateau.create_cases()
        self.assertEqual(len(self.plateau.cases), 7, "Le nombre total de cases est incorrect.")
        self.assertEqual(self.plateau.cases[0].type, "DEPART", "La première case devrait être DEPART.")
        self.assertEqual(self.plateau.cases[-1].type, "ARRIVE", "La dernière case devrait être ARRIVE.")

    def test_create_cases_error(self):
        """Cas d'erreur : Nombre de cases négatif."""
        self.plateau.nombre_cases = -1
        with self.assertRaises(ValueError, msg="Une erreur aurait dû être levée pour un nbCases négatif."):
            self.plateau.create_cases()

    def test_faire_plateau_normal(self):
        """Cas normal : Les cases sont placées correctement sur le plateau."""
        self.plateau.cases = [Case("DEPART"), Case("NEUTRE"), Case("ARRIVE")]
        self.plateau.faire_plateau()

        # Vérifie que les cases sont placées sur le plateau
        plateau_cases = [case for row in self.plateau.plateau for case in row if case.type != "VIDE"]
        self.assertEqual(len(plateau_cases), len(self.plateau.cases), "Le placement des cases est incorrect.")

    def test_faire_plateau_error(self):
        """Cas d'erreur : Trop de cases pour la taille du plateau."""
        self.plateau.size = 2  # Plateau trop petit
        self.plateau.cases = [Case("DEPART"), Case("NEUTRE"), Case("NEUTRE"), Case("ARRIVE")]

        with self.assertRaises(Exception, msg="Une erreur aurait dû être levée pour un plateau trop petit."):
            self.plateau.faire_plateau()

    def test_afficher_plateau(self):
        """Test de l'affichage du plateau sur le canvas"""
        # Simulation des cases du plateau
        self.plateau.plateau = [
            [Case("DEPART"), Case("VIDE"), Case("ARRIVE")],
            [Case("VIDE"), Case("NEUTRE"), Case("VIDE")],
            [Case("JEU"), Case("VIDE"), Case("EVENT")]
        ]
        self.plateau.cases = [
            Case("DEPART"),
            Case("NEUTRE"),
            Case("JEU"),
            Case("EVENT"),
            Case("ARRIVE")
        ]
        self.plateau.joueur = Joueur(0)  # Position initiale du joueur

        # Appel de la méthode à tester
        self.plateau.afficher_plateau()

        # Vérification des rectangles dessinés (correspondant aux cases)
        self.assertEqual(self.plateau.canvas.create_rectangle.call_count, 9,
                         "Le nombre de cases dessinées est incorrect.")

        # Vérification de l'affichage du joueur (ovale)
        self.plateau.canvas.create_oval.assert_called_once_with(
            ANY, ANY, ANY, ANY, fill=self.plateau.couleurs["JOUEUR"]
        )


if __name__ == "__main__":
    unittest.main()
