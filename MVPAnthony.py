class Carte:
    def __init__(self, niveau : int = 0, id_carte : int = 0, question : str = "", reponse : str = ""):
        self.niveau = niveau
        self.id_carte = id_carte
        self.question = question
        self.reponse = reponse

    def changer_niveau(self, nouveau_niveau : int):
        self.niveau = nouveau_niveau
        if self.reponse == True:
            nouveau_niveau += 1
        else:
            nouveau_niveau -= 1
            
