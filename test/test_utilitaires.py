"""import pour les test unitaires"""
import unittest
from unittest.mock import MagicMock, patch
from modules.chapitre import Chapitres
from modules.carte import Cartes
from modules.quiz import Quiz


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
