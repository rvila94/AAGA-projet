from graph_utils import generate_graph, plot_graph, degree_sequence
from swap_algo import swap_randomization
from trade_algo import curveball
from convergence import run_empirical, run_until_stable
import networkx as nx

def main():
    
    # Generation de graphe aleatoire, 
    # par la suite on pourra faire des tests sur des graphes specifique qu'on aura trouver ou generer nous meme
    G = generate_graph()

    # Lancement des algos swap et trade jusqu'a stabilisation des indicateurs 
    new_G_swap, history, n_trials = run_until_stable(G, swap_randomization, verbose=True)
    # TODO: lancer ici run_until_stable avec l'algo de trade quand implementé

    # Check piur voir si la sequence de degrée est toujours la meme
    deg_before = degree_sequence(G)

    deg_after_swap  = degree_sequence(new_G_swap)
    assert sorted(deg_before) == sorted(deg_after_swap), "Erreur: Séquence de degrés modifiée lors de l'algorithme swap!"
    # TODO: faire le meme assert pour l'algo de trade 


if __name__ == "__main__":
    main()