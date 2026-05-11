# =============================================================
#  ncd.py
#  Contient tout ce qui est specifique au sujet 6 - Matrice NCD :
#    - suppression aleatoire d'arcs
#    - courbe iterations vs alpha  (1 combinee + 3 separees)
#    - courbe iterations vs epsilon (1 combinee + 3 separees)
# =============================================================

import random
import matplotlib.pyplot as plt

from Pagerank import pagerank


# =============================================================
#  FONCTION 1 : supprimer des arcs aleatoirement
# =============================================================

def supprimer_arcs(out, n, taux):
    """
    Parcourt tous les arcs du graphe.
    Pour chaque arc, tire un nombre u entre 0 et 1.
    Si u < taux  -> arc supprime.
    Si u >= taux -> arc garde.
    Les nouveaux degres sortants sont recalcules automatiquement
    via len(out_modifie[i]).
    """

    out_modifie = [[] for _ in range(n)]

    for i in range(n):
        for j in out[i]:
            u = random.random()
            if u >= taux:
                out_modifie[i].append(j)

    return out_modifie


# =============================================================
#  FONCTION 2 : collecter les donnees iterations vs alpha
# =============================================================
#
#  On separe la collecte des donnees du trace des graphes
#  pour ne pas repeter les calculs (ils sont longs).
#  On appelle cette fonction une seule fois, elle retourne
#  les listes de resultats, puis on trace autant de graphes
#  qu'on veut sans recalculer.

def collecter_donnees_alpha(n, out, out_10, out_20, epsilon=1e-6):
    """
    Lance PageRank pour chaque valeur d'alpha sur les 3 graphes.
    Retourne : alphas, iters_base, iters_10, iters_20
    """

    alphas = [0.5, 0.7, 0.85, 0.9, 0.99]

    iters_base = []
    iters_10   = []
    iters_20   = []

    print("\n[calcul donnees alpha] ...")

    for a in alphas:
        print(f"  alpha = {a} ...", end=' ', flush=True)

        _, k_base = pagerank(n, out,    alpha=a, epsilon=epsilon)
        _, k_10   = pagerank(n, out_10, alpha=a, epsilon=epsilon)
        _, k_20   = pagerank(n, out_20, alpha=a, epsilon=epsilon)

        iters_base.append(k_base)
        iters_10.append(k_10)
        iters_20.append(k_20)

        print(f"original={k_base}, -10%={k_10}, -20%={k_20}")

    return alphas, iters_base, iters_10, iters_20


# =============================================================
#  FONCTION 3 : tracer les graphes alpha
# =============================================================
#
#  4 graphes au total :
#    - 1 graphe avec les 3 courbes ensemble (vue de comparaison)
#    - 1 graphe original seul
#    - 1 graphe -10% seul
#    - 1 graphe -20% seul

def tracer_courbes_alpha(alphas, iters_base, iters_10, iters_20):

    print("\n[trace graphes alpha]")

    # -------------------------------------------------------
    # graphe 1 : les 3 courbes sur le meme graphe
    # -------------------------------------------------------
    plt.figure(figsize=(9, 5))

    plt.plot(alphas, iters_base, marker='o', linewidth=2, label='graphe original')
    plt.plot(alphas, iters_10,   marker='s', linewidth=2, label='arcs -10%')
    plt.plot(alphas, iters_20,   marker='^', linewidth=2, label='arcs -20%')

    plt.xlabel('alpha')
    plt.ylabel("nombre d'iterations")
    plt.title('Convergence selon alpha — comparaison des 3 graphes')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('alpha_compare_3graphes.png', dpi=150)
    plt.close()
    print("  -> alpha_compare_3graphes.png")

    # -------------------------------------------------------
    # graphe 2 : graphe original seul
    # on annote chaque point avec le nombre exact d'iterations
    # -------------------------------------------------------
    plt.figure(figsize=(8, 5))

    plt.plot(alphas, iters_base, marker='o', linewidth=2, color='steelblue')

    for a, k in zip(alphas, iters_base):
        plt.annotate(str(k), xy=(a, k), textcoords='offset points',
                     xytext=(0, 8), ha='center', fontsize=8)

    plt.xlabel('alpha')
    plt.ylabel("nombre d'iterations")
    plt.title('Convergence selon alpha — graphe original')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('alpha_original.png', dpi=150)
    plt.close()
    print("  -> alpha_original.png")

    # -------------------------------------------------------
    # graphe 3 : graphe -10% seul
    # -------------------------------------------------------
    plt.figure(figsize=(8, 5))

    plt.plot(alphas, iters_10, marker='s', linewidth=2, color='darkorange')

    for a, k in zip(alphas, iters_10):
        plt.annotate(str(k), xy=(a, k), textcoords='offset points',
                     xytext=(0, 8), ha='center', fontsize=8)

    plt.xlabel('alpha')
    plt.ylabel("nombre d'iterations")
    plt.title('Convergence selon alpha — graphe arcs -10%')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('alpha_moins10.png', dpi=150)
    plt.close()
    print("  -> alpha_moins10.png")

    # -------------------------------------------------------
    # graphe 4 : graphe -20% seul
    # -------------------------------------------------------
    plt.figure(figsize=(8, 5))

    plt.plot(alphas, iters_20, marker='^', linewidth=2, color='seagreen')

    for a, k in zip(alphas, iters_20):
        plt.annotate(str(k), xy=(a, k), textcoords='offset points',
                     xytext=(0, 8), ha='center', fontsize=8)

    plt.xlabel('alpha')
    plt.ylabel("nombre d'iterations")
    plt.title('Convergence selon alpha — graphe arcs -20%')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('alpha_moins20.png', dpi=150)
    plt.close()
    print("  -> alpha_moins20.png")


