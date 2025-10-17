import random
import networkx as nx
from copy import deepcopy

def swap_randomization(G, num_trials=1000, copy_graph=True, trace=False):
    """
    Perform edge swaps based on Miklós & Podani trial-swap algorithm 
    Preserves degree sequence and graph simplicity
    """

    if copy_graph:
        G = deepcopy(G)

    edges = list(G.edges())
    n_swaps = 0
    swap_log = []

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
            swap_log.append({
                "old_edges": [(a, b), (c, d)],
                "new_edges": new_edges
            })

            n_swaps += 1
            edges = list(G.edges())

            if trace:
                print(f"Swap #{n_swaps}: {(a,b),(c,d)} → {new_edges}")

    print(f"\nNombre de swaps valides effectués : {n_swaps} / {num_trials}")

    if trace:
        print("\nJournal des swaps :")
        for s in swap_log:
            print(f"  {s['old_edges']} → {s['new_edges']}")

    return G
