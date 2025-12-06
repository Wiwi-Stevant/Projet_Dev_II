from modules.chapitre import Chapitres
import random
import os
import json
class Quiz:
    def __init__(self, chapitre):
        if isinstance(chapitre, Chapitres): # --> chat GPT
            self.chapitre = chapitre
        else:
            self.chapitre = Chapitres(chapitre)
            self.chapitre.charger_cartes()
        self.score = 0

#charger un chapitre et tirer une carte aléatoire
    def tirer_cartes(self): 
        listeCartes = list(self.chapitre.cartes.values())
        return random.choice(listeCartes)
            
    def jouer(self):
        print(f"Quiz sur le chapitre : {self.chapitre.nom}")
        compteur = 0
        type_questions = ["ouvert", "vraiFaux", "qcm"]
        while True:
            carteActuelle = self.tirer_cartes()
            type_actuel = random.choice(type_questions)
            if type_actuel == "ouvert":
                print(f"Question : {carteActuelle.question}")
                reponse_utilisateur = input("Entrez votre réponse (q pour quitter)")
                if reponse_utilisateur.lower() == "q":
                    break
                elif reponse_utilisateur.lower() == carteActuelle.reponse.lower():
                    print("Bonne réponse !")
                    self.score += 1
                    carteActuelle.connue()
                else:
                    print(f"Mauvaise réponse ! La bonne réponse était {carteActuelle.reponse}")
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
                    reponse_utilisateur = input(f"Vrai(v) ou Faux(f) : \nQuestion : {question} \nRéponse : {reponse} (q pour quitter)")
                    if reponse_utilisateur.lower() not in ("v", "f", "q"):
                        print("Répondez par v, f ou q")
                if reponse_utilisateur.lower() == "q":
                    break
                elif reponse_utilisateur.lower() == reponseQuestion:
                    print("Bonne réponse !")
                    self.score += 1
                    carteActuelle.connue()
                else:
                    print(f"Mauvaise réponse ! La bonne réponse était {reponseQuestion}")
                    carteActuelle.pas_connue()
                compteur += 1
        print(f"Quiz terminé ! Score final : {self.score}/{compteur}")
            
