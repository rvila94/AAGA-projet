import networkx as nx
import numpy as np
import time
import argparse

from graph_utils import generate_graph, plot_graph, degree_sequence, plot_convergence, plot_convergence_tail
from swap_algo import swap_randomization
from trade_algo import curveball, undirected_curveball
from convergence import run_empirical, run_until_stable

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
        plot_convergence(history, title="Convergence des indicateurs - " + algo_name)
        plot_convergence_tail(history, k=50, title="Zoom sur la convergence des indicateurs - " + algo_name)

    if verbose:
        print(f"=== Test terminé ===\n")

    return new_G, history, n_trials

def generate_test_graphs():
    """
    Génère une liste de graphes à tester.
    Chaque graphe est donné avec un nom pour l'affichage.
    """
    graphs = []

    # 1. Petit graphe pour tester le bon fonctionnement, pas utile pour comparer les deux algorithmes
    graphs.append(("SmallExampleGraph (n=5, m=7)", generate_graph(5, 7)))

    # 2. Graph aléatoire avec n=20 et m=30
    graphs.append(("Random graph (n=20, m=30)", generate_graph(20, 30)))

    # 3. Erdos–Renyi n=100 p=0.05 (exemple)
    graphs.append(("Erdos-Renyi (n=100, p=0.05)", nx.erdos_renyi_graph(100, 0.05, seed=0)))

    # 4. quatrieme graphe à tester


    # 5. cinquieme graphe à tester etc...
    

    return graphs

def compare_algorithms_on_graph(G, algo_funcs, runs=5, verbose=False, plot=False):
    """
    Exécute les algorithmes sur un graph donné, plusieurs fois,
    puis renvoie les statistiques moyennes.
    """
    results = []

    for algo in algo_funcs:
        algo_name = "Swap" if algo.__name__ == "swap_randomization" else "Trade"

        exec_times = []
        conv_iters = []
        triangles = []
        clusts = []
        comps = []

        for i in range(runs):
            print(f"Starting {algo_name} algorithm (run = {i})")
            start = time.time()
            new_G, history, n_trials = test_randomization_convergence(
                G,
                algo,
                verbose=verbose,
                plot=plot
            )
            end = time.time()

            exec_times.append(end - start)
            conv_iters.append(n_trials)
            triangles.append(history["triangles"][-1])
            clusts.append(history["avg_clustering"][-1])
            comps.append(history["largest_component"][-1])

        # Moyennes des runs
        results.append({
            "algorithm": algo_name,
            "avg_execution_time": np.mean(exec_times),
            "std_execution_time": np.std(exec_times),

            "avg_convergence_iterations": np.mean(conv_iters),
            "std_convergence_iterations": np.std(conv_iters),

            "avg_triangles": np.mean(triangles),
            "avg_clustering": np.mean(clusts),
            "avg_lcc": np.mean(comps),
        })

    return results


def main():
    parser = argparse.ArgumentParser(description="Swap vs Trade — random graph experiments")

    parser.add_argument("--runs", type=int, default=5, help="Nombre de répétitions par algorithme")
    parser.add_argument("--verbose", action="store_true", help="Affiche les détails des algorithmes")
    parser.add_argument("--plot", action="store_true", help="Affiche les graphiques de convergence")

    args = parser.parse_args()

    runs = args.runs
    verbose = args.verbose
    plot = args.plot

    algo_funcs = [swap_randomization, undirected_curveball]
    graph_list = generate_test_graphs()

    for graph_name, G in graph_list:
        print("\n" + "="*60)
        print(f"   TEST : {graph_name}")
        print("="*60)

        results = compare_algorithms_on_graph(
            G, algo_funcs, runs=runs, verbose=verbose, plot=plot
        )

        # Toujours afficher le résumé final (verbose ou pas)
        for r in results:
            print(f"\nAlgorithme : {r['algorithm']}")
            print(f"  Temps moyen d'exécution : {r['avg_execution_time']:.4f}s ± {r['std_execution_time']:.4f}")
            print(f"  Itérations de convergence : {r['avg_convergence_iterations']:.1f} ± {r['std_convergence_iterations']:.1f}")
            print(f"  Nombre moyen de triangles : {r['avg_triangles']:.1f}")
            print(f"  Clustering moyen : {r['avg_clustering']:.4f}")
            print(f"  Taille du LCC : {r['avg_lcc']:.1f}")
        
        

if __name__ == "__main__":
    main()