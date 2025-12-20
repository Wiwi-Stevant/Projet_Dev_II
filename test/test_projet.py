import unittest
from modules.carte import Cartes
from modules.flashCard import FlashCards
from modules.chapitre import Chapitres

class TestCartes(unittest.TestCase):

    def test_jsonification_carte(self):
        carte = Cartes(
            id=1,
            question="Q1",
            reponse="R1",
            img="img.png",
            niveau=4
        )

        resultat = carte.jsonification()

        attendu = {
            "id": 1,
            "question": "Q1",
            "reponse": "R1",
            "img": "img.png",
            "niveau": 4
        }

        self.assertEqual(resultat, attendu)



class TestFlashCards(unittest.TestCase):

    def test_generer_cartes(self):
        chap = Chapitres("Test")
        chap.cree_cartes("Q1", "R1", None)
        chap.cree_cartes("Q2", "R2", None)

        fc = FlashCards(chap)
        cartes = list(fc.generer_cartes())

        self.assertEqual(len(cartes), 2)
        self.assertEqual(cartes[0].question, "Q1")
        self.assertEqual(cartes[1].question, "Q2")

