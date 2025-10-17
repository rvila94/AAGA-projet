from graph_utils import generate_graph, plot_graph, degree_sequence
from swap_algo import swap_randomization
from convergence import run_empirical, run_until_stable

def main():

    G = generate_graph()
    #plot_graph(G)

    new_G = run_empirical(G, swap_randomization, verbose=True)
    #plot_graph(new_G)

    deg_before = degree_sequence(G)
    deg_after  = degree_sequence(new_G)
    assert sorted(deg_before) == sorted(deg_after), "Erreur: Séquence de degrés modifiée !"

if __name__ == "__main__":
    main()