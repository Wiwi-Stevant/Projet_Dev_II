class Cartes:
    limiter_niveau = lambda self, n: max(0, min(10, n))
    def __init__(self, id, question, reponse, img ,niveau = 4):
        self.id = id
        self.reponse = reponse
        self.question = question
        self.img = img
        self.niveau = niveau # change le niveau d'apparition de la carte
    
    def get_niveau(self):
        return self.niveau
    
    def set_niveau(self, niveau): # en fonction de nos reponses dans les quiz et de si on connait ou pas la carte dans les flashcards on modifie le niveau
        self.niveau = self.limiter_niveau(niveau)

    def connue(self): # on augmente le niveau de la carte
        self.set_niveau(self.niveau + 1)
    
    def pas_connue(self): # on diminue le niveau de la carte
        self.set_niveau(self.niveau - 1)

    def jsonification(self): # on met la carte en json pour la sauvgarde
        return {
            "id": self.id,
            "reponse": self.reponse,
            "question": self.question,
            "img": self.img,
            "niveau": self.niveau
        }
        
    def __str__(self):
        return f"Carte(id={self.id}, question={self.question}, reponse={self.reponse}, img={self.img}, niveau={self.niveau})"