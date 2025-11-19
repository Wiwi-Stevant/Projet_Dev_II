import random
from mvpQuiz import Quiz
from mvpChapitre import Chapitre
from mvpFlashCards import FlashCards

chapitre = Chapitre("Maths")
chapitre.cree_cartes(1, "2+2 ?", "4")
chapitre.cree_cartes(2, "3+2 ?", "5")

jeu = input("choix jeu : Q ou F")
if jeu.lower() == "q":
    quiz = Quiz(chapitre)
    quiz.jouer()
elif jeu.lower() == "f":
    flashcards = FlashCards(chapitre)
    flashcards.jouer()