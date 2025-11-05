import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
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

def plot_all_indicators(history, window, tol_rel, algo_name):
    """
    Affiche l’évolution de chaque indicateur avec un diagnostic de convergence basé
    uniquement sur les `window` dernières valeurs observées.

    Signification des lignes tracées :
      - Bleu  : évolution brute de l’indicateur au cours des itérations.
      - Rouge : moyenne des `window` derniers points -> estimation de l’état actuel stable.
      - Orange: intervalle [moyenne ± écart-type] -> mesure de la variabilité récente.
      - Vert  : bande de tolérance [moyenne ± tol_rel * moyenne] -> seuil de stabilisation attendu.

    Critère visuel de convergence :
      -> L’indicateur est considéré comme stable lorsque ses variations récentes
        (bande orange) restent entièrement **à l’intérieur** de la bande verte.
    """

    indicators = {
        "largest_component": "Taille de la plus grande composante connexe",
        "avg_clustering": "Clustering moyen",
        "triangles": "Nombre de triangles"
    }

    for key, label in indicators.items():
        values = history[key]

        plt.figure(figsize=(10, 6))
        plt.plot(values, label=label, color="blue", alpha=0.7)

        if len(values) >= window:
            recent = np.array(values[-window:], dtype=float)
            mean = recent.mean()
            std = recent.std()
            tol_range = tol_rel * mean

            # Moyenne locale (rouge)
            plt.axhline(mean, color="red", linestyle="--", linewidth=1.4,
                        label=f"Moyenne locale (sur {window} derniers) = {mean:.3f}")

            # Bande d’écart-type (orange)
            plt.axhline(mean + std, color="orange", linestyle=":", linewidth=1.2,
                        label=f"Moyenne ± écart-type (± {std:.3f})")
            plt.axhline(mean - std, color="orange", linestyle=":")

            # Bande de tolérance (vert)
            plt.axhline(mean + tol_range, color="green", linestyle="--", linewidth=1.2,
                        label=f"Limite de tolérance (± {tol_rel:.3f} × mean)")
            plt.axhline(mean - tol_range, color="green", linestyle="--")

        plt.xlabel("Bloc d’itérations (x batch_size)")
        plt.ylabel(label)
        plt.title(f"Convergence de {label} — {algo_name}")
        plt.legend(loc="upper left")
        plt.grid(True, alpha=0.4)
        plt.tight_layout()

    plt.show()
