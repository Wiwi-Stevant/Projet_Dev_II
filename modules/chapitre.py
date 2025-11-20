import json
from modules.carte import Cartes

class Chapitres:
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom
        self.sauvgarde = f"{self.nom}.json".lower() #on met le non du chapitre avec .json pour dire quel fichier gere la sauvgarde du chap

    def charger_cartes(self): #on recupere les carte depuis le json
        pass

    def sauvegarder_cartes(self): #on sauvgarde les cartes dans le json
        pass

    def cree_cartes(self, id, question, reponse, img=""): #on cree une nouvelle carte
        pass

    def supprimer_carte(self):# on supprime une carte via son id ou sa question jsp 
        pass

    def modifier_carte(self, id, question, reponse, img):
        pass

    def __str__(self): # on affiche toutes les carte du chap
        pass