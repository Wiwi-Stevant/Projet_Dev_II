import random

class FlashCards:
    def __init__(self, chapitre):
        """
        Initialise FlashCards avec un chapitre existant.
        - chapitre : instance de Chapitres
        """
        self._chapitre = chapitre
        self._ids = list(chapitre.cartes.keys())  # liste des IDs des cartes
        self._index = 0

    def mettre_a_jour_cartes(self):
        """Met à jour la liste des IDs si le chapitre change"""
        self._ids = list(self._chapitre.cartes.keys())
        if self._index >= len(self._ids):
            self._index = 0

    def tirer_carte(self):
        """Tire une carte aléatoire selon le niveau (plus faible = plus de chances)"""
        cartes = list(self._chapitre.cartes.values())
        if not cartes:
            print("Aucune carte disponible.")
            return None

        poids = [max(1, 5 - c.niveau) for c in cartes]  # plus le niveau est bas, plus la carte est tirée
        return random.choices(cartes, weights=poids, k=1)[0]

    def retourner(self, id_carte):
        """Retourne la réponse de la carte sélectionnée"""
        if id_carte not in self._chapitre.cartes:
            print("Carte introuvable.")
            return None
        return self._chapitre.cartes[id_carte].reponse

    def carte_suivante(self):
        """Passe à la carte suivante et retourne sa question"""
        if not self._ids:
            print("Aucune carte dans le chapitre.")
            return None

        self._index = (self._index + 1) % len(self._ids)
        id_carte = self._ids[self._index]
        return self._chapitre.cartes[id_carte].question
