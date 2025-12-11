import os
from modules.flashCard import FlashCards
from modules.quiz import Quiz
from modules.chapitre import Chapitres

confirmation = ["o", "oui", "yes", "y",""]
refus = ["n", "non", "no"]
chapitres_dict = {}  # Dictionnaire pour stocker les chapitres

def charger_chapitres(): # -> chat GPT
    """Charge tous les chapitres existants depuis le dossier data"""
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'data'))
    if os.path.exists(data_dir):
        for fichier in os.listdir(data_dir):
            if fichier.endswith('.json'):
                nom_chap = fichier.replace('.json', '')
                chap = Chapitres(nom_chap)
                chap.charger_cartes()
                chapitres_dict[nom_chap] = chap
        if chapitres_dict:
            print(f"{len(chapitres_dict)} chapitre(s) chargé(s).")
    else:
        print("Le dossier data n'existe pas encore.")

def main():
    print("""\n ===== Menu Principal =====
Bonjour, quel option souhaitez-vous exécuter ?
    => 1. Lancer le quiz
    => 2. Lancer les flashcards
    => 3. Gérer les chapitres
    => 4. Quitter\n""")
    choix = input("Veuillez entrer le numéro de l'option : ").strip()
    print("")

    if choix == "1":
        quizz()
    elif choix == "2":
        flashcards()
    elif choix == "3":
        gestion_chapitres()
    elif choix == "4":
        print("Au revoir !")
    else:
        print("Il y a une erreur.\nVeuillez réessayer.")
        main()

def quizz():
    print("\n ===== Quiz ===== \nQuel chapitre voulez-vous utiliser pour le quiz ?")
    
    for nom in chapitres_dict:
        print(f" => {nom}")

    chap = input("\nVeuillez entrer le nom du chapitre : ").strip()
    print("")

    if chap not in chapitres_dict:
        print("Chapitre introuvable.")
        quizz()

    else:
        quiz = Quiz(chap)
        quiz.jouer()

    main()

def flashcards():
    print("\n ===== Flashcards =====")
    if not chapitres_dict:
        print("Aucun chapitre chargé. Créez d'abord un chapitre dans la gestion des chapitres.")
        return

    print("Choisissez un chapitre pour les flashcards :")
    for nom in chapitres_dict:
        print(f" => {nom}")

    nom_chap = input("\nVeuillez entrer le nom du chapitre : ").strip()
    print("")

    if nom_chap not in chapitres_dict:
        print("Chapitre introuvable.")
        return

    chap = chapitres_dict[nom_chap]

    # Création du gestionnaire FlashCards
    fc = FlashCards(chap)

    print(f"\n[===== {chap.nom} =====]")
    print("Tapez 'q' pour quitter à tout moment.\n")

    while True:
        fc.mettre_a_jour_cartes()  # mettre à jour la liste si des cartes ont été ajoutées/supprimées

        carte = fc.tirer_carte()
        if carte is None:
            print("Aucune carte disponible.")
            break

        print(f"\nQuestion : {carte.question}")
        cmd = input("Voir la réponse : ").strip().lower()
        if cmd == 'q':
            break

        print(f"Réponse : {carte.reponse}")
        if carte.img:
            print(f"Image associée : {carte.img}")

        choix = input("\nCarte suivante ? (o/n) : ").strip().lower()
        if choix not in confirmation:
            break
    main()

def gestion_chapitres():
    print("\n ===== Chapitres =====\nQuel chapitre voulez-vous gérer ?")
    for nom in chapitres_dict:
        print(f" => {nom}")

    nom_chap = input("\nVeuillez entrer le nom du chapitre : ").strip()
    print("")

    if nom_chap in chapitres_dict:
        chap_charger = chapitres_dict[nom_chap]
        menu_chapitre(chap_charger)
    else:
        print("Voulez-vous créer ce chapitre ? (o/n) :")
        reponse = input().strip().lower()
        #print (chapitres_dict)

        if reponse in confirmation:
            chap = Chapitres(nom_chap)
            chapitres_dict[nom_chap] = chap
            menu_chapitre(chap)
        else:
            gestion_chapitres()

def menu_chapitre(chap_charger):
    while True:
        print(f"""\n [===== {chap_charger.nom} =====]
    => 1. Ajouter une carte
    => 2. Supprimer une carte
    => 3. Modifier une carte
    => 4. Afficher les cartes
    => 5. Retour au menu principal\n""")
        choix = input("Veuillez entrer le numéro de l'option : ").strip()
        print("")

        if choix == "1":
            print("\n <== Création d'une nouvelle carte ==>")
            question = input("Entrez la question de la carte : ").strip()
            reponse = input("Entrez la réponse de la carte : ").strip()
            img = input("Entrez le chemin de l'image associée (laisser vide si aucune) : ").strip()
            print(f"""\nVoici les informations de la nouvelle carte :
    => question : {question}
    => réponse : {reponse}
    => image : {img if img else "Aucune"}""")
            confirm = input("\nConfirmez-vous la création de cette carte ? (o/n) : ").strip().lower()
            print("")
            if confirm in confirmation:
                chap_charger.cree_cartes(question, reponse, img)
            else:
                print("Création de la carte annulée.\n")

        elif choix == "2":
            print(" \n <== Suppression d'une carte ==>\nVoici les cartes disponibles :")
            chap_charger.__str__()

            demand_suppression = (int(input("\nEntrez l'ID de la carte à supprimer : ").strip()))
            print("")
            carte = chap_charger.cartes.get(demand_suppression)
            print(f"voulez-vous vraiment supprimer la carte {carte} ? (o/n) :")
            confirm = input().strip().lower()
            if confirm in confirmation:
                chap_charger.supprimer_carte(demand_suppression)
                print("Carte supprimée.\n")
            
            else:
                print("Suppression annulée.\n")

        elif choix == "3":
            print("\n <== Modification d'une carte ==>\nVoici les cartes disponibles :")
            chap_charger.__str__()
            id_modification = int(input("\nEntrez l'ID de la carte à modifier : ").strip())
            print("")
            if id_modification not in chap_charger.cartes:
                print("Carte introuvable.\n")
                continue
            
            confirm = input(f"Voulez-vous modifier la carte {chap_charger.cartes[id_modification]} ? (o/n) : ").strip().lower()
            print("")
            if confirm in confirmation:
                nouvelle_question = input("Nouvelle question : ").strip()
                nouvelle_reponse = input("Nouvelle réponse : ").strip()
                nouvelle_img = input("Nouveau chemin d'image (laisser vide si aucune) : ").strip()
                print(f"""\nVous avez entré :
    => question : {nouvelle_question}
    => réponse : {nouvelle_reponse}
    => image : {nouvelle_img if nouvelle_img else "Aucune"}\n""")
                
                confirm_modif = input("Confirmez-vous les modifications ? (o/n) : ").strip().lower()
                if confirm_modif in confirmation:
                    chap_charger.modifier_carte(id_modification, nouvelle_question, nouvelle_reponse, nouvelle_img)
                    print("Carte modifiée.\n")
                else:
                    print("Modifications annulées.\n")
            else:
                print("Modification annulée.\n")

        elif choix == "4":
            print("\n <== Affichage des cartes ==>")
            chap_charger.__str__()
            print("")
        elif choix == "5":
            main()
            break
        else:
            print("Choix invalide\n")

if __name__ == "__main__":
    charger_chapitres()
    main()