"""Module gérant le quiz."""
from modules.chapitre import Chapitres

import random
import re

class Quiz:
    """Classe gérant le quiz pour un chapitre donné."""
    def __init__(self, chapitre):
        if isinstance(chapitre, Chapitres): # --> chat GPT
            self.chapitre = chapitre
        else:
            self.chapitre = Chapitres(chapitre)
            self.chapitre.charger_cartes()
        self.score = 0

    @staticmethod
    def choix_aleatoire(liste):
        """Retourne un élément aléatoire d'une liste donnée."""
        return random.choice(liste)

#charger un chapitre et tirer une carte aléatoirement
    def tirer_cartes(self):
        """Tire une carte aléatoire du chapitre."""
        liste_cartes = list(self.chapitre.cartes.values())
        return Quiz.choix_aleatoire(liste_cartes)

    def jouer(self):
        """Démarre le quiz."""
        print(f" [===== {self.chapitre.nom} =====]\nTapez 'q' pour quitter à tout moment.\n")
        compteur = 0
        type_questions = ["ouvert", "vraiFaux", "qcm"]

        while True:
            carte_actuelle = self.tirer_cartes()
            type_actuel = random.choice(type_questions)
            regex_reponse = re.compile(r"^[a-zA-ZÀ-ÿ0-9\s]+$")

            if type_actuel == "ouvert":
                print(f"\nQuestion : {carte_actuelle.question}")
                reponse_utilisateur = input("Entrez votre réponse : ")
                print("")
                if reponse_utilisateur.lower() == "q":
                    break
                if not regex_reponse.match(reponse_utilisateur):
                    print("    => Réponse invalide (caractères non autorisés)\n")
                    continue
                if reponse_utilisateur.lower() == carte_actuelle.reponse.lower():
                    print("    => Bonne réponse !\n")
                    self.score += 1
                    carte_actuelle.connue()
                else:
                    print("    => Mauvaise réponse !")
                    print(f"La bonne réponse était {carte_actuelle.reponse}\n")
                    carte_actuelle.pas_connue()

                compteur += 1

            elif type_actuel == "vraiFaux":
                autre_carte = self.tirer_cartes()
                reponses = [carte_actuelle.reponse, autre_carte.reponse]
                question = carte_actuelle.question
                reponse = random.choice(reponses)
                if reponse == carte_actuelle.reponse:
                    reponse_question = "v"
                else:
                    reponse_question = "f"
                reponse_utilisateur = ""
                while reponse_utilisateur.lower() != "v" and reponse_utilisateur.lower() != "f" and reponse_utilisateur.lower() != "q":
                    print(f" <== Vrai ou Faux ==> \n\nQuestion : {question} \nRéponse : {reponse}")
                    reponse_utilisateur = input("Répondez par v, f ou q : ")
                    print("")
                    if reponse_utilisateur.lower() not in ("v", "f", "q"):
                        print("Répondez par v, f ou q")
                if reponse_utilisateur.lower() == "q":
                    break
                elif reponse_utilisateur.lower() == reponse_question:
                    print("    => Bonne réponse !\n")
                    self.score += 1
                    carte_actuelle.connue()
                else:
                    print(f"    => Mauvaise réponse ! La bonne réponse était {reponse_question}\n")
                    carte_actuelle.pas_connue()
                compteur += 1

        print(f"\n <== Quiz terminé ! Score final : {self.score}/{compteur} ==>\n")
