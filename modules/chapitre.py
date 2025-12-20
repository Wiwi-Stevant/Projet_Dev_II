import json
import os
from modules.carte import Cartes

#création de l'exception personnalisée
class CarteInexistante(Exception):
    pass
class Chapitres:
    idGlobal = 0
    def __init__(self, nom):
        Chapitres.idGlobal += 1
        self.id = Chapitres.idGlobal
        self.cartes = {}
        self.idCarte = 1
        self.nom = nom
        self.sauvegarde = f"{self.nom}.json".lower() #on met le nom du chapitre avec .json pour dire quel fichier gere la sauvgarde du chap

    def _get_data_path(self): # chemin du fichier de sauvegarde (chat GPT)
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, self.sauvegarde)

    def charger_cartes(self):# On récupère les cartes depuis le json
        fichier_path = self._get_data_path() 
        try :
            with open(fichier_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for carte_data in data:
                        carte = Cartes(
                            carte_data['id'],
                            carte_data['question'],
                            carte_data['reponse'],
                            carte_data.get('img', ""),
                            carte_data.get('niveau', 4)
                        )
                        self.cartes[carte.id] = carte
                        self.idCarte = max(self.idCarte, carte.id + 1)
        except FileNotFoundError:
            print("Le Chapitre n'existe pas encore.")

    def sauvegarder_cartes(self):  # On sauvegarde les cartes dans le json
        data_cartes = [carte.jsonification() for carte in self.cartes.values()]
        fichier_path = self._get_data_path()
        with open(fichier_path, 'w', encoding='utf-8') as f:
            json.dump(data_cartes, f, ensure_ascii=False, indent=4)
        print(f"chapitre {self.nom} sauvgardé dans {fichier_path}.")

    def cree_cartes(self, question, reponse, img=""): #on cree une nouvelle carte
        nouvelle_id = self.idCarte
        nouvelle_carte = Cartes(nouvelle_id, question, reponse, img)
        self.cartes[nouvelle_id] = nouvelle_carte
        self.idCarte += 1
        print(f"La carte {nouvelle_id} : '{question}', {reponse} a été créée.")
        self.sauvegarder_cartes()
        return nouvelle_carte

    def supprimer_carte(self, id):# on supprime une carte via son id 
        try:
            self.cartes.pop(id)
        except KeyError:
            raise CarteInexistante(f"Erreur : l'id {id} n'existe pas")
        else:
            self.sauvegarder_cartes()


    def modifier_carte(self, id, question, reponse, img):
        if id not in self.cartes:
            raise ValueError("La carte n'existe pas")
        carte = self.cartes[id]
        carte.question = question
        carte.reponse = reponse
        carte.img = img
        self.sauvegarder_cartes()

    def nombre_cartes(self): # on compte le nombre de cartes dans le chapitre
        compteur = 0
        for _ in self.cartes:
            compteur += 1
        yield compteur # utilisation d'un générateur

    def __str__(self): # on affiche toutes les cartes du chapitre
        print(f" [===== {self.nom} ({self.id}) =====]")

        for carte in self.cartes.values():
            print(carte)