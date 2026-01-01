"""permet de gérer les fichiers de chapitres et les opérations associées."""
import json
import os
from modules.carte import Cartes

#création de l'exception personnalisée
class CarteInexistante(Exception):
    pass

class Chapitres:
    """Classe représentant un chapitre contenant des cartes de flashcards."""
    idGlobal = 0
    def __init__(self, nom):
        Chapitres.idGlobal += 1
        self.id = Chapitres.idGlobal
        self.cartes = {}
        self.id_carte = 1
        self.nom = nom
        self.sauvegarde = f"{self.nom}.json".lower() #on cree le nom du fichier de sauvegarde

    def _get_data_path(self): # chemin du fichier de sauvegarde (chat GPT)
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, self.sauvegarde)

    def charger_cartes(self):
        """Charge les cartes depuis le fichier JSON associé au chapitre."""

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
                        self.id_carte = max(self.id_carte, carte.id + 1)

        except FileNotFoundError:
            print("Le Chapitre n'existe pas encore.")

    def sauvegarder_cartes(self):
        """Sauvegarde les cartes dans le fichier JSON associé au chapitre."""

        data_cartes = [carte.jsonification() for carte in self.cartes.values()]
        fichier_path = self._get_data_path()

        with open(fichier_path, 'w', encoding='utf-8') as f:
            json.dump(data_cartes, f, ensure_ascii=False, indent=4)
        print(f"chapitre {self.nom} sauvgardé dans {fichier_path}.")

    def cree_cartes(self, question, reponse, img=""):
        """Crée une nouvelle carte et l'ajoute au chapitre."""

        nouvelle_id = self.id_carte
        nouvelle_carte = Cartes(nouvelle_id, question, reponse, img)
        self.cartes[nouvelle_id] = nouvelle_carte
        self.id_carte += 1
        print(f"La carte {nouvelle_id} : '{question}', {reponse} a été créée.")
        self.sauvegarder_cartes()
        return nouvelle_carte

    def supprimer_carte(self, id):
        """Supprime une carte du chapitre en fonction de son ID."""

        try:
            self.cartes.pop(id)
        except KeyError:
            raise CarteInexistante(f"Erreur : l'id {id} n'existe pas")
        else:
            self.sauvegarder_cartes()

    def modifier_carte(self, id, question, reponse, img):
        """Modifie une carte existante dans le chapitre."""

        if id not in self.cartes:
            raise ValueError("La carte n'existe pas")
        carte = self.cartes[id]
        carte.question = question
        carte.reponse = reponse
        carte.img = img
        self.sauvegarder_cartes()

    def nombre_cartes(self):
        """Renvoie le nombre de cartes dans le chapitre."""

        compteur = 0
        for _ in self.cartes:
            compteur += 1
        yield compteur # utilisation d'un générateur

    def __str__(self):
        """on affiche toutes les cartes du chapitre"""

        retours = f" [===== {self.nom} ({self.id}) =====]"

        for carte in self.cartes.values():
            retours += f"\n{carte}"

        return retours
