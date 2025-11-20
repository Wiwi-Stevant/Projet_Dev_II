#from modules.quiz import Quiz
#from modules.flashCard import FlashCards
#from modules.chapitre import Chapitres

def main():
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
    print("Quel chapitre voulez-vous gérer ?") 
    chap = input()

    if chap == ... : # on regarde si le chapitre existe -- code à compléter quand on aura fini le module chapitre -- !!!!!!!!!!!!!!!!!!!!
        print(f"""Gestion du chapitre : {chap}
            1. Ajouter une carte
            2. Supprimer une carte
            3. Modifier une carte
            4. Afficher les cartes
            5. Retour au menu principal
            :""")
        choix = input()

        if choix == "1":
            pass
        elif choix == "2":
            pass
        elif choix == "3":
            pass
        elif choix == "4":
            pass
        elif choix == "5":
            main()

    else:
        print("voulez-vous créer ce chapitre ? (o/n) :")
        reponse = input()

        if reponse.lower() == "o" or reponse.lower() == "oui" or reponse.lower() == "yes" or reponse.lower() == "y":
            pass

        else:
            gestion_chapitres()

main()