import random
import numpy as np
import networkx as nx
from copy import deepcopy

def swap_randomization(G, num_trials=1000, copy_graph=True, verbose=False):
    """
    Perform edge swaps based on Miklós & Podani trial-swap algorithm.
    Preserves degree sequence and graph simplicity.
    """

    # --- Copier le graphe si demandé ---
    if copy_graph:
        G = G.copy()

    # Liste des arêtes (sera mise à jour localement)
    edges = list(G.edges())
    edge_set = set(edges)      # pour les tests rapides

    n_swaps = 0
    swap_history = []

    for _ in range(num_trials):

        # Si moins de 2 arêtes → impossible de faire un swap
        if len(edges) < 2:
            break

        # Choisir 2 arêtes distinctes
        (a, b), (c, d) = random.sample(edges, 2)

        # Vérifie qu'elles ne partagent pas de sommet
        if len({a, b, c, d}) < 4:
            continue

        # Choix aléatoire du schéma de réécriture
        if random.random() < 0.5:
            new_edges = [(a, d), (c, b)]
        else:
            new_edges = [(a, c), (b, d)]

        # Vérification de validité : pas de boucle, pas d’arête existante
        valid = True
        for u, v in new_edges:
            if u == v or (u, v) in edge_set or (v, u) in edge_set:
                valid = False
                break

        if not valid:
            continue

        # --- APPLIQUER LE SWAP ---
        G.remove_edge(a, b)
        G.remove_edge(c, d)
        G.add_edges_from(new_edges)

        # Mise à jour locale des structures
        edge_set.discard((a, b))
        edge_set.discard((b, a))
        edge_set.discard((c, d))
        edge_set.discard((d, c))

        edges.remove((a, b))
        edges.remove((c, d))

        for u, v in new_edges:
            edges.append((u, v))
            edge_set.add((u, v))

        # Historique du swap
        if verbose:
            print(f"Swap #{n_swaps+1}: {(a,b),(c,d)} → {new_edges}")

        swap_history.append({
            "old_edges": [(a, b), (c, d)],
            "new_edges": new_edges
        })

        n_swaps += 1

    # --- Affichage final ---
    if verbose:
        print(f"\nNombre de swaps valides effectués : {n_swaps} / {num_trials}")
        print("\nJournal des swaps :")
        for s in swap_history:
            print(f"  {s['old_edges']} → {s['new_edges']}")

    return G