#from MVP.... import Quizz
#from MVP.... import Flashcard
#from MVP.... import AddQuestion

def main():
    choix = input("""pour commencer le quizz, tapez 'quizz'
                  pour réviser les questions, tapez 'flashcard'
                  pour ajouter une question, tapez 'add'
                  pour quitter, tapez 'exit': """)
    
    if choix.lower() == 'quizz':
        chapitre = input("sur quel chapitre voulez vous vous entrainer ?")
        #new_quizz = Quizz(chapitre)

    elif choix.lower() == 'flashcard':
        chapitre = input("Quel chapitre voulez vous étudier ?")
        #new_flashcard = Flashcard(chapitre)

    elif choix.lower() == 'add':
        chapitre = input("Dans quel chapitre voulez vous ajouter une question ?")
        question = input("Entrez la question que vous souhaitez ajouter : ")
        reponse = input("Entrez la réponse à cette question : ")
        #new_addquestion = AddQuestion(chapitre, question, reponse)

    elif choix.lower() == 'exit':
        pass

    else:
        print("il y a une erreur. veuillez réessayer.")
        main()

main()