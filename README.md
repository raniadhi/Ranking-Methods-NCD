# Projet PageRank – Sujet 6 : Matrice NCD


Encadrants : Franck Quessette & Sandrine Vial
etudiants : Debbihi Fatiha et Dadoune Ikram

---

## Description

Ce projet étudie le comportement de l'algorithme PageRank lorsque la matrice du graphe du web
est Nearly Completely Decomposable (NCD) et que le paramètre alpha s'approche de 1.

On rend le graphe progressivement NCD en supprimant des arcs aléatoirement (10% puis 20%),
puis on compare la vitesse de convergence par rapport au graphe de base.

---

## Fichiers

```
Ranking-Methods-NCD/
├── Pagerank.py            algorithme PageRank : lecture .mtx, structure creuse, algo
├── ncd.py                 suppression d'arcs, collecte données, tracé des courbes
├── main.py                point d'entrée, lance tout dans l'ordre
├── wb-cs-stanford.mtx     matrice du graphe web (Stanford CS department)
└── README.md
```

---

## Prérequis

Python 3.x et matplotlib :

```
pip install matplotlib
```

---

## Lancer le programme

Mettre tous les fichiers dans le même dossier puis :

```
python main.py
```

---

## Ce que fait le programme

1. Lit le fichier `wb-cs-stanford.mtx` (9914 sommets, 36854 arcs)
2. Crée deux versions NCD du graphe en supprimant 10% puis 20% des arcs
3. Lance PageRank sur les 3 versions avec alpha=0.85 et epsilon=1e-6
4. Fait varier alpha dans {0.5, 0.7, 0.85, 0.9, 0.99} et mesure le nombre d'itérations
5. Génère 4 graphiques PNG

---

## Fichiers générés

```
alpha_compare_3graphes.png   les 3 courbes sur le même graphe
alpha_original.png           graphe original seul
alpha_moins10.png            graphe -10% seul
alpha_moins20.png            graphe -20% seul
```

---

## Paramètre étudié

**alpha** : facteur d'amortissement de PageRank.  
Plus alpha est proche de 1, plus la convergence est lente.  
Sur un graphe NCD cet effet est amplifié car les clusters sont mal connectés.