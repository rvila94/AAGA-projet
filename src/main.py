from graph_utils import generate_graph, plot_graph, degree_sequence
from swap_algo import swap_randomization
from trade_algo import curveball
from convergence import run_empirical, run_until_stable
import networkx as nx


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
    #G = nx.erdos_renyi_graph(10, 0.8, seed=42)
    G = generate_graph(5,7)

    # Lancer le test sur l'algorithme de swap
    test_randomization_convergence(G, swap_randomization)

if __name__ == "__main__":
    main()