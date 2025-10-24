import random
import numpy as np
import networkx as nx
from copy import deepcopy

def swap_randomization_matrix(A, num_trials=1000, directed=True, copy_matrix=True, verbose=False):
    """
    Perform edge swaps on an adjacency matrix (0/1) following
    Miklós & Podani (2004) trial-swap algorithm.
    """

    if copy_matrix:
        A = A.copy()

    n_swaps = 0
    swap_history = []

    edges = [tuple(e) for e in np.argwhere(A == 1)]
    edge_set = set(edges)

    for _ in range(num_trials):
        if len(edges) < 2:
            break

        # Sélectionne deux arêtes distinctes
        e1, e2 = random.sample(list(edges), 2)
        a, b = e1
        c, d = e2

        # Évite les sommets en commun (a,b,c,d distincts)
        if len({a, b, c, d}) < 4:
            continue

        # Choisit l'un des deux schémas de swap
        if random.random() < 0.5:
            new_edges = [(a, d), (c, b)]
        else:
            new_edges = [(a, c), (b, d)]

        # Vérifie la validité : pas de boucle ni d’arête déjà existante
        if any(x == y or (x, y) in edge_set for x, y in new_edges):
            continue

        # Effectue le swap
        A[a, b] = 0
        A[c, d] = 0
        for x, y in new_edges:
            A[x, y] = 1

        # Si graphe non orienté : enforce symétrie
        if not directed:
            A[b, a] = A[a, b]
            A[d, c] = A[c, d]
            A[new_edges[0][1], new_edges[0][0]] = 1
            A[new_edges[1][1], new_edges[1][0]] = 1

        # Met à jour les arêtes
        for e in [(a, b), (c, d)]:
            edge_set.remove(e)
            edges.remove(e)
        for e in new_edges:
            edge_set.add(e)
            edges.append(e)
            
        n_swaps += 1

        if verbose:
            print(f"Swap #{n_swaps}: ({a,b}),({c,d}) -> {new_edges}")

            swap_history.append({
                "old_edges": [(a, b), (c, d)],
                "new_edges": new_edges
            })

    print(f"\nNombre de swaps valides effectués : {n_swaps} / {num_trials}")
    return A, n_swaps



def swap_randomization(G, num_trials=1000, copy_graph=True, verbose=False):
    """
    Perform edge swaps based on Miklós & Podani trial-swap algorithm 
    Preserves degree sequence and graph simplicity
    """

    if copy_graph:
        G = deepcopy(G)

    edges = list(G.edges())
    n_swaps = 0
    swap_history = []

    for _ in range(num_trials):
        # Sélection aléatoire de deux arêtes
        (a, b), (c, d) = random.sample(edges, 2)

        # Vérifie que les deux arêtes ne partagent aucun sommet
        if len({a, b, c, d}) < 4:
            continue

        # Choisit aléatoirement l’un des deux schémas de réécriture possibles
        if random.random() < 0.5:
            new_edges = [(a, d), (c, b)]
        else:
            new_edges = [(a, c), (b, d)]

        # Vérifie la validité du swap
        if all(not G.has_edge(*e) and e[0] != e[1] for e in new_edges):
            G.remove_edges_from([(a, b), (c, d)])
            G.add_edges_from(new_edges)

            # Enregistre le swap effectué pour vérification
            swap_history.append({
                "old_edges": [(a, b), (c, d)],
                "new_edges": new_edges
            })

            n_swaps += 1
            edges = list(G.edges())

            if verbose:
                print(f"Swap #{n_swaps}: {(a,b),(c,d)} → {new_edges}")

    print(f"\nNombre de swaps valides effectués : {n_swaps} / {num_trials}")

    if verbose:
        print("\nJournal des swaps :")
        for s in swap_history:
            print(f"  {s['old_edges']} → {s['new_edges']}")

    return G
