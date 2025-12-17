"""
ici on pourra mettre des tests unitaires (si on a le courage)
on va utiliser pytest (pour l'installer : pip install pytest)
"""

"""Étant donné une carte avec un niveau initial, lorsque la méthode connue() est appelée,
     alors le niveau de la carte augmente de 1 sans dépasser la valeur maximale autorisée."""

import unittest
from unittest.mock import MagicMock, patch
from modules.flashCard import FlashCards
from modules.chapitre import Chapitres
from modules.carte import Cartes
from modules.quiz import Quiz

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

class TestQuiz(unittest.TestCase):
    def setUp(self):
        self.chapitre = Chapitres("TestUnitaire")
        self.carte1 = Cartes(1, "Capitale de la Belgique ?", "Bruxelles", "")
        self.carte2 = Cartes(2, "5*5 ?", "25", "")
        self.chapitre.cartes = {1: self.carte1, 2: self.carte2}

        self.quiz = Quiz(self.chapitre)

    def test_init(self):
        self.assertEqual(self.quiz.score, 0)
        self.assertEqual(self.quiz.chapitre, self.chapitre)

    def test_tirer_cartes(self):
        carte = self.quiz.tirer_cartes()
        self.assertIn(carte, self.chapitre.cartes.values())
    
    def test_question_ouverte_bon(self):
        carte = self.carte1
        reponse_utilisateur = "Bruxelles"
        if reponse_utilisateur.lower() == carte.reponse.lower():
            self.quiz.score += 1
            carte.connue()

        self.assertEqual(carte.niveau, 5)
        self.assertEqual(self.quiz.score, 1)
    
    def test_question_ouverte_mauvais(self):
        carte = self.carte1
        reponse_utilisateur = "Paris"
        if reponse_utilisateur.lower() != carte.reponse.lower():
            carte.pas_connue()

        self.assertEqual(carte.niveau, 3)
        self.assertEqual(self.quiz.score, 0)