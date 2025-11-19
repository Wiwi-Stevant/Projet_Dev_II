import random
#classe Carte
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
    
#classe chapitre

class Chapitre:
    def __init__(self, nom):
        self.nom = nom
        self.cartes = {}

    def cree_cartes(self, carte_id, question, reponse, image = None):
        if carte_id in self.cartes:
            raise ValueError("La carte existe déjà")
        self.cartes[carte_id] = Carte(carte_id, question, reponse, image)
    
    def supprimer_carte(self, carte_id):
        carte = self.cartes.pop(carte_id)
    
    def modifier_carte(self, carte_id, question, reponse):
        if carte_id not in self.cartes:
            raise ValueError("La carte n'existe pas")
        carte = self.cartes[carte_id]
        carte.question = question
        carte.reponse = reponse

#classe Quiz

class Quiz:
    def __init__(self, chapitre):
        self.chapitre = chapitre
        self.score = 0

    def tirer_carte(self):
        cartes = list(self.chapitre.cartes.values())
        poids = []
        for c in cartes:
            poids.append(max(1, 5 - c.niveau))
        return random.choices(cartes, weights=poids, k=1)[0]
    
    def jouer(self):
        print(f"Mode Quiz : {self.chapitre.nom}")
        compteur = 0
        while True:
            carte = self.tirer_carte()
            print(f"Question : {carte.question}")
            reponsee_utilisateur = input("Votre réponse (q pour quitter) : ")
            if reponsee_utilisateur.lower() == "q":
                break
            if reponsee_utilisateur.lower() == carte.reponse.lower():
                print("Bonne réponse !")
                self.score += 1
                carte.connue()
            else:
                print(f"Mauvaise réponse ! La bonne réponse était {carte.reponse}")
                carte.pas_connue()
            compteur += 1
        
        print(f"Votre score est de {self.score} sur {compteur}")

class FlashCards:
    def __init__(self, chapitre):
        self.chapitre = chapitre

    def tirer_carte(self):
        cartes = list(self.chapitre.cartes.values())
        poids = []
        for c in cartes:
            poids.append(max(1, 5 - c.niveau))
        return random.choices(cartes, weights=poids, k=1)[0]

    def jouer(self):
        print(f"Mode FlashCards : {self.chapitre.nom}")

        while True:
            carte = self.tirer_carte()

            print(f"Question : {carte.question}")
            input("Appuyer sur Entrer pour voir la réponse")
            print(f"Réponse : {carte.reponse}")

            choix = input("Connu (c), Pas connu (p), Quitter (q) : ")
            if choix.lower() == "q":
                break
            elif choix.lower() == "c":
                carte.connue()
            elif choix.lower() == "p":
                carte.pas_connue()

chapitre = Chapitre("Maths")
chapitre.cree_cartes(1, "2+2 ?", "4")
chapitre.cree_cartes(2, "3+2 ?", "5")

jeu = input("choix jeu : Q ou F")
if jeu.lower() == "q":
    quiz = Quiz(chapitre)
    quiz.jouer()
elif jeu.lower() == "f":
    flashcards = FlashCards(chapitre)
    flashcards.jouer()