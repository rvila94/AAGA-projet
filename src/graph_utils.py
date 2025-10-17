import matplotlib.pyplot as plt
import networkx as nx
import random

def generate_graph(n=10, m=15):
    """Generates a random graph with n nodes and m edges"""
    G = nx.gnm_random_graph(n, m)
    return G

def plot_graph(G, title="Graoh"):
    """Plot a given graph"""
    nx.draw(G, with_labels=True, node_color='blue', edge_color='gray')
    plt.title(title)
    plt.show()
    
def degree_sequence(G):
    """Return degree sequence"""
    return [d for _, d in G.degree()]