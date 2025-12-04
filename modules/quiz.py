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
        while True:
            carteActuelle = self.tirer_cartes()
            print(f"Question : {carteActuelle.question}")
            reponse_utilisateur = input("Entrez votre réponse (q pour quitter)")
            if reponse_utilisateur.lower() == "q":
                break
            if reponse_utilisateur.lower() == carteActuelle.reponse.lower():
                print("Bonne réponse !")
                self.score += 1
                carteActuelle.connue()
            else:
                print(f"Mauvaise réponse ! La bonne réponse était {carteActuelle.reponse}")
                carteActuelle.pas_connue()
            compteur += 1
            

#quiz = Quiz('test')
#quiz.jouer()