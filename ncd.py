# =============================================================
#  ncd.py
#  Contient tout ce qui est specifique au sujet 6 - Matrice NCD :
#    - suppression aleatoire d'arcs
#    - courbe iterations vs alpha
#    - courbe iterations vs epsilon
#
#  Ce fichier importe pagerank_base pour utiliser l'algorithme.
# =============================================================

import random
import matplotlib.pyplot as plt

# on importe les fonctions du fichier pagerank_base.py
from Pagerank import pagerank, compter_arcs


# =============================================================
#  FONCTION 1 : supprimer des arcs aleatoirement
# =============================================================
#
#  Pour rendre le graphe NCD (Nearly Completely Decomposable),
#  on supprime des arcs au hasard.
#
#  Methode (tirage aleatoire, comme dit dans le sujet) :
#    Pour chaque arc i -> j :
#      - tirer u = random() entre 0 et 1
#      - si u < taux  -> supprimer l'arc
#      - si u >= taux -> garder l'arc
#
#  taux = 0.1 pour supprimer environ 10% des arcs
#  taux = 0.2 pour supprimer environ 20% des arcs
#
#  Les degres sortants sont automatiquement recalcules car on
#  reconstruit entierement la structure : len(out_modifie[i])
#  donne le nouveau degre de i apres suppression.

def supprimer_arcs(out, n, taux):

    out_modifie = [[] for _ in range(n)]   # nouvelle structure, commence vide

    for i in range(n):
        for j in out[i]:               # pour chaque arc existant i -> j

            u = random.random()        # tirage uniforme entre 0 et 1

            if u >= taux:
                # on garde l'arc (cela arrive avec probabilite 1 - taux)
                out_modifie[i].append(j)
            # si u < taux on n'ajoute pas l'arc = il est supprime

    return out_modifie


# =============================================================
#  FONCTION 2 : courbe nombre d'iterations en fonction de alpha
# =============================================================
#
#  On fait varier alpha parmi : 0.5, 0.7, 0.85, 0.9, 0.99, 0.999
#  Pour chacune des 3 versions du graphe :
#    - graphe original
#    - graphe avec 10% des arcs supprimes
#    - graphe avec 20% des arcs supprimes
#  On mesure combien d'iterations sont necessaires pour converger.
#
#  Intuition attendue :
#    Plus alpha est proche de 1, plus on fait confiance aux liens
#    du graphe et moins on teleporte. Sur un graphe NCD, les clusters
#    sont mal relies, donc l'info met longtemps a se propager.
#    => convergence beaucoup plus lente quand alpha est grand.

def courbe_alpha(n, out, out_10, out_20, epsilon=1e-6):

    alphas = [0.5, 0.7, 0.85, 0.9, 0.99, 0.999]

    # on va stocker le nombre d'iterations pour chaque version du graphe
    iters_base = []
    iters_10   = []
    iters_20   = []

    print("\n[courbe alpha] calcul en cours...")

    for a in alphas:
        print(f"  alpha = {a} ...", end=' ', flush=True)

        # on lance pagerank sur les 3 graphes avec ce meme alpha
        _, k_base = pagerank(n, out,    alpha=a, epsilon=epsilon)
        _, k_10   = pagerank(n, out_10, alpha=a, epsilon=epsilon)
        _, k_20   = pagerank(n, out_20, alpha=a, epsilon=epsilon)

        iters_base.append(k_base)
        iters_10.append(k_10)
        iters_20.append(k_20)

        print(f"original={k_base}, -10%={k_10}, -20%={k_20}")

    # --- trace de la courbe ---
    plt.figure(figsize=(9, 5))

    plt.plot(alphas, iters_base, marker='o', linewidth=2, label='graphe original')
    plt.plot(alphas, iters_10,   marker='s', linewidth=2, label='arcs -10%')
    plt.plot(alphas, iters_20,   marker='^', linewidth=2, label='arcs -20%')

    plt.xlabel('alpha')
    plt.ylabel("nombre d'iterations")
    plt.title('Convergence PageRank selon alpha (sujet 6 - NCD)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('courbe_alpha_ncd.png', dpi=150)
    plt.show()

    print("  -> sauvegarde : courbe_alpha_ncd.png")


# =============================================================
#  FONCTION 3 : courbe nombre d'iterations en fonction de epsilon
# =============================================================
#
#  On fixe alpha = 0.85 et on fait varier la precision demandee
#  de 10^-3 a 10^-9 (puissances de 10).
#
#  Intuition attendue :
#    Plus epsilon est petit, plus on exige de precision,
#    donc plus il faut d'iterations.

def courbe_epsilon(n, out, out_10, out_20, alpha=0.85):

    # les valeurs de epsilon a tester : 1e-3, 1e-4, ..., 1e-9
    epsilons     = [10**(-e) for e in range(3, 10)]
    # pour l'axe X du graphe on affiche juste l'exposant : 3, 4, ..., 9
    exposants    = list(range(3, 10))

    iters_base = []
    iters_10   = []
    iters_20   = []

    print("\n[courbe epsilon] calcul en cours...")

    for e, eps in zip(exposants, epsilons):
        print(f"  epsilon = 1e-{e} ...", end=' ', flush=True)

        _, k_base = pagerank(n, out,    alpha=alpha, epsilon=eps)
        _, k_10   = pagerank(n, out_10, alpha=alpha, epsilon=eps)
        _, k_20   = pagerank(n, out_20, alpha=alpha, epsilon=eps)

        iters_base.append(k_base)
        iters_10.append(k_10)
        iters_20.append(k_20)

        print(f"original={k_base}, -10%={k_10}, -20%={k_20}")

    # --- trace de la courbe ---
    plt.figure(figsize=(9, 5))

    plt.plot(exposants, iters_base, marker='o', linewidth=2, label='graphe original')
    plt.plot(exposants, iters_10,   marker='s', linewidth=2, label='arcs -10%')
    plt.plot(exposants, iters_20,   marker='^', linewidth=2, label='arcs -20%')

    plt.xlabel('precision (10^-x)')
    plt.ylabel("nombre d'iterations")
    plt.title(f'Convergence PageRank selon epsilon (alpha={alpha}, sujet 6 - NCD)')
    plt.xticks(exposants, [f'1e-{e}' for e in exposants])
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('courbe_epsilon_ncd.png', dpi=150)
    plt.show()

    print("  -> sauvegarde : courbe_epsilon_ncd.png")