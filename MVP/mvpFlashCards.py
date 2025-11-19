import random
from mvpChapitre import Chapitre


class FlashCards:
    def __init__(self, chapitre):
        self.chapitre = chapitre

    def tirer_carte(self):
        cartes = list(self.chapitre.cartes.values())
        poids = []
        for c in cartes:
            poids.append(max(1, 5 - c.niveau))
        return random.choices(cartes, weights=poids, k=1)[0]

    def jouer(self):
        print(f"Mode FlashCards : {self.chapitre.nom}")

        while True:
            carte = self.tirer_carte()

            print(f"Question : {carte.question}")
            input("Appuyer sur Entrer pour voir la réponse")
            print(f"Réponse : {carte.reponse}")

            choix = input("Connu (c), Pas connu (p), Quitter (q) : ")
            if choix.lower() == "q":
                break
            elif choix.lower() == "c":
                carte.connue()
            elif choix.lower() == "p":
                carte.pas_connue()