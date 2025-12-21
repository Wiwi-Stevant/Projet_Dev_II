import random

# Exception personnalisée
class FlashCardError(Exception):
    pass


class FlashCards:
    def __init__(self, chapitre):
        """
        Initialise FlashCards avec un chapitre existant.
        - chapitre : instance de Chapitres
        """
        self._chapitre = chapitre
        self._ids = list(chapitre.cartes.keys())  # liste des IDs des cartes
        self._index = 0

    @property
    def chapitre(self):
        """Retourne le chapitre associé"""
        return self._chapitre

    @chapitre.setter
    def chapitre(self, nouveau_chapitre):
        if nouveau_chapitre is None:
            raise FlashCardError("Le chapitre ne peut pas être vide")
        self._chapitre = nouveau_chapitre
        self.mettre_a_jour_cartes()

    @property
    def ids(self):
        """Retourne la liste des IDs des cartes"""
        return self._ids

    @property
    def index(self):
        """Retourne l index courant"""
        return self._index

    def mettre_a_jour_cartes(self):  #chat gpt
        """Met à jour la liste des IDs si le chapitre change"""
        self._ids = list(self._chapitre.cartes.keys())
        if self._index >= len(self._ids):
            self._index = 0

    def generer_cartes(self):
        """
        Générateur qui parcourt  les cartes une par une.

        PRE:
            - Un chapitre valide est associé à l’objet FlashCards.
            - Le chapitre peut contenir zéro ou plusieurs cartes.

        POST:
            - Les cartes sont retournées une par une grâce au mot-clé yield.
            - L’ordre de retour des cartes correspond à celui du dictionnaire des cartes dans le chapitre.
        """
        for carte in self._chapitre.cartes.values():
            yield carte       

    def tirer_carte(self):
        """Tire une carte aléatoire selon le niveau (plus faible = plus de chances)"""
        cartes = list(self._chapitre.cartes.values())
        if not cartes:
            raise FlashCardError("Aucune carte disponible pour le tirage")


        poids = [max(1, 5 - c.niveau) for c in cartes]  # plus le niveau est bas, plus la carte est tirée
        return random.choices(cartes, weights=poids, k=1)[0]
    
    def toutes_les_questions(self):
        """Retourne la liste de toutes les questions du chapitre"""
        return list(map(lambda c: c.question, self._chapitre.cartes.values()))


    def retourner(self, id_carte):
        """Retourne la réponse de la carte sélectionnée"""
        if id_carte not in self._chapitre.cartes:
            raise FlashCardError(f"La carte avec l ID {id_carte} n existe pas")
        return self._chapitre.cartes[id_carte].reponse
    
    def cartes_difficiles(self, seuil=3):
        """Retourne les cartes dont le niveau est inférieur ou égal au seuil"""
        return list(filter(lambda c: c.niveau <= seuil, self._chapitre.cartes.values()))


    def carte_suivante(self):
        """Passe à la carte suivante et retourne sa question"""
        if not self._ids:
            raise FlashCardError("Aucune carte dans le chapitre")


        self._index = (self._index + 1) % len(self._ids)
        id_carte = self._ids[self._index]
        return self._chapitre.cartes[id_carte].question
    
    



    def __str__(self):
        return f"FlashCards(chapitre={self._chapitre.nom}, cartes={len(self._ids)})"
