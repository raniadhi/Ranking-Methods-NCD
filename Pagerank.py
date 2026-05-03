import random
import matplotlib.pyplot as plt

def lire_mtx(nom_fichier):
    """
    Lit un fichier .mtx et retourne le graphe sous forme de liste de listes.
 
    out[i] = liste des pages vers qui la page i a un lien sortant
    Exemple : out[0] = [1, 4, 7] signifie que la page 0 pointe vers 1, 4 et 7.
 
    Pourquoi une liste de listes ?
      - On n'a besoin que des voisins sortants pour calculer x * P.
      - La complexite en memoire est O(M) avec M = nombre d'arcs.
      - Pas besoin de stocker les zeros de la matrice.
    """
 
    n = 0          # nombre de sommets (pages web)
    out = None     # out[i] = voisins sortants de i
 
    with open(nom_fichier, 'r') as f:
        for ligne in f:
 
            # --- on ignore toutes les lignes de commentaire ---
            # les commentaires commencent par '%' dans le format mtx
            if ligne.startswith('%'):
                continue
 
            valeurs = ligne.split()   # decoupe la ligne en mots
 
            # --- premiere ligne non-commentaire = dimensions du graphe ---
            if n == 0:
                n   = int(valeurs[0])   # nombre de sommets
                # valeurs[1] = nb colonnes (pareil que n ici)
                # valeurs[2] = nb arcs total (on n'en a pas besoin)
                out = [[] for _ in range(n)]  # on cree n listes vides
                continue
 
            # --- lignes suivantes = les arcs du graphe ---
            i = int(valeurs[0]) - 1   # source  (on passe en base 0)
            j = int(valeurs[1]) - 1   # cible   (on passe en base 0)
 
            # on ignore les boucles (page qui pointe vers elle-meme)
            # elles n'apportent rien au pagerank et peuvent fausser les degres
            if i != j:
                out[i].append(j)
 
    return n, out 