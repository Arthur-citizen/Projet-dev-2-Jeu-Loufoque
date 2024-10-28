questions_rand = ["Pourquoi le ciel est bleu ?", "Pourquoi la Terre est-elle ronde ?", "Où est le Nord ?", "regarde la porte."]
réponse_rand = ["Parce qu'il serai rouge sinon", "Parce que tu crois qu'elle est ronde ?? Ferme le jeu si tu penses que oui!!!"]

def random(min=0, max=10):
    return random.uniform(min, max)
    
def rand_list(list):
    return random.choice(list)
