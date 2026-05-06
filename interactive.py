import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def show_interactive(user_graph, track, mode):
    """
    Plots the graph and the state of the nodes for every round in the simulation.

    Parameters:
        user_graph (NetworkX.Graph): the original graph
        track ([NetworkX.Graph]): a list of graphs containing the resulting graphs after every round
        mode (string): the graph's mode (either 'cascade' or 'covid')
    """

    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(bottom=0.2) # Make room for the slider
    
    pos = nx.spring_layout(user_graph, seed=42)
    
    # Setup the slider
    ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
    slider = Slider(ax_slider, 'Round', 0, len(track) - 1, valinit=0, valfmt='%d')

    def update(val):
        round_idx = int(slider.val)
        ax.clear()
        G_step = track[round_idx]
        
        node_colors = []
        for node, attrs in G_step.nodes(data=True):
            if mode == 'cascade':
                node_colors.append('orange' if attrs.get('adopt') == True else 'skyblue')
            else: # covid mode
                stage = attrs.get('stage', 'S')
                if stage == 'I': node_colors.append('red')
                elif stage == 'R': node_colors.append('green')
                elif stage == 'D': node_colors.append('black')
                elif attrs.get('vaccinated'): node_colors.append('blue')
                elif attrs.get('sheltered'): node_colors.append('gray')
                else: node_colors.append('skyblue')

        ax.set_title(f"Interactive View: {mode.capitalize()} - Round {round_idx}")
        nx.draw(G_step, pos, ax=ax, with_labels=True, node_color=node_colors, 
                node_size=500, edge_color='silver')
        
        # Re-add legend (Matplotlib clears it on ax.clear())
        labels = {'Infected/Adopted': 'red' if mode=='covid' else 'orange', 'Susceptible': 'skyblue'}
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=c, label=l) for l, c in labels.items()]
        ax.legend(handles=handles, loc='upper right')
        fig.canvas.draw_idle()

    slider.on_changed(update)
    update(0) # Initial draw
    plt.show()