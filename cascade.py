import networkx as nx
import copy


def cascade(graph, initiators, threshold):
    try:
        threshold = float(threshold)
    except Exception as e:
        raise Exception(f"Program terminated due to a failure in cascade calculation: threshold {threshold }is not a number.")

    if threshold < 0 or threshold > 1:
        raise Exception(f"Program terminated due to a failure in cascade calculation: threshold {threshold} is not between 0 and 1.")

    for initiator in initiators:
        if initiator not in graph:
            raise Exception(f"Program terminated due to a failure in cascade calculation: node {initiator} does not exist in the given graph.")

    try:
        cascade_stop = False
        tracker = []
        new_graph = copy.deepcopy(graph)

        # initialize all attributes and initiators
        nx.set_node_attributes(new_graph, False, name="adopt")
        nx.set_node_attributes(new_graph, False, name="initiator")
        for node in initiators:
            new_graph.nodes[node]["adopt"] = True
            new_graph.nodes[node]["initiator"] = True
        
        # save the initial graph, where just the initiators adopted
        tracker.append(copy.deepcopy(new_graph))

        while not cascade_stop:
            last_step_graph = copy.deepcopy(new_graph)
            changed = False
            
            # for every node in the graph, get its neighbors
            for node in last_step_graph:
                neighbors = list(last_step_graph.neighbors(node))
                num_neighbors = len(neighbors)
                adopt = 0

                # iterate through all neighbors to determine the number of neighbors who adopted
                for neighbor in neighbors:
                    if last_step_graph.nodes[neighbor]["adopt"]:
                        adopt += 1
                
                # if the number of adoptee neighbors is at least the threshold, then the node adopts too
                if (num_neighbors > 0) and (adopt / num_neighbors) >= threshold:
                    if not new_graph.nodes[node]["adopt"]:
                        new_graph.nodes[node]["adopt"] = True
                        changed = True
            
            # save the current state of the graph for interactive/plot
            tracker.append(copy.deepcopy(new_graph))

            # if the current graph is the same at the end of this step as it was at the beginning, then the cascade stopped, so stop iterating
            if not changed:
                cascade_stop = True

        # determine the final state of the graph
        adopters = []
        for node in new_graph:
            if new_graph.nodes[node]["adopt"]:
                adopters.append(node)

        # print results
        print("\n-----Cascade-----")
        print("Initial nodes:", initiators)
        print("Threshold:", threshold)
        print("\nAll adopters:", adopters)
        print(f"Percentage of nodes in the graph that ultimately adopted: {(len(adopters) / len(list(new_graph.nodes())) * 100):.2f}%")
    
    except Exception as e:
        raise Exception("Program terminated due to a failure in cascade calculation:", e)

    # return the tracked states
    return tracker