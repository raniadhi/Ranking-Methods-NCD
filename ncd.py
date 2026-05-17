import os
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from Pagerank import pagerank


def supprimer_arcs(out, n, taux):
    out_modifie = [[] for _ in range(n)]
    for i in range(n):
        for j in out[i]:
            if random.random() >= taux:
                out_modifie[i].append(j)
    return out_modifie


def collecter_donnees_alpha(n, out, out_10, out_20, epsilon=1e-6):

    alphas     = [0.5, 0.7, 0.85, 0.9, 0.99, 0.999]
    iters_base = []
    iters_10   = []
    iters_20   = []
    temps_base = []
    temps_10   = []
    temps_20   = []

    print("\n[calcul donnees alpha] ...")

    for a in alphas:
        print(f"  alpha = {a} ...", end=' ', flush=True)
        _, k_base, t_base = pagerank(n, out,    alpha=a, epsilon=epsilon)
        _, k_10,   t_10   = pagerank(n, out_10, alpha=a, epsilon=epsilon)
        _, k_20,   t_20   = pagerank(n, out_20, alpha=a, epsilon=epsilon)

        iters_base.append(k_base)
        iters_10.append(k_10)
        iters_20.append(k_20)
        temps_base.append(t_base)
        temps_10.append(t_10)
        temps_20.append(t_20)
        print(f"original={k_base}, -10%={k_10}, -20%={k_20}")

    return alphas, iters_base, iters_10, iters_20, temps_base, temps_10, temps_20


def tracer_courbes_alpha(alphas, iters_base, iters_10, iters_20,
                         temps_base, temps_10, temps_20, dossier="."):

    print("\n[trace graphes alpha]")

    # graphe 1 : itérations — 3 courbes ensemble
    plt.figure(figsize=(9, 5))
    plt.plot(alphas, iters_base, marker='o', linewidth=2, label='graphe original')
    plt.plot(alphas, iters_10,   marker='s', linewidth=2, label='arcs -10%')
    plt.plot(alphas, iters_20,   marker='^', linewidth=2, label='arcs -20%')
    plt.xlabel('alpha')
    plt.ylabel("nombre d'iterations")
    plt.title('Convergence selon alpha -- comparaison des 3 graphes')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(dossier, 'alpha_compare_3graphes.png'), dpi=150)
    plt.close()
    print("  -> alpha_compare_3graphes.png")

    # graphe 2 : temps — 3 courbes ensemble
    plt.figure(figsize=(9, 6))
    plt.plot(alphas, temps_base, marker='o', linewidth=2, label='graphe original')
    plt.plot(alphas, temps_10,   marker='s', linewidth=2, label='arcs -10%')
    plt.plot(alphas, temps_20,   marker='^', linewidth=2, label='arcs -20%')
    plt.xlabel('alpha')
    plt.ylabel("temps de convergence (secondes)")
    plt.title('Temps de convergence selon alpha -- comparaison des 3 graphes')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(dossier, 'alpha_compare_temps.png'), dpi=150)
    plt.close()
    print("  -> alpha_compare_temps.png")

    # graphe 3 : original seul
    plt.figure(figsize=(8, 5))
    plt.plot(alphas, iters_base, marker='o', linewidth=2, color='steelblue')
    for a, k in zip(alphas, iters_base):
        plt.annotate(str(k), xy=(a, k), textcoords='offset points',
                     xytext=(0, 8), ha='center', fontsize=8)
    plt.xlabel('alpha')
    plt.ylabel("nombre d'iterations")
    plt.title('Convergence selon alpha -- graphe original')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(dossier, 'alpha_original.png'), dpi=150)
    plt.close()
    print("  -> alpha_original.png")

    # graphe 4 : -10% seul
    plt.figure(figsize=(8, 5))
    plt.plot(alphas, iters_10, marker='s', linewidth=2, color='darkorange')
    for a, k in zip(alphas, iters_10):
        plt.annotate(str(k), xy=(a, k), textcoords='offset points',
                     xytext=(0, 8), ha='center', fontsize=8)
    plt.xlabel('alpha')
    plt.ylabel("nombre d'iterations")
    plt.title('Convergence selon alpha -- graphe arcs -10%')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(dossier, 'alpha_moins10.png'), dpi=150)
    plt.close()
    print("  -> alpha_moins10.png")

    # graphe 5 : -20% seul
    plt.figure(figsize=(8, 5))
    plt.plot(alphas, iters_20, marker='^', linewidth=2, color='seagreen')
    for a, k in zip(alphas, iters_20):
        plt.annotate(str(k), xy=(a, k), textcoords='offset points',
                     xytext=(0, 8), ha='center', fontsize=8)
    plt.xlabel('alpha')
    plt.ylabel("nombre d'iterations")
    plt.title('Convergence selon alpha -- graphe arcs -20%')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(dossier, 'alpha_moins20.png'), dpi=150)
    plt.close()
    print("  -> alpha_moins20.png")


def collecter_et_tracer_precision(n, out, nom_matrice, dossier="."):
    print(f"\n[Calcul precision pour {nom_matrice}] (Question 2.1.5 du TD) ...")

    precisions = [10**(-i) for i in range(3, 10)]
    iterations = []
    temps      = []

    for eps in precisions:
        _, k, t = pagerank(n, out, alpha=0.85, epsilon=eps)
        iterations.append(k)
        temps.append(t)
        print(f"  Epsilon = {eps:.1e} -> {k} iterations, {t:.3f}s")

    nom_base = os.path.splitext(os.path.basename(nom_matrice))[0]

    # courbe 1 : itérations
    plt.figure(figsize=(9, 5))
    plt.plot(precisions, iterations, marker='o', color='purple', linewidth=2)
    for eps, k in zip(precisions, iterations):
        plt.annotate(str(k), xy=(eps, k), textcoords='offset points',
                     xytext=(0, 8), ha='center', fontsize=8)
    plt.xscale('log')
    plt.gca().invert_xaxis()
    plt.xlabel('Précision ε')
    plt.ylabel("Nombre d'itérations")
    plt.title(f'Itérations selon ε — {nom_base}')
    plt.grid(True, which='both', linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(dossier, f'precision_iterations_{nom_base}.png'), dpi=150)
    plt.close()
    print(f"  -> precision_iterations_{nom_base}.png")

    # courbe 2 : temps
    plt.figure(figsize=(9, 5))
    plt.plot(precisions, temps, marker='s', color='darkorange', linewidth=2)
    for eps, t in zip(precisions, temps):
        plt.annotate(f'{t:.2f}s', xy=(eps, t), textcoords='offset points',
                     xytext=(0, 8), ha='center', fontsize=8)
    plt.xscale('log')
    plt.gca().invert_xaxis()
    plt.xlabel('Précision ε')
    plt.ylabel('Temps de convergence (secondes)')
    plt.title(f'Temps de convergence selon ε — {nom_base}')
    plt.grid(True, which='both', linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(dossier, f'precision_temps_{nom_base}.png'), dpi=150)
    plt.close()
    print(f"  -> precision_temps_{nom_base}.png")