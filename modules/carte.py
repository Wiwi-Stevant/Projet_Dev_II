class Cartes:
    def __init__(self, id, reponse, question, img ,niveau = 4):
        self.id = id
        self.reponse = reponse
        self.question = question
        self.img = img
        self.niveau = niveau
    
    def set_niveau(self, niveau):
        self.niveau = niveau

    def jsonification(self):
        return {
            "id": self.id,
            "reponse": self.reponse,
            "question": self.question,
            "img": self.img,
            "niveau": self.niveau
        }
    
    @staticmethod
    def cree_carte_depuis_json(data):
        return Cartes(
            id=data["id"],
            reponse=data["reponse"],
            question=data["question"],
            img=data["img"],
            niveau=data["niveau"]
        )
    
    def __str__(self):
        return f"Carte(id={self.id}, question={self.question}, reponse={self.reponse}, img={self.img}, niveau={self.niveau})"