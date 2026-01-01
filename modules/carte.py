class Cartes:
    """Classe représentant une carte de flashcard avec question, 
    réponse, image et niveau de connaissance."""

    limiter_niveau = lambda self, n: max(0, min(10, n))
    def __init__(self, id, question, reponse, img ,niveau = 4):
        self.id = id
        self.reponse = reponse
        self.question = question
        self.img = img
        self.niveau = niveau # change le niveau d'apparition de la carte

    def get_niveau(self):
        """Renvoie le niveau de la carte."""
        return self.niveau

    def set_niveau(self, niveau): 
        """Définit le niveau de la carte en le limitant entre 0 et 10."""
        self.niveau = self.limiter_niveau(niveau)
        print(self.id, self.niveau) # tuple affichant le niveau actuel de la carte.

    def connue(self):
        """On augmente le niveau de la carte."""
        self.set_niveau(self.niveau + 1)

    def pas_connue(self):
        """On diminue le niveau de la carte."""
        self.set_niveau(self.niveau - 1)

    def jsonification(self): # on met la carte en json pour la sauvgarde
        """ 
        PRE:
            - La carte possède des attributs valides : 
            id (int), question (str), reponse (str), img (str), niveau (int).

        POST:
            - Retourne un dictionnaire contenant toutes 
            les informations de la carte sous forme clé-valeur.
            - Le dictionnaire est prêt à être sauvegardé ou transmis en JSON.
        """
        return {
            "id": self.id,
            "reponse": self.reponse,
            "question": self.question,
            "img": self.img,
            "niveau": self.niveau
        }

    def __str__(self):
        """Renvoie une représentation textuelle de la carte."""

        retours = f"\n => Carte n°{self.id},"
        retours += f"\n   -> question : {self.question},"
        retours += f"\n   -> reponse : {self.reponse},"
        retours += f"\n   -> img : {self.img if self.img else '/'},"
        retours += f"\n   -> niveau : {self.niveau}"
        return retours
