"""import pour les test unitaires"""
import unittest
from unittest.mock import MagicMock, patch
from modules.chapitre import Chapitres
from modules.carte import Cartes
from modules.quiz import Quiz
from modules.flashCard import FlashCards

class TestQuiz(unittest.TestCase):
    """Tests unitaires pour la classe Quiz."""
    def setUp(self):
        self.chapitre = Chapitres("TestUnitaire")
        self.carte1 = Cartes(1, "Capitale de la Belgique ?", "Bruxelles", "")
        self.carte2 = Cartes(2, "5*5 ?", "25", "")
        self.chapitre.cartes = {1: self.carte1, 2: self.carte2}

        self.quiz = Quiz(self.chapitre)

    def test_init(self):
        """Test de l'initialisation de la classe Quiz."""
        self.assertEqual(self.quiz.score, 0)
        self.assertEqual(self.quiz.chapitre, self.chapitre)

    def test_tirer_cartes(self):
        """Test de la méthode tirer_cartes."""
        carte = self.quiz.tirer_cartes()
        self.assertIn(carte, self.chapitre.cartes.values())

    def test_question_ouverte_bon(self):
        """Test de la gestion d'une question ouverte avec bonne réponse."""
        carte = self.carte1
        reponse_utilisateur = "Bruxelles"
        if reponse_utilisateur.lower() == carte.reponse.lower():
            self.quiz.score += 1
            carte.connue()

        self.assertEqual(carte.niveau, 5)
        self.assertEqual(self.quiz.score, 1)

    def test_question_ouverte_mauvais(self):
        """Test de la gestion d'une question ouverte avec mauvaise réponse."""
        carte = self.carte1
        reponse_utilisateur = "Paris"
        if reponse_utilisateur.lower() != carte.reponse.lower():
            carte.pas_connue()

        self.assertEqual(carte.niveau, 3)
        self.assertEqual(self.quiz.score, 0)

class TestCartes(unittest.TestCase):
    """Tests unitaires pour la classe Cartes."""
    def test_jsonification_carte(self):
        """Test de la méthode jsonification de la classe Cartes."""
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
    """Tests unitaires pour la classe FlashCards."""
    def test_generer_cartes(self):
        """Test de la méthode generer_cartes de la classe FlashCards."""
        chap = Chapitres("Test")
        chap.cree_cartes("Q1", "R1", None)
        chap.cree_cartes("Q2", "R2", None)

        fc = FlashCards(chap)
        cartes = list(fc.generer_cartes())

        self.assertEqual(len(cartes), 2)
        self.assertEqual(cartes[0].question, "Q1")
        self.assertEqual(cartes[1].question, "Q2")
