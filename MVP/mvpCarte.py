import random

class Carte:
    def __init__(self, carte_id : int = 0, question : str = "", reponse : str = "", image = None):
        self._niveau = 0
        self._carte_id = carte_id
        self._question = question
        self._reponse = reponse
        self._image = image

    @property
    def carte_id(self):
        return self._carte_id
    
    @property
    def question(self):
        return self._question
    
    @question.setter
    def question(self, valeur):
        self._question = valeur
    
    @property
    def reponse(self):
        return self._reponse
    
    @reponse.setter
    def reponse(self, valeur):
        self._reponse = valeur

    @property
    def niveau(self):
        return self._niveau
    

    def connue(self):
        self._niveau += 1

    def pas_connue(self):
        self._niveau = max(0, self._niveau - 1)