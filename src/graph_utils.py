import matplotlib.pyplot as plt
import networkx as nx
import random

def generate_graph(n=5, m=7):
    """Generates a random graph with n nodes and m edges"""
    # complete_bipartite_graph(n1, n2[, create_using]) Returns the complete bipartite graph K_{n_1,n_2}.
    G = nx.gnm_random_graph(n, m, directed=False, seed=0)
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

def plot_convergence(history, title="Convergence des indicateurs"):
    """
    Affiche les courbes de convergence pour :
    - nombre de triangles
    - clustering moyen
    - taille de la plus grande composante connexe
    """
    plt.figure(figsize=(10, 6))
    
    for key, values in history.items():
        plt.plot(values, label=key)
    
    plt.xlabel("Bloc d’itérations (x batch_size)")
    plt.ylabel("Valeur de l’indicateur")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_convergence_tail(history, k=100, title="Zoom sur la convergence des indicateurs"):
    """
    Affiche uniquement les k DERNIERS points de chaque indicateur,
    pour visualiser la convergence locale.
    """
    plt.figure(figsize=(10, 6))
    
    for key, values in history.items():
        tail_values = values[-k:] if len(values) >= k else values
        plt.plot(tail_values, label=key)
    
    plt.xlabel(f"Derniers blocs (fenêtre = {k})")
    plt.ylabel("Valeur de l’indicateur")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()