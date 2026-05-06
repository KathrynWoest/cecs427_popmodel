import matplotlib.pyplot as plt

def plot(user_graph, track, action):
    """
    Plots the number of new infections per day when the simulation completes.

    Parameters:
        user_graph (NetworkX.Graph): the original graph
        track ([NetworkX.Graph]): a list of graphs containing the resulting graphs after every round
        mode (string): the graph's mode (either 'cascade' or 'covid') 
    """

    if not track:
        print("No simulation data to plot.")
        return

    # Using user_graph to get the total population for reference/scaling
    total_population = len(user_graph.nodes)
    new_counts = []
    
    for i in range(len(track)):
        if i == 0:
            # For round 0, count initial initiators
            if action == 'cascade':
                count = sum(1 for n, d in track[i].nodes(data=True) if d.get('adopt') == True)
            else:
                count = sum(1 for n, d in track[i].nodes(data=True) if d.get('stage') == 'I')
        else:
            # Compare current step to previous step to find 'NEW' occurrences
            if action == 'cascade':
                prev_nodes = {n for n, d in track[i-1].nodes(data=True) if d.get('adopt') == True}
                curr_nodes = {n for n, d in track[i].nodes(data=True) if d.get('adopt') == True}
            else:
                prev_nodes = {n for n, d in track[i-1].nodes(data=True) if d.get('stage') == 'I'}
                curr_nodes = {n for n, d in track[i].nodes(data=True) if d.get('stage') == 'I'}
            
            # New = (nodes infected now) MINUS (nodes that were already infected)
            count = len(curr_nodes - prev_nodes)
        
        new_counts.append(count)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(new_counts)), new_counts, color='tab:red', marker='o', linewidth=2)
    
    title_text = "New Adoptions" if action == 'cascade' else "New Infections"
    plt.title(f"{title_text} Per Day (Total Population: {total_population})")
    plt.xlabel("Day / Round")
    plt.ylabel("Count")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()