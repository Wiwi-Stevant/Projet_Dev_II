class Carte:
    def __init__(self, niveau : int = 0, id_carte : int = 0, question : str = "", reponse : str = ""):
        self.niveau = niveau
        self.id_carte = id_carte
        self.question = question
        self.reponse = reponse

    @property
    def id_carte(self):
        return self._id_carte
    
    @property
    def reponse(self):
        return self._reponse

    @property
    def question(self):
        return self._question
    
    @question.setter
    def question(self, valeur):
        self._question = valeur

    def changer_niveau(self, nouveau_niveau : int):
        self.niveau = nouveau_niveau
        if self.reponse == True:
            nouveau_niveau += 1
        else:
            nouveau_niveau -= 1
     
        return (self.id_carte, self.niveau) # tuple qui retourne l'id et le niveau actuel de la carte
