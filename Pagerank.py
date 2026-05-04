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


#  PARTIE 2 - PRODUIT VECTEUR * MATRICE CREUSE
# =============================================================
#
#  La matrice P de taille N x N n'est JAMAIS stockee en memoire.
#  On sait juste que :
#
#    P[i][j] = 1 / degre_sortant(i)   si l'arc i->j existe
#    P[i][j] = 0                       sinon
#
#  Donc pour calculer nouveau = x * P :
#
#    nouveau[j] = somme sur i de ( x[i] * P[i][j] )
#               = somme sur i ayant un arc vers j de ( x[i] / degre(i) )
#
#  En pratique on fait ca en parcourant les arcs :
#    pour chaque arc i -> j :
#        nouveau[j] += x[i] / degre(i)
#
#  Complexite : O(M) avec M = nombre d'arcs  (au lieu de O(N^2))

def produit_vecteur_matrice(x, out, n):
    """
    Calcule le produit x * P sans jamais construire P.
    Retourne un nouveau vecteur de taille n.
    """

    resultat = [0.0] * n   # on initialise tout a zero

    for i in range(n):
        d = len(out[i])    # degre sortant de i = nombre de liens sortants

        if d == 0:
            # c'est un "dangling node" (page sans lien sortant)
            # on ne peut pas diviser par 0, on le saute ici
            # sa masse est geree separement dans pagerank()
            continue

        contribution = x[i] / d   # ce que i donne a chacun de ses voisins

        for j in out[i]:           # pour chaque voisin j de i
            resultat[j] += contribution   # j recoit la contribution de i

    return resultat