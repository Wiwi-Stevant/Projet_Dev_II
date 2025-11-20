import json
from modules.carte import Cartes

class Chapitres:
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom
        self.sauvgarde = f"{self.nom}.json".lower()

    def charger_cartes(self):
        pass

    def sauvegarder_cartes(self):
        pass

    def cree_cartes(self, id, question, reponse, img=""):
        pass

    def supprimer_carte(self, id):
        pass

    def modifier_carte(self, id, question, reponse, img):
        pass

    def afficher_cartes(self):
        pass