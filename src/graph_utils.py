import matplotlib.pyplot as plt
import networkx as nx
import random

def generate_graph(n=5, m=7):
    """Generates a random graph with n nodes and m edges"""
    # complete_bipartite_graph(n1, n2[, create_using]) Returns the complete bipartite graph K_{n_1,n_2}.
    G = nx.gnm_random_graph(n, m, directed=True)
    return G

def plot_graph(G, new_G, title="Graph"):
    """Plot a given graph"""
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    nx.draw(G, with_labels=True, node_color='blue', edge_color='gray')
    plt.title(title)

    plt.subplot(1, 2, 2)
    nx.draw(new_G, with_labels=True, node_color='red', edge_color='gray')
    plt.title("Modified " + title)

    plt.show()
    
def degree_sequence(G):
    """Return degree sequence"""
    return [d for _, d in G.degree()]