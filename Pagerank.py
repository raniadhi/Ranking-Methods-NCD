# =============================================================
#  pagerank_base.py
#  Contient tout ce qui est generique a PageRank :
#    - lecture du fichier .mtx
#    - structure creuse (liste de listes)
#    - produit vecteur * matrice creuse
#    - algorithme PageRank complet
#
#  Ce fichier ne fait rien tout seul, il est importe par les
#  autres fichiers qui l'utilisent.
# =============================================================


# =============================================================
#  FONCTION 1 : lire le fichier .mtx
# =============================================================
#
#  Format du fichier Matrix Market :
#
#    %%MatrixMarket matrix coordinate pattern general
#    % commentaire (on ignore)
#    9914  9914  36854     <- nombre de sommets et d'arcs
#    1  2                  <- arc de la page 1 vers la page 2
#    3  7
#    ...
#
#  Les indices dans le fichier commencent a 1 (convention Fortran).
#  On fait -1 pour passer en base 0 (convention Python).
#
#  On retourne :
#    n   = nombre de sommets
#    out = liste de listes : out[i] = liste des voisins sortants de i

def lire_mtx(nom_fichier):

    n   = 0     # on ne connait pas encore le nombre de sommets
    out = None  # sera une liste de n listes vides

    with open(nom_fichier, 'r') as f:
        for ligne in f:

            # les lignes de commentaire commencent par '%', on les saute
            if ligne.startswith('%'):
                continue

            valeurs = ligne.split()   # decoupe en mots : ['9914', '9914', '36854']

            # premiere ligne non-commentaire = les dimensions du graphe
            if n == 0:
                n   = int(valeurs[0])           # nombre de sommets
                out = [[] for _ in range(n)]    # n listes vides
                continue

            # toutes les lignes suivantes = un arc i -> j
            i = int(valeurs[0]) - 1   # source, on passe en base 0
            j = int(valeurs[1]) - 1   # cible,  on passe en base 0

            # on ignore les boucles (page qui pointe vers elle-meme)
            # elles ne changent pas le pagerank et peuvent fausser les degres
            if i != j:
                out[i].append(j)

    return n, out


# =============================================================
#  FONCTION 2 : produit vecteur * matrice creuse
# =============================================================
#
#  On veut calculer  nouveau = x * P
#  mais on ne construit JAMAIS la matrice P en memoire.
#
#  On sait que :  P[i][j] = 1 / degre_sortant(i)  si l'arc i->j existe
#                P[i][j] = 0                        sinon
#
#  Donc :  nouveau[j] = somme_i ( x[i] * P[i][j] )
#                     = somme des i qui ont un arc vers j de ( x[i] / degre(i) )
#
#  En pratique on parcourt tous les arcs :
#    pour chaque arc i -> j :
#        nouveau[j] += x[i] / degre(i)
#
#  Complexite : O(M) avec M = nombre d'arcs  (et non O(N^2) !)

def produit_vecteur_matrice(x, out, n):

    resultat = [0.0] * n    # initialise a zero partout

    for i in range(n):
        d = len(out[i])     # degre sortant de i = nombre de liens sortants

        if d == 0:
            continue        # dangling node : aucun lien sortant, on saute

        contribution = x[i] / d    # x[i] divise equitablement entre d voisins

        for j in out[i]:           # pour chaque voisin j de i
            resultat[j] += contribution   # j recoit la part de i

    return resultat


# =============================================================
#  FONCTION 3 : algorithme PageRank complet
# =============================================================
#
#  Formule du TD2 :
#
#    x(0)   = (1/N) * e
#    x(k+1) = alpha * x(k) * P
#             + [ (1-alpha)/N  +  alpha/N * somme_dangling(x(k)) ] * e
#
#  Les dangling nodes sont les pages sans lien sortant.
#  Elles "absorbent" de la probabilite sans en redistribuer.
#  On les gere en redistribuant leur masse uniformement sur toutes les pages.
#
#  Parametres :
#    n       : nombre de sommets
#    out     : liste de listes des voisins sortants
#    alpha   : facteur d'amortissement (0.85 par defaut)
#    epsilon : seuil de convergence en norme L1 (1e-6 par defaut)
#
#  Retourne :
#    x : vecteur PageRank final
#    k : nombre d'iterations jusqu'a convergence

def pagerank(n, out, alpha=0.85, epsilon=1e-6):

    # initialisation : distribution uniforme
    # toutes les pages ont la meme importance au depart
    x = [1.0 / n] * n

    # on repere les dangling nodes une seule fois avant la boucle
    # (leur liste ne change pas au cours des iterations)
    dangling = [i for i in range(n) if len(out[i]) == 0]

    k = 0   # compteur d'iterations

    while True:
        k += 1

        # -- etape 1 : masse totale des dangling nodes --
        # c'est la somme des probabilites de toutes les pages sans liens sortants
        # cette masse va etre redistribuee uniformement sur toutes les pages
        masse_dangling = sum(x[i] for i in dangling)

        # -- etape 2 : produit creux x * P --
        # propage la probabilite le long des arcs existants
        # les dangling nodes ne contribuent pas ici (ils ont d=0, skipes dans le produit)
        nouveau = produit_vecteur_matrice(x, out, n)

        # -- etape 3 : ajouter la teleportation --
        # cette valeur est la meme pour toutes les pages (on l'ajoute partout)
        # elle vient de :
        #   - (1-alpha)/N : probabilite de sauter vers une page aleatoire
        #   - alpha * masse_dangling / N : redistribution de la masse des dangling nodes
        teleportation = (alpha * masse_dangling / n) + ((1.0 - alpha) / n)

        for i in range(n):
            nouveau[i] = alpha * nouveau[i] + teleportation

        # -- etape 4 : test de convergence en norme L1 --
        # ||x_nouveau - x_ancien||_1 = somme des valeurs absolues des differences
        # si cette somme est petite, les vecteurs sont presque identiques => converge
        diff = sum(abs(nouveau[i] - x[i]) for i in range(n))

        x = nouveau   # on avance d'une iteration

        if diff <= epsilon:
            break   # converge, on arrete

    return x, k


# =============================================================
#  FONCTIONS UTILITAIRES
# =============================================================

def compter_arcs(out, n):
    """Retourne le nombre total d'arcs dans le graphe."""
    return sum(len(out[i]) for i in range(n))


def compter_dangling(out, n):
    """Retourne le nombre de pages sans lien sortant."""
    return sum(1 for i in range(n) if len(out[i]) == 0)


def top_pages(x, n, k=5):
    """Retourne les indices des k pages avec le PageRank le plus eleve."""
    return sorted(range(n), key=lambda i: -x[i])[:k]