from graph_utils import generate_graph, plot_graph, degree_sequence
from swap_algo import swap_randomization

def main():

    G = generate_graph()
    #plot_graph(G)

    new_G = swap_randomization(G, 100, trace=True)
    #plot_graph(new_G)

    deg_before = degree_sequence(G)
    deg_after  = degree_sequence(new_G)

    print("\nSéquence de degrés initiale :", deg_before)
    print("Séquence de degrés finale   :", deg_after)
    assert sorted(deg_before) == sorted(deg_after), "Erreur: Séquence de degrés modifiée !"

if __name__ == "__main__":
    main()