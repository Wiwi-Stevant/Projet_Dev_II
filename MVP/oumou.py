class Carte:
    def _init_(self, id: int, question: str, reponse: str, niveau: int = 1, image=None):
        self.id = id
        self.question = question
        self.repnse = reponse
        self.niveau = niveau
        self.image = image

    def changer_niveau(self, id: int):
        """Change le niveau en fonction d'un id reçu (ex: résultat du quiz)."""
        self.niveau = id
        return self.niveau




class Chapitre:
    def _init_(self, nom: str):
        self.nom = nom
        self.cartes = {}   # dict des cartes : {id: Carte}

    def cree_cartes(self, id: int, question: str, reponse: str):
        """Crée une nouvelle carte et l'ajoute au dictionnaire."""
        self.cartes[id] = Carte(id, question, reponse)

    def cree_titre(self, titre: str):
        """Change le nom du chapitre."""
        self.nom = titre

    def supprimer_carte(self, id: int):
        """Supprime une carte via son id"""
        if id in self.cartes:
            del self.cartes[id]

    def modifier_carte(self, id: int, q: str, r: str, n: int):
        """Modifie question, réponse et niveau d'une carte."""
        if id in self.cartes:
            self.cartes[id].question = q
            self.cartes[id].reponse = r
            self.cartes[id].niveau = n



class FlashCards:
    def _init_(self, chapitre):
        # On garde le chapitre et la liste des IDs des cartes
        self.chapitre = chapitre
        self.ids = list(chapitre.cartes.keys())
        self.index = 0

    def retourner(self):
        """Retourne la réponse de la carte actuelle"""
        id_carte = self.ids[self.index]
        carte = self.chapitre.cartes[id_carte]
        return carte.reponse

    def carte_suivante(self):
        """Passe à la carte suivante et retourne la question."""
        self.index = (self.index + 1) % len(self.ids)
        id_carte = self.ids[self.index]
        carte = self.chapitre.cartes[id_carte]
        return carte.question

    def demarrer(self):
        """Revient au début de la liste des cartes."""
        self.index = 0