# =============================================================
#  main.py
#  Point d'entree du projet - Sujet 6 : Matrice NCD
#
#  Pour lancer :  python main.py
#  Fichiers requis dans le meme dossier :
#    - Pagerank.py
#    - ncd.py
#    - wb-cs-stanford.mtx
# =============================================================

import random

from Pagerank import lire_mtx, pagerank, compter_arcs, compter_dangling, top_pages
from ncd import supprimer_arcs, collecter_donnees_alpha, tracer_courbes_alpha


def main():

    random.seed(42)

    print("=" * 55)
    print("  Projet PageRank - Sujet 6 : Matrice NCD")
    print("  M1 AMIS Informatique - UVSQ 2025/2026")
    print("=" * 55)

    # ----------------------------------------------------------
    # etape 1 : lecture du graphe
    # ----------------------------------------------------------
    nom_fichier = 'wb-cs-stanford.mtx'
    print(f"\nLecture de {nom_fichier} ...")

    n, out = lire_mtx(nom_fichier)

    nb_arcs     = compter_arcs(out, n)
    nb_dangling = compter_dangling(out, n)

    print(f"  Sommets  : {n}")
    print(f"  Arcs     : {nb_arcs}")
    print(f"  Dangling : {nb_dangling} pages sans lien sortant")

    # ----------------------------------------------------------
    # etape 2 : creation des versions NCD
    # ----------------------------------------------------------
    print("\nCreation des graphes NCD ...")

    out_10 = supprimer_arcs(out, n, taux=0.1)
    arcs_10 = compter_arcs(out_10, n)
    print(f"  Graphe -10% : {arcs_10} arcs restants  (enleve {nb_arcs - arcs_10})")

    out_20 = supprimer_arcs(out, n, taux=0.2)
    arcs_20 = compter_arcs(out_20, n)
    print(f"  Graphe -20% : {arcs_20} arcs restants  (enleve {nb_arcs - arcs_20})")

    # ----------------------------------------------------------
    # etape 3 : pagerank sur les 3 versions (alpha=0.85)
    # ----------------------------------------------------------
    print("\n--- PageRank (alpha=0.85, epsilon=1e-6) ---")

    print("Graphe original ...")
    x_base, k_base = pagerank(n, out, alpha=0.85, epsilon=1e-6)
    print(f"  Converge en {k_base} iterations")
    print(f"  Top 5 pages : {top_pages(x_base, n, k=5)}")

    print("\nGraphe -10% ...")
    x_10, k_10 = pagerank(n, out_10, alpha=0.85, epsilon=1e-6)
    print(f"  Converge en {k_10} iterations")

    print("\nGraphe -20% ...")
    x_20, k_20 = pagerank(n, out_20, alpha=0.85, epsilon=1e-6)
    print(f"  Converge en {k_20} iterations")

    print("\nComparaison :")
    print(f"  original : {k_base} iterations")
    print(f"  -10%     : {k_10}  iterations  (delta = {k_10 - k_base:+d})")
    print(f"  -20%     : {k_20}  iterations  (delta = {k_20 - k_base:+d})")

    # ----------------------------------------------------------
    # etape 4 : courbes alpha (collecte puis trace)
    # ----------------------------------------------------------
    alphas, iters_base, iters_10, iters_20 = collecter_donnees_alpha(
        n, out, out_10, out_20, epsilon=1e-6
    )
    tracer_courbes_alpha(alphas, iters_base, iters_10, iters_20)

    print("\nTermine ! Fichiers PNG generes :")
    print("  alpha_compare_3graphes.png")
    print("  alpha_original.png")
    print("  alpha_moins10.png")
    print("  alpha_moins20.png")


if __name__ == '__main__':
    main()