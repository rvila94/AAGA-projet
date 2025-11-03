from graph_utils import generate_graph, plot_graph, degree_sequence
from swap_algo import swap_randomization
from trade_algo import curveball, undirected_curveball
from convergence import run_empirical, run_until_stable
import networkx as nx
import numpy as np
import time


def test_randomization_convergence(
    G,
    algo_func,
    batch_size=500,
    max_trials=1_000_000,
    window=6,
    tol_rel=1e-3,
    copy_graph=True,
    verbose=True,
    plot=False,
):
    """
    Teste la convergence d'un algorithme de randomisation (swap ou trade) sur un graphe donné.
    """

    algo_name = algo_func.__name__

    if verbose:
        print(f"\n=== Test de convergence ({algo_name}) ===")
        print(f"Graphe : {G.number_of_nodes()} sommets, {G.number_of_edges()} arêtes\n")

    # --- Vérification de la séquence de degrés initiale ---
    deg_before = sorted(degree_sequence(G))

    # --- Lancer la convergence ---
    new_G, history, n_trials = run_until_stable(
        G,
        algo_func,
        batch_size=batch_size,
        max_trials=max_trials,
        window=window,
        tol_rel=tol_rel,
        copy_graph=copy_graph,
        verbose=verbose,
    )

    # --- Vérification de la préservation de la séquence de degrés ---
    deg_after = sorted(degree_sequence(new_G))
    assert deg_before == deg_after, "ERREUR: Séquence de degrés modifiée"

    # --- Vérifier que le graphe est toujours simple ---
    assert not any(u == v for u, v in new_G.edges()), "ERREUR: Boucle détectée dans le graphe"
    assert isinstance(new_G, nx.Graph), "ERREUR: Le graphe n'est plus de type simple"

    # --- Si activé, affichage visualisation graphique  ---
    if plot:
        # TODO
        print("TODO: visualisation graphique de la convergence des indicateurs ")

    if verbose:
        print(f"=== Test terminé ===\n")

    return new_G, history, n_trials

def main():
    # Générer un graphe simple non orienté
    n=100
    m=500
    G = generate_graph(n, m)

    A = nx.to_numpy_array(G)

    #np.savetxt("matrice_adjacence1.txt", A, delimiter=",", fmt="%d") #Pour générer un fichier avec la matrice du graphe 

    # Liste des algorithmes à comparer
    algorithms = [undirected_curveball,swap_randomization]

    results = []

    for algo in algorithms:
        start_time = time.time()
        new_G, history, n_trials = test_randomization_convergence(G, algo, verbose=False)
        end_time = time.time()

        ls_triangle = history["triangles"]
        ls_clust = history["avg_clustering"]
        ls_comp = history["largest_component"]

        """print("aaaaaaaa")
        print(history["triangles"])
        print("bbbbbbbbbb")"""

        algo_name = ""
        if algo.__name__ == "swap_randomization" :
            algo_name = "Swap"
        else:
            algo_name ="Trades"
        # Enregistrer les résultats
        results.append({
            "algorithm": algo_name,
            "execution_time": end_time - start_time,
            "num_triangles": ls_triangle[-1],
            "average_clustering":ls_clust[-1],
            "largest_connected_component" : ls_comp[-1],
            "convergence_iterations": n_trials
        })

    # Afficher les résultats
    print(f"\n=== Comparaison des algorithmes pour un graphe avec {n} noeuds et {m} arrêtes ===")
    for result in results:
        print(f"Algorithme: {result['algorithm']}")
        print(f"  Temps d'exécution: {result['execution_time']:.4f} s")
        print(f"  Nombre de triangles: {result['num_triangles']}")
        print(f"  Coefficient de clustering: {result['average_clustering']}")
        print(f"  Taille du plus grand composant connexe: {result['largest_connected_component']}")
        print(f"  Itérations de convergence: {result['convergence_iterations']}")
        
        

if __name__ == "__main__":
    main()