# =============================================================
#  FONCTION 4 : collecter les donnees iterations vs epsilon
# =============================================================

def collecter_donnees_epsilon(n, out, out_10, out_20, alpha=0.85):
    """
    Lance PageRank pour chaque valeur d'epsilon sur les 3 graphes.
    Retourne : exposants, iters_base, iters_10, iters_20
    """

    epsilons  = [10**(-e) for e in range(3, 10)]   # 1e-3 jusqu'a 1e-9
    exposants = list(range(3, 10))                  # [3, 4, 5, 6, 7, 8, 9]

    iters_base = []
    iters_10   = []
    iters_20   = []

    print("\n[calcul donnees epsilon] ...")

    for e, eps in zip(exposants, epsilons):
        print(f"  epsilon = 1e-{e} ...", end=' ', flush=True)

        _, k_base = pagerank(n, out,    alpha=alpha, epsilon=eps)
        _, k_10   = pagerank(n, out_10, alpha=alpha, epsilon=eps)
        _, k_20   = pagerank(n, out_20, alpha=alpha, epsilon=eps)

        iters_base.append(k_base)
        iters_10.append(k_10)
        iters_20.append(k_20)

        print(f"original={k_base}, -10%={k_10}, -20%={k_20}")

    return exposants, iters_base, iters_10, iters_20


# =============================================================
#  FONCTION 5 : tracer les graphes epsilon
# =============================================================

def tracer_courbes_epsilon(exposants, iters_base, iters_10, iters_20, alpha=0.85):

    labels_x = [f'1e-{e}' for e in exposants]   # ['1e-3', '1e-4', ...]

    print("\n[trace graphes epsilon]")

    # -------------------------------------------------------
    # graphe 1 : les 3 courbes ensemble
    # -------------------------------------------------------
    plt.figure(figsize=(9, 5))

    plt.plot(exposants, iters_base, marker='o', linewidth=2, label='graphe original')
    plt.plot(exposants, iters_10,   marker='s', linewidth=2, label='arcs -10%')
    plt.plot(exposants, iters_20,   marker='^', linewidth=2, label='arcs -20%')

    plt.xlabel('precision (epsilon)')
    plt.ylabel("nombre d'iterations")
    plt.title(f'Convergence selon epsilon (alpha={alpha}) — comparaison des 3 graphes')
    plt.xticks(exposants, labels_x)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('epsilon_compare_3graphes.png', dpi=150)
    plt.close()
    print("  -> epsilon_compare_3graphes.png")

    # -------------------------------------------------------
    # graphe 2 : graphe original seul
    # -------------------------------------------------------
    plt.figure(figsize=(8, 5))

    plt.plot(exposants, iters_base, marker='o', linewidth=2, color='steelblue')

    for e, k in zip(exposants, iters_base):
        plt.annotate(str(k), xy=(e, k), textcoords='offset points',
                     xytext=(0, 8), ha='center', fontsize=8)

    plt.xlabel('precision (epsilon)')
    plt.ylabel("nombre d'iterations")
    plt.title(f'Convergence selon epsilon (alpha={alpha}) — graphe original')
    plt.xticks(exposants, labels_x)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('epsilon_original.png', dpi=150)
    plt.close()
    print("  -> epsilon_original.png")

    # -------------------------------------------------------
    # graphe 3 : graphe -10% seul
    # -------------------------------------------------------
    plt.figure(figsize=(8, 5))

    plt.plot(exposants, iters_10, marker='s', linewidth=2, color='darkorange')

    for e, k in zip(exposants, iters_10):
        plt.annotate(str(k), xy=(e, k), textcoords='offset points',
                     xytext=(0, 8), ha='center', fontsize=8)

    plt.xlabel('precision (epsilon)')
    plt.ylabel("nombre d'iterations")
    plt.title(f'Convergence selon epsilon (alpha={alpha}) — graphe arcs -10%')
    plt.xticks(exposants, labels_x)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('epsilon_moins10.png', dpi=150)
    plt.close()
    print("  -> epsilon_moins10.png")

    # -------------------------------------------------------
    # graphe 4 : graphe -20% seul
    # -------------------------------------------------------
    plt.figure(figsize=(8, 5))

    plt.plot(exposants, iters_20, marker='^', linewidth=2, color='seagreen')

    for e, k in zip(exposants, iters_20):
        plt.annotate(str(k), xy=(e, k), textcoords='offset points',
                     xytext=(0, 8), ha='center', fontsize=8)

    plt.xlabel('precision (epsilon)')
    plt.ylabel("nombre d'iterations")
    plt.title(f'Convergence selon epsilon (alpha={alpha}) — graphe arcs -20%')
    plt.xticks(exposants, labels_x)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('epsilon_moins20.png', dpi=150)
    plt.close()
    print("  -> epsilon_moins20.png")