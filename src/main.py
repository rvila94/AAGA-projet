from graph_utils import generate_graph, plot_graph, degree_sequence
from swap_algo import swap_randomization
from convergence import run_empirical, run_until_stable
import networkx as nx

from trade_algo import curveball

def main():

    G = generate_graph()
    M = nx.to_numpy_array(G)
    #plot_graph(G)

    new_G_swap = run_empirical(G, swap_randomization, verbose=True)
    print("Matrice avant trade :")
    print(M)
    adj_matrix_trade = curveball(M)
    print("Matrice après trade :")
    print(adj_matrix_trade)
    new_G_trade = nx.from_numpy_array(adj_matrix_trade, create_using=nx.DiGraph)

    plot_graph(G, new_G_swap)
    plot_graph(G, new_G_trade)

    deg_before = degree_sequence(G)
    deg_after  = degree_sequence(new_G_swap)
    assert sorted(deg_before) == sorted(deg_after), "Erreur: Séquence de degrés modifiée !"

if __name__ == "__main__":
    main()