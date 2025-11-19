import random
from mvpCarte import Carte

class Chapitre:
    def __init__(self, nom):
        self.nom = nom
        self.cartes = {}

    def cree_cartes(self, carte_id, question, reponse, image = None):
        if carte_id in self.cartes:
            raise ValueError("La carte existe déjà")
        self.cartes[carte_id] = Carte(carte_id, question, reponse, image)
    
    def supprimer_carte(self, carte_id):
        carte = self.cartes.pop(carte_id)
    
    def modifier_carte(self, carte_id, question, reponse):
        if carte_id not in self.cartes:
            raise ValueError("La carte n'existe pas")
        carte = self.cartes[carte_id]
        carte.question = question
        carte.reponse = reponse