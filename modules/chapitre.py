import json
import os
from modules.carte import Cartes

class Chapitres:
    id = 1
    def __init__(self, nom):
        Chapitres.idGlobal += 1
        self.id = Chapitres.idGlobal
        self.cartes = {}
        self.idCarte = 1
        self.nom = nom
        self.sauvgarde = f"{self.nom}.json".lower() #on met le non du chapitre avec .json pour dire quel fichier gere la sauvgarde du chap

    def charger_cartes(self): #on recupere les carte depuis le json
        if os.path.exists(self.sauvgarde):
            with open(self.sauvgarde, 'r', encoding='utf-8') as f:
                data = json.load(f)
                cartes = []
                for carte_data in data:
                    carte = Cartes(
                        carte_data['id'],
                        carte_data['question'],
                        carte_data['reponse'],
                        carte_data.get('img', "")
                    )
                    cartes.append(carte)
                return cartes
        else:
            print("Le Chapitre n'existe pas encore.")

    def sauvegarder_cartes(self): #on sauvgarde les cartes dans le json -----> metode fait avec AI
        data_cartes = [carte.to_dict() for carte in self.cartes.values()]
        with open(f"../data/{self.sauvgarde}", 'w', encoding='utf-8') as f:
            json.dump(data_cartes, f, ensure_ascii=False, indent=4)
        print(f"chapitre {self.nom} sauvgardé dans {self.sauvgarde}.")

    def cree_cartes(self, question, reponse, img=""): #on cree une nouvelle carte
        nouvelle_id = self.idCarte
        nouvelle_carte = Cartes(nouvelle_id, question, reponse, img)
        self.cartes[nouvelle_id] = nouvelle_carte
        self.idCarte += 1
        print(f"La carte {nouvelle_id} : '{question}', {reponse} a été créée.")
        self.sauvegarder_cartes()
        return nouvelle_carte

    def supprimer_carte(self, id):# on supprime une carte via son id ou sa question jsp 
        pass

    def modifier_carte(self, id, question, reponse, img):
        pass

    def __str__(self): # on affiche toutes les carte du chap
        print(f"voici les cartes du chapitre {self.nom} ({self.id}) :")
        for carte in self.cartes.values():
            print(carte)