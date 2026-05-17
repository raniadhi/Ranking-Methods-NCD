import random
import sys
import os

from Pagerank import lire_graphe, pagerank, compter_arcs, compter_dangling, top_pages
from ncd import supprimer_arcs, collecter_donnees_alpha, tracer_courbes_alpha, collecter_et_tracer_precision


def creer_dossier_resultats(nom_fichier):
    base    = os.path.basename(nom_fichier)       # 'wikipedia-20051105.mtx'
    nom     = os.path.splitext(base)[0]           # 'wikipedia-20051105'
    dossier = f"resultats_{nom}"
    os.makedirs(dossier, exist_ok=True)
    print(f"\nDossier de résultats : {dossier}/")
    return dossier


def main():

    random.seed(42)

    print("=" * 55)
    print("  Projet PageRank - Sujet 6 : Matrice NCD")
    print("  M1 AMIS Informatique - UVSQ 2025/2026")
    print("=" * 55)

    nom_fichier = sys.argv[1] if len(sys.argv) > 1 else 'wb-cs-stanford.mtx'

    # ✅ création du dossier dès le début
    dossier = creer_dossier_resultats(nom_fichier)

    print(f"\nLecture de {nom_fichier} ...")
    n, out = lire_graphe(nom_fichier)

    nb_arcs     = compter_arcs(out, n)
    nb_dangling = compter_dangling(out, n)

    print(f"  Sommets  : {n}")
    print(f"  Arcs     : {nb_arcs}")
    print(f"  Dangling : {nb_dangling} pages sans lien sortant")

    # ✅ sauvegarde stats dans le dossier
    with open(os.path.join(dossier, "stats.txt"), "w") as f:
        f.write(f"Fichier  : {nom_fichier}\n")
        f.write(f"Sommets  : {n}\n")
        f.write(f"Arcs     : {nb_arcs}\n")
        f.write(f"Dangling : {nb_dangling}\n")

    # etape 2 : courbe epsilon (iterations + temps) → dans le dossier
    collecter_et_tracer_precision(n, out, nom_fichier, dossier=dossier)  # ✅ dossier passé

    # etape 3 : création des versions NCD
    print("\nCreation des graphes NCD ...")

    out_10  = supprimer_arcs(out, n, taux=0.1)
    arcs_10 = compter_arcs(out_10, n)
    print(f"  Graphe -10% : {arcs_10} arcs restants  (enleve {nb_arcs - arcs_10})")

    out_20  = supprimer_arcs(out, n, taux=0.2)
    arcs_20 = compter_arcs(out_20, n)
    print(f"  Graphe -20% : {arcs_20} arcs restants  (enleve {nb_arcs - arcs_20})")

    # etape 4 : pagerank sur les 3 versions
    print("\n--- PageRank (alpha=0.85, epsilon=1e-6) ---")

    print("Graphe original ...")
    x_base, k_base, _ = pagerank(n, out,    alpha=0.85, epsilon=1e-6)
    print(f"  Converge en {k_base} iterations")
    print(f"  Top 5 pages : {top_pages(x_base, n, k=5)}")

    print("\nGraphe -10% ...")
    x_10, k_10, _ = pagerank(n, out_10, alpha=0.85, epsilon=1e-6)
    print(f"  Converge en {k_10} iterations")

    print("\nGraphe -20% ...")
    x_20, k_20, _ = pagerank(n, out_20, alpha=0.85, epsilon=1e-6)
    print(f"  Converge en {k_20} iterations")

    print("\nComparaison :")
    print(f"  original : {k_base} iterations")
    print(f"  -10%     : {k_10}  iterations  (delta = {k_10 - k_base:+d})")
    print(f"  -20%     : {k_20}  iterations  (delta = {k_20 - k_base:+d})")

    # ✅ sauvegarde résultats pagerank
    with open(os.path.join(dossier, "stats.txt"), "a") as f:
        f.write(f"\n--- PageRank alpha=0.85, epsilon=1e-6 ---\n")
        f.write(f"Original : {k_base} iterations\n")
        f.write(f"-10%     : {k_10} iterations\n")
        f.write(f"-20%     : {k_20} iterations\n")
        f.write(f"Top 5    : {top_pages(x_base, n, k=5)}\n")

    # etape 5 : courbes alpha → dans le dossier
    alphas, iters_base, iters_10, iters_20, temps_base, temps_10, temps_20 = \
        collecter_donnees_alpha(n, out, out_10, out_20, epsilon=1e-6)

    tracer_courbes_alpha(alphas, iters_base, iters_10, iters_20,
                         temps_base, temps_10, temps_20,
                         dossier=dossier)  # ✅ dossier passé

    print(f"\nTerminé ! Tous les fichiers sont dans : {dossier}/")


if __name__ == '__main__':
    main()