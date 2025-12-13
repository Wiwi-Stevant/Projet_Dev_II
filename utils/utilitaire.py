#import json

#def get_json(precision):
#    with open('data/questions.json', 'r') as liste_de_questions:
#        if precision == None:
#            return json.load(liste_de_questions)
#        else:
#            return json.load(liste_de_questions[precision])

def verification_chapitre(chap, chapitres_dict):
    if chap not in chapitres_dict:
        print("Chapitre introuvable.")
        return False
    
    elif not chapitres_dict[chap].cartes:
        print("Le chapitre ne contient aucune carte.")
        return False
    
    else:
        return True