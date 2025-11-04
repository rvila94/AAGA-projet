# Génération de graphes uniformément aléatoires — Swap vs Trade

## Structure du projet

```bash
src/
├── convergence.py     # Gestion des critères et suivi de convergence
├── graph_util.py      # Fonctions utilitaires
├── main.py            # Point d'entrée principal (tests et exécutions)
├── swap_algo.py       # Implémentation de l'algorithme de swap
└── trade_algo.py      # Implémentation de l'algorithme de trade
```

## Fichiers

### `graph_util.py`

Regroupe des fonctions utilitaires utilisées dans tout le projet, telles que `degree_sequence(G)` qui retourne la séquence des degrés du graphe G sous forme de liste.
Mais aussi les fonctions qui nous servent de visualiser la convergence des indicateurs: `plot_convergence(history, title)` et `plot_convergence_tail(history, k, title)`

Ce fichier a un rôle de support et ne contient pas de logique algorithmique principale.

---

### `swap_algo.py` et `trade_algo.py`

Ces deux modules implémentent respectivement les **algorithmes de Swap et Trade** qui permettent de générer des graphes uniformément aléatoires tout en préservant la séquence des degrés.<br><br>

`swap_randomization(G, num_trials, copy_graph, verbose)`:

Implémente l'algorithme de trial-swap (Miklós & Podani, 2004).  
 Il sélectionne deux arêtes aléatoires (a,b) et (c,d) et tente d'échanger leurs extrémités selon l'un des deux schémas possibles :  
 (a,b),(c,d) → (a,d),(c,b) ou (a,c),(b,d).

Les swaps sont acceptés uniquement si le graphe reste simple (pas de boucles ni d'arêtes multiples).<br><br>

`trade_randomization(G, num_trials, copy_graph, verbose)` :

<!-- TODO: détailler l'algorithme de trade et éventuellement changer le nom de la fonction -->

<br><br>
Ces deux méthodes seront comparées expérimentalement selon leurs performances et leur vitesse de convergence.

---

### `convergence.py`

Regroupe les fonctions d'évaluation de la convergence des algorithmes de randomisation.

`run_empirical(G, algo_func, factor, copy_graph, verbose)` :  
Méthode de convergence empirique, inspirée de Miklós & Podani (2004).

Elle fixe un nombre de tentatives proportionnel au nombre d'arêtes :

> "We suggest that the number of trials should be set such that the expected number of swaps equals twice the number of 1's in the matrix"

**Paramètres :**

- `G` : graphe d'entrée
- `algo_func` : fonction de randomisation à appliquer (`swap_randomization` ou `trade_randomization`)
- `factor` : coefficient multiplicateur du nombre d'arêtes (num_trials = factor × edges)
- `copy_graph` : si True, l'algorithme travaille sur une copie de G
- `verbose` : si True, affiche les informations détaillées pendant l'exécution

Cette approche est simple et rapide, mais ne garantit pas une convergence réelle.
<br><br><br>

`run_until_stable(G, algo_func, batch_size, max_trials, window, tol_rel, copy_graph, verbose)` :  
Exécute l'algorithme de randomisation jusqu'à ce que plusieurs indicateurs structurels du graphe se stabilisent.

**Indicateurs surveillés :**

1. Nombre total de triangles
2. Clustering moyen
3. Taille de la plus grande composante connexe

**Principe :**  
Après chaque bloc (`batch_size`) d'itérations :

- Les trois indicateurs sont calculés et ajoutés à l'historique
- Une fenêtre glissante de taille `window` évalue leur stabilité : si la variation relative (std/mean) reste < `tol_rel` pour tous les indicateurs, la convergence est atteinte

**Paramètres :**

- `G` : graphe d'entrée
- `algo_func` : fonction de randomisation à appliquer (`swap_randomization` ou `trade_randomization`)
- `batch_size` : nombre d'essais entre chaque mesure
- `max_trials` : limite totale d'itérations avant arrêt forcé
- `window` : taille de la fenêtre d'observation
- `tol_rel` : tolérance relative pour juger la stabilisation

---

### `main.py`

Ce fichier constitue le point d'entrée du projet.
Il orchestre l’exécution, la comparaison et l’analyse de la convergence des deux algorithmes :
swap_randomization et undirected_curveball (trade).
<br>

**Rôle général**:

- Génère différents graphes de test.
- Applique les algorithmes de randomisation sur chaque graphe.
- Mesure la convergence selon plusieurs indicateurs structurels.
- Compare les performances (temps, stabilité, nombre d’itérations).
- Peut afficher des graphiques de convergence pour une analyse visuelle.
  <br><br>

**Fonctionnement principal**:  
L’exécution se fait via la fonction `main()`, qui:

1. Lit les arguments de ligne de commande

   - `--runs R` : avec R le nombre de répétitions indépendantes de chaque algorithme (par défaut 5).
   - `--verbose` : active l’affichage détaillé du déroulement
   - `--plot` : active les graphiques de convergence pour visualiser graphiquement
   - `--h` ou `--help` : affiche le message d'aide avec les options disponibles

2. Sélectionne la liste d’algorithmes à comparer (`swap_randomization`, `undirected_curveball`)

3. Génère plusieurs graphes de test via `generate_test_graphs()`

4. Exécute chaque algorithme plusieurs fois sur chaque graphe
   (nombre défini par `--runs`)

5. Affiche un résumé clair et comparatif pour chaque graphe testé.
   <br><br>

**Exemples d’utilisation**:

Exécution simple:

```bash
python main.py
```

<br>

Exécution avec 10 répétitions:

```bash
python main.py --runs 10
```

<br>

Exécution avec affichage des graphiques de convergence:

```bash
python main.py --plot
```

<br>

Exécution en mode verbeux (affiche les détails de chaque itération):

```bash
python main.py --verbose
```

<br>

Exécution complète (tout activé) :

```bash
python main.py --runs 10 --verbose --plot
```
