import json

def get_json(precision):
    with open('data/questions.json', 'r') as liste_de_questions:
        if precision == None:
            return json.load(liste_de_questions)
        else:
            return json.load(liste_de_questions[precision])