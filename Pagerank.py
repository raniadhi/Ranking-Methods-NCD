import time


#lire le fichier .mtx


def lire_graphe(nom_fichier):
    """
    Lecteur universel : détecte automatiquement le format du fichier.
    Supporte :
      - Matrix Market (.mtx)  : header %%MatrixMarket, symmetric, pattern
      - Liste d'arcs (.txt, .edges, .dat) : commentaires # ou %, base 0 ou 1
    Retourne (n, out) comme lire_mtx.
    """
    ext = nom_fichier.lower()

    if ext.endswith('.mtx'):
        return _lire_mtx(nom_fichier)
    else:
        return _lire_edgelist(nom_fichier)


# ---------------------------------------------------------------
def _lire_mtx(nom_fichier):
    """Lit un fichier Matrix Market robuste (symmetric, pattern, real)."""
    n = 0
    out = None
    is_symmetric = False
    header_done  = False

    with open(nom_fichier, 'r') as f:
        for ligne in f:
            ligne = ligne.strip()

            # bannière %%MatrixMarket
            if ligne.lower().startswith('%%matrixmarket') or \
               ligne.lower().startswith('%matrixmarket'):
                low = ligne.lower()
                is_symmetric = 'symmetric' in low or 'hermitian' in low
                continue

            # autres commentaires
            if ligne.startswith('%') or ligne == '':
                continue

            valeurs = ligne.split()

            # première ligne non-commentaire = dimensions
            if not header_done:
                n   = int(valeurs[0])
                out = [[] for _ in range(n)]
                header_done = True
                continue

            # arc i -> j
            i = int(valeurs[0]) - 1   # base 1 → base 0
            j = int(valeurs[1]) - 1

            if i == j or not (0 <= i < n and 0 <= j < n):
                continue

            out[i].append(j)
            if is_symmetric:
                out[j].append(i)   # arc inverse pour matrices symétriques

    return n, out


# ---------------------------------------------------------------
def _lire_edgelist(nom_fichier):
    """
    Lit une liste d'arcs simple (format .txt, .edges, .dat).
    - Commentaires : lignes commençant par '#' ou '%'
    - Première ligne non-commentaire : peut être "n m" (dimensions)
      OU directement un arc — on détecte automatiquement.
    - Base 0 ou base 1 détectée automatiquement.
    """
    arcs_bruts = []
    n_declare  = None
    min_idx    = float('inf')
    max_idx    = -1

    with open(nom_fichier, 'r') as f:
        for ligne in f:
            ligne = ligne.strip()

            if ligne.startswith('#') or ligne.startswith('%') or ligne == '':
                continue

            valeurs = ligne.split()
            if len(valeurs) < 2:
                continue

            a, b = int(valeurs[0]), int(valeurs[1])

            # heuristique : si la ligne a exactement 2 grands nombres égaux
            # c'est probablement une ligne de dimension "n n" ou "n m"
            if len(valeurs) == 2 and a == b and a > 1000 and not arcs_bruts:
                n_declare = a
                continue

            arcs_bruts.append((a, b))
            min_idx = min(min_idx, a, b)
            max_idx = max(max_idx, a, b)

    # détection base 0 / base 1
    base = 0 if min_idx == 0 else 1

    n = n_declare if n_declare else (max_idx - base + 1)
    out = [[] for _ in range(n)]

    for a, b in arcs_bruts:
        i = a - base
        j = b - base
        if i == j or not (0 <= i < n and 0 <= j < n):
            continue
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
    start = time.perf_counter()  

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
    temps = time.perf_counter() - start 

    return x, k , temps  


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
