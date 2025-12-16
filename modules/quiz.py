from modules.chapitre import Chapitres
import random
import re
class Quiz:
    def __init__(self, chapitre):
        if isinstance(chapitre, Chapitres): # --> chat GPT
            self.chapitre = chapitre
        else:
            self.chapitre = Chapitres(chapitre)
            self.chapitre.charger_cartes()
        self.score = 0

    @staticmethod
    def choix_aleatoire(liste):
        return random.choice(liste)

#charger un chapitre et tirer une carte aléatoirement
    def tirer_cartes(self): 
        listeCartes = list(self.chapitre.cartes.values())
        return Quiz.choix_aleatoire(listeCartes)
            
    def jouer(self):
        print(f" [===== {self.chapitre.nom} =====]\nTapez 'q' pour quitter à tout moment.\n")
        compteur = 0
        type_questions = ["ouvert", "vraiFaux", "qcm"]

        while True:
            carteActuelle = self.tirer_cartes()
            type_actuel = random.choice(type_questions)
            regex_reponse = re.compile(r"^[a-zA-ZÀ-ÿ0-9\s]+$")

            if type_actuel == "ouvert":
                print(f"\nQuestion : {carteActuelle.question}")
                reponse_utilisateur = input("Entrez votre réponse : ")
                print("")
                if reponse_utilisateur.lower() == "q":
                    break
                if not regex_reponse.match(reponse_utilisateur):
                    print("    => Réponse invalide (caractères non autorisés)\n")
                    continue
                if reponse_utilisateur.lower() == carteActuelle.reponse.lower():
                    print("    => Bonne réponse !\n")
                    self.score += 1
                    carteActuelle.connue()
                else:
                    print(f"    => Mauvaise réponse ! La bonne réponse était {carteActuelle.reponse}\n")
                    carteActuelle.pas_connue()

                compteur += 1

            elif type_actuel == "vraiFaux":
                autreCarte = self.tirer_cartes()
                reponses = [carteActuelle.reponse, autreCarte.reponse]
                question = carteActuelle.question
                reponse = random.choice(reponses)
                if reponse == carteActuelle.reponse:
                    reponseQuestion = "v"
                else:
                    reponseQuestion = "f"
                reponse_utilisateur = ""
                while reponse_utilisateur.lower() != "v" and reponse_utilisateur.lower() != "f" and reponse_utilisateur.lower() != "q":
                    reponse_utilisateur = input(f" <== Vrai ou Faux ==> \n\nQuestion : {question} \nRéponse : {reponse} \nRépondez par v, f ou q : ")
                    print("")
                    if reponse_utilisateur.lower() not in ("v", "f", "q"):
                        print("Répondez par v, f ou q")
                if reponse_utilisateur.lower() == "q":
                    break
                elif reponse_utilisateur.lower() == reponseQuestion:
                    print("    => Bonne réponse !\n")
                    self.score += 1
                    carteActuelle.connue()
                else:
                    print(f"    => Mauvaise réponse ! La bonne réponse était {reponseQuestion}\n")
                    carteActuelle.pas_connue()
                compteur += 1

        print(f"\n <== Quiz terminé ! Score final : {self.score}/{compteur} ==>\n")
            
