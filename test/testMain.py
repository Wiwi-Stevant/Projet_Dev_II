import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # code donné par AI pour reconnaitre les modules

#from modules.quiz import Quiz
#from modules.flashCard import FlashCards
from modules.chapitre import Chapitres

confirmation = ["o", "oui", "yes", "y"]
refus = ["n", "non", "no"]    
    
def main():#fonction principale -> choix de l'action
    print("""Bonjour, quel option souhaitez-vous exécuter ?
          1. Lancer le quiz
          2. Lancer les flashcards
          3. Gérer les chapitres
          4. Quitter
           :""")
    choix = input()

    if choix == "1":
        quizz()

    elif choix == "2":
        flashcards()

    elif choix == "3":
        gestion_chapitres()

    elif choix == "4":
        print("Au revoir !")

    else:
        print ("il y a une erreur.")
        main()

def quizz():
    pass

def flashcards():
    pass

def gestion_chapitres():
    print("Quel chapitre voulez-vous gérer ?") #selection du chap
    chap = input()

    if chap == ... : # on regarde si le chapitre existe -- code à compléter quand on aura fini le module chapitre -- !!!!!!!!!!!!!!!!!!!!
        chap_charger = chap.Chapitres.changer_cartes()
        while True:
            print(f"""Gestion du chapitre : {chap}
                1. Ajouter une carte
                2. Supprimer une carte
                3. Modifier une carte
                4. Afficher les cartes
                5. Retour au menu principal
                :""")
            choix = input()

            if choix == "1":
                question = input("Entrez la question de la carte : ")
                reponse = input("Entrez la réponse de la carte : ")
                img = input("Entrez le chemin de l'image associée (laisser vide si aucune) : ")
                confirm = input(f"""Confirmez-vous la création de cette carte  ? 
                                question : {question}
                                réponse : {reponse}
                                image : {img if img else "Aucune"}
                                (o/n) : """)
                if confirm.lower() in confirmation:
                    chap_charger.cree_cartes(... , question, reponse, img)
                else:
                    print("Création de la carte annulée.")

            elif choix == "2":
                pass
            elif choix == "3":
                pass
            elif choix == "4":
                chap.Chapitres.__str__()
                
            elif choix == "5":
                break

        main()

    else:
        print("voulez-vous créer ce chapitre ? (o/n) :")#on demande si on veut cree le chap car le nom n'existe pas
        reponse = input()

        if reponse.lower() in confirmation:
            chap = Chapitres(... , chap)

        else:
            gestion_chapitres()

main()