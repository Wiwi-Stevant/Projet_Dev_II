import random
from mvpChapitre import Chapitre

class Quiz:
    def __init__(self, chapitre):
        self.chapitre = chapitre
        self.score = 0

    def tirer_carte(self):
        cartes = list(self.chapitre.cartes.values())
        poids = []
        for c in cartes:
            poids.append(max(1, 5 - c.niveau))
        return random.choices(cartes, weights=poids, k=1)[0]
    
    def jouer(self):
        print(f"Mode Quiz : {self.chapitre.nom}")
        compteur = 0
        while True:
            carte = self.tirer_carte()
            print(f"Question : {carte.question}")
            reponsee_utilisateur = input("Votre réponse (q pour quitter) : ")
            if reponsee_utilisateur.lower() == "q":
                break
            if reponsee_utilisateur.lower() == carte.reponse.lower():
                print("Bonne réponse !")
                self.score += 1
                carte.connue()
            else:
                print(f"Mauvaise réponse ! La bonne réponse était {carte.reponse}")
                carte.pas_connue()
            compteur += 1
        
        print(f"Votre score est de {self.score} sur {compteur}")