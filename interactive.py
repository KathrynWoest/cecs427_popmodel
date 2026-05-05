import networkx as nx
import matplotlib.pyplot as plt

def interactive(G, round_num, mode='cascade'):
    """
    Plots the graph and the state of the nodes for a single round.

    Parameters:
        G (NetworkX.Graph): the original graph
        round_num (int): the current round number being visualized
        mode (string): the graph's mode (either 'cascade' or 'covid')
    """
    
    plt.figure(figsize=(8, 6))
    plt.title(f"Interactive View: {mode.capitalize()} - Round {round_num}")
    
    # Consistent layout
    pos = nx.spring_layout(G, seed=42)
    node_colors = []
    
    for node, attrs in G.nodes(data=True):
        if mode == 'cascade':
            node_colors.append('orange' if attrs.get('adopt') == 'yes' else 'skyblue')
        else: # covid mode
            stage = attrs.get('stage', 'susceptible')
            if stage == 'infected': node_colors.append('red')
            elif stage == 'recovery': node_colors.append('green')
            elif attrs.get('vaccinated'): node_colors.append('blue')
            elif attrs.get('sheltered'): node_colors.append('gray')
            else: node_colors.append('skyblue')

    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, edge_color='silver')
    plt.show()