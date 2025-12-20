def verification_chapitre(chap, chapitres_dict):
    if chap not in chapitres_dict:
        print("Chapitre introuvable.")
        return False
    
    elif not chapitres_dict[chap].cartes:
        print("Le chapitre ne contient aucune carte.")
        return False
    
    else:
        return True