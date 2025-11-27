from chapitre import Chapitres
import random
import os
import json
class Quiz:
    def __init__(self, chapitre):
        self.score = 0
        self.chapitre = chapitre

#charger un chapitre et tirer une carte aléatoire
    def tirer_cartes(self): 
        cartes = os.path.relpath(f'../data/{self.chapitre}.json')
        print(cartes)
chapitre = Chapitres('test')
quiz = Quiz(chapitre)