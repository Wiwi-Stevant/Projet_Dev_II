import json
#from ..utils.utilitaire import get_json

with open('data/questions.json', 'r') as liste_de_questions:
    questions = json.load(liste_de_questions) #on met toutes les question du json dans questions

def quizz():
    score = 0

    for i in questions:
        print(questions[i]["question"]) #on affiche les question dans l'ordre
        reponse = input("entrer la reponse: ")

        if reponse.lower() == questions[i]["answer"].lower(): #on met tt en minuscule et on compare a la reponse du json
            print("Bonne reponse!")
            score += 1

        else:
            print(f"mauvaise reponse, la bonne reponse était: {questions[i]['answer']}")

    print(f"vous avez eu : {score}/{len(questions)}") # on met le score et le nombre de question du json
    main()

def flashcard():
    for i in questions: #on affiche les question et on donne les differente option
        print("""Appuyez sur Entrée pour voir la réponse.
                tapez 'next' pour passer à la question suivante.
                tapez 'exit' pour quitter les flashcards.
            """)
        while True: # boucle pour si on veux revoir la reponse ou la question
            print(f"Question: {questions[i]['question']}")

            next = input(" :") # on attend la reponse et on 

            if next.lower() == 'exit':
                return main()
            
            elif next.lower() == 'next':
                break

            elif next == '':
                print(f"reponse: {questions[i]['answer']}\n")
    main()

def main():# ----------------------------------------FONCTION PRINCIPALE---------------------------------------------
    choix = input("""pour commencer le quizz, tapez 'quizz'
                  pour réviser les questions, tapez 'flashcard'
                  pour quitter, tapez 'exit': """)
    
    if choix.lower() == 'quizz':
        quizz()

    elif choix.lower() == 'flashcard':
        flashcard()

    elif choix.lower() == 'exit':
        pass

    else:
        print("il y a une erreur. veuillez réessayer.")
        main()

main()