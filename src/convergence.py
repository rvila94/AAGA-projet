import numpy as np
import networkx as nx

def run_empirical(G, algo_func, factor=20, copy_graph=True, verbose=False):
    """
    Applies a randomization algorithm (swap or trade)
    for an empirical number of iteration fixed according to Miklós & Podani (2004).

    Ref:
    Miklós & Podani (2004) suggest that the number of trials should be set
    such that the expected number of swaps ≈ 4 × (edges in the graph)
    """

    num_edges = G.number_of_edges()
    num_trials = factor * num_edges

    if verbose:
        print(f"\n=== Convergence empirique ({algo_func.__name__}) ===")
        print(f"- Nombre d'arêtes        : {num_edges}")
        print(f"- Tentatives totales     : {num_trials}")
        print(f"- Objectif swap (temp)   : {4 * num_edges}")

    new_G = algo_func(G, num_trials=num_trials, copy_graph=copy_graph)

    if verbose:
        print(f"=== Fin ===\n")

    return new_G

# Not done 
# FIXME
def run_until_stable(
    G,
    algo_func,
    batch_size=200,
    max_trials=200000,
    window=6,
    tol_rel=1e-3,
    copy_graph=True,
    verbose=True,
):
    """
    Applies a randomization algorithm (swap or trade)
    until the simultaneous stabikization of the follwong indicators:
    - total number of triangles 
    - average clustering
    - size of the largest connected component
    """

    # Historique des indicateurs
    history = {
        "triangles": [],
        "avg_clustering": [],
        "largest_component": [],
    }

    n_trials = 0
    stable_all = False

    if verbose:
        print("=== Suivi de convergence multi-indicateurs ===")
        print(
            f"Mesures suivies : triangles, clustering moyen, taille plus garnde composante connexe\n"
            f"batch_size={batch_size}, tol_rel={tol_rel}, window={window}\n"
        )

    while n_trials < max_trials:
        # Effectuer un bloc d'itérations de l'algo choisi
        G = algo_func(G, num_trials=batch_size, copy_graph=copy_graph)
        n_trials += batch_size

        # Mesure des trois indicateurs
        triangles = sum(nx.triangles(G).values()) // 3
        clustering = nx.average_clustering(G)
        largest_component = len(max(nx.connected_components(G), key=len))

        history["triangles"].append(triangles)
        history["avg_clustering"].append(clustering)
        history["largest_component"].append(largest_component)

        if verbose:
            print(
                f"Après {n_trials:6d} itérations → "
                f"triangles={triangles}, "
                f"clust={clustering:.4f}, "
                f"LCC={largest_component}"
            )

        # Vérifie la stabilisation sur la fenêtre glissante
        stable_all = True
        for key, values in history.items():
            if len(values) < window:
                stable_all = False
                break
            recent = np.array(values[-window:], dtype=float)
            mean = np.mean(recent)
            std = np.std(recent, ddof=0)

            if abs(mean) < 1e-12:
                stable = std < tol_rel
            else:
                stable = (std / abs(mean)) < tol_rel

            if not stable:
                stable_all = False
                break

        if stable_all:
            if verbose:
                print(
                    f"\nConvergence détectée après {n_trials} itérations "
                    f"(toutes les mesures stables sur {window} fenêtres consécutives)."
                )
            break

    if not stable_all and verbose:
        print("\nAucune convergence détectée avant max_trials atteint.")

    return G, history, n_trials