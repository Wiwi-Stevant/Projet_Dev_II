"""
ici on pourra mettre des tests unitaires (si on a le courage)
on va utiliser pytest (pour l'installer : pip install pytest)
"""

"""Étant donné une carte avec un niveau initial, lorsque la méthode connue() est appelée,
     alors le niveau de la carte augmente de 1 sans dépasser la valeur maximale autorisée."""

import unittest
from modules.flashCard import FlashCards
from modules.chapitre import Chapitres
from modules.carte import Cartes

class TestCartes(unittest.TestCase):

    def test_connue_augmente_niveau(self):
        carte = Cartes(1, "Question ?", "Réponse", None, niveau=4)
        carte.connue()
        self.assertEqual(carte.get_niveau(), 5)


"""Étant donné un chapitre contenant plusieurs cartes, lorsque la méthode generer_cartes() est utilisée,
 alors les cartes sont retournées une par une dans l’ordre, sans créer de liste intermédiaire."""



class TestFlashCards(unittest.TestCase):

    def test_generateur_cartes(self):
        chap = Chapitres("Test")
        chap.cree_cartes("Q1", "R1", None)
        chap.cree_cartes("Q2", "R2", None)

        fc = FlashCards(chap)

        cartes = list(fc.generer_cartes())

        self.assertEqual(len(cartes), 2)
        self.assertEqual(cartes[0].question, "Q1")
        self.assertEqual(cartes[1].question, "Q2")
