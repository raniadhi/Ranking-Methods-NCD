# Projet PageRank – Sujet 6 : Matrices NCD (Nearly Completely Decomposable)

**M1 Informatique – UVSQ 2025/2026**  
Cours : Ranking et Recommandation — F. Quessette & S. Vial

---

## Description

Ce projet implémente l'algorithme PageRank (version Google / surfer aléatoire) et étudie l'effet des matrices **NCD (Nearly Completely Decomposable)** sur la convergence. Une matrice NCD est un graphe dont on a supprimé aléatoirement une fraction des arcs, simulant un web "dégradé" ou clairsemé.

L'objectif est de comparer le comportement du PageRank sur :
- le graphe original
- le graphe avec 10 % des arcs supprimés aléatoirement
- le graphe avec 20 % des arcs supprimés aléatoirement

---

## Structure du projet

```
Ranking-Methods-NCD/
│
├── Pagerank.py          # Algorithme PageRank + lecteur universel de matrices
├── ncd.py               # Suppression d'arcs, collecte de données, tracé des courbes
├── main.py              # Point d'entrée principal
│
├── test_matrice/
│   ├── petite/          # Petits graphes de test (G101.txt, G10001.txt, ...)
│   └── grande/          # Grandes matrices (wb-cs-stanford.mtx, wikipedia, wb-edu, ...)
│
└── resultats_<nom>/     # Dossier généré automatiquement par matrice
    ├── stats.txt
    ├── precision_iterations_<nom>.png
    ├── precision_temps_<nom>.png
    ├── alpha_compare_3graphes.png
    ├── alpha_compare_temps.png
    ├── alpha_original.png
    ├── alpha_moins10.png
    └── alpha_moins20.png
```

---

## Installation des dépendances

```bash
pip install matplotlib
```

Python 3.8+ requis. Aucune autre dépendance externe.

---

## Utilisation

```bash
python main.py <fichier_matrice>
```

**Exemples :**

```bash
# Petite matrice de test
python main.py test_matrice/petite/G101.txt

# Matrice Stanford
python main.py test_matrice/grande/wb-cs-stanford.mtx

# Wikipedia
python main.py test_matrice/grande/wikipedia-20051105.mtx

# Web éducatif
python main.py test_matrice/grande/wb-edu.mtx
```

Si aucun fichier n'est passé, le programme utilise `wb-cs-stanford.mtx` par défaut.

Tous les résultats (graphes PNG + statistiques) sont sauvegardés automatiquement dans un dossier `resultats_<nom_matrice>/`.

---

## Formats de matrices supportés

Le lecteur universel (`lire_graphe` dans `Pagerank.py`) détecte automatiquement le format :

| Format | Extensions | Particularités gérées |
|--------|-----------|----------------------|
| Matrix Market | `.mtx` | Header `%%MatrixMarket`, `symmetric`, `hermitian`, `pattern` |
| Liste d'arcs | `.txt`, `.edges`, `.dat` | Commentaires `#` ou `%`, base 0 ou base 1 auto-détectée |

Pour les matrices **symétriques**, les arcs inverses sont automatiquement ajoutés.

---

## Algorithme PageRank implémenté

Formule itérative (TD2) :

```
x(0)   = (1/N) · e

x(k+1) = α · x(k) · P  +  [ (1−α)/N  +  α/N · (x(k) · fᵀ) ] · e
```

Où :
- `P` est la matrice stochastique des transitions (jamais construite en mémoire)
- `f[i] = 1` si le sommet `i` est un dangling node (aucun lien sortant), 0 sinon
- `α` est le facteur d'amortissement (damping factor)
- La convergence est testée en norme L1 : `||x(k+1) − x(k)||₁ ≤ ε`

**Complexité par itération :** O(N + M) avec N sommets et M arcs — grâce à la représentation creuse (liste d'adjacence), la matrice P n'est jamais stockée.

---

## Expériences réalisées

### 1. Influence de la précision ε (TD exercice 2.1.5)

Pour `α = 0.85`, on fait varier ε de `10⁻³` à `10⁻⁹` et on mesure :
- le nombre d'itérations jusqu'à convergence
- le temps de convergence en secondes

→ Fichiers générés : `precision_iterations_<nom>.png`, `precision_temps_<nom>.png`

### 2. Influence du facteur α (TD exercice 2.1.6)

Pour `ε = 10⁻⁶`, on fait varier α dans `{0.5, 0.7, 0.85, 0.9, 0.99, 0.999}` sur les 3 graphes (original, −10%, −20%) et on mesure :
- le nombre d'itérations
- le temps de convergence

→ Fichiers générés : `alpha_compare_3graphes.png`, `alpha_compare_temps.png`, `alpha_original.png`, `alpha_moins10.png`, `alpha_moins20.png`

### 3. Effet NCD

Comparaison directe du PageRank entre :
- le graphe original
- le graphe avec 10 % des arcs supprimés aléatoirement (seed fixée à 42)
- le graphe avec 20 % des arcs supprimés aléatoirement

Les suppressions sont faites arc par arc avec probabilité uniforme (`random.random() < taux`).

---

## Fichiers de sortie

Pour chaque matrice, un dossier `resultats_<nom>/` est créé contenant :

| Fichier | Contenu |
|---------|---------|
| `stats.txt` | Statistiques du graphe + résultats PageRank |
| `precision_iterations_<nom>.png` | Nb itérations en fonction de ε |
| `precision_temps_<nom>.png` | Temps de convergence en fonction de ε |
| `alpha_compare_3graphes.png` | Nb itérations vs α pour les 3 graphes |
| `alpha_compare_temps.png` | Temps vs α pour les 3 graphes |
| `alpha_original.png` | Nb itérations vs α — graphe original seul |
| `alpha_moins10.png` | Nb itérations vs α — graphe −10% |
| `alpha_moins20.png` | Nb itérations vs α — graphe −20% |

---

## Détails d'implémentation

### `Pagerank.py`

- `lire_graphe(nom_fichier)` — lecteur universel (`.mtx` ou liste d'arcs)
- `_lire_mtx(nom_fichier)` — lecteur Matrix Market robuste
- `_lire_edgelist(nom_fichier)` — lecteur liste d'arcs avec auto-détection base 0/1
- `produit_vecteur_matrice(x, out, n)` — multiplication creuse x·P en O(M)
- `pagerank(n, out, alpha, epsilon)` — algorithme complet, retourne `(x, k, temps)`
- `compter_arcs(out, n)` — nombre total d'arcs
- `compter_dangling(out, n)` — nombre de dangling nodes
- `top_pages(x, n, k)` — top-k pages par score PageRank

### `ncd.py`

- `supprimer_arcs(out, n, taux)` — suppression aléatoire d'une fraction `taux` des arcs
- `collecter_donnees_alpha(...)` — itérations et temps pour plusieurs valeurs de α
- `tracer_courbes_alpha(...)` — génère les 5 graphes alpha (avec paramètre `dossier`)
- `collecter_et_tracer_precision(...)` — génère les 2 graphes epsilon (itérations + temps)

---

## Remarques

- La graine aléatoire est fixée à `random.seed(42)` pour assurer la reproductibilité des suppressions d'arcs NCD.
- Le backend matplotlib `Agg` est forcé dans `ncd.py` pour garantir la génération correcte des PNG sur tous les OS (Windows, Linux, macOS) sans interface graphique.
- `α = 1.0` n'est pas testé car sans téléportation, PageRank peut ne pas converger sur des graphes avec dangling nodes ou composantes non fortement connexes.