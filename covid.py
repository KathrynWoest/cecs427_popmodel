import networkx as nx
import copy
import random


def covid(graph, initiators, prob_infect, prob_death, lifespan, shelter, vaccination):
    try:
        prob_infect = float(prob_infect)
        prob_death = float(prob_death)
        lifespan = int(lifespan)
        shelter = float(shelter)
        vaccination = float(vaccination)
    
    except Exception as e:
        raise Exception("Program terminated due to a failure in covid calculation with the argument types. Error:", e)

    if lifespan < 1:
        raise Exception(f"Program terminated due to a failure in covid calculation: lifespan {lifespan} must be greater than 0.")

    if (prob_infect < 0 or prob_infect > 1) or (prob_death < 0 or prob_death > 1) or (shelter < 0 or shelter > 1) or (vaccination < 0 or vaccination > 1):
        raise Exception(f"Program terminated due to a failure in cascade calculation: probability of infection, death, shelter, and/or vaccination is not between 0 and 1.")

    for initiator in initiators:
        if initiator not in graph:
            raise Exception(f"Program terminated due to a failure in cascade calculation: node {initiator} does not exist in the given graph.")

    try:
        tracker = []
        new_graph = copy.deepcopy(graph)
        T_INFECT = 2
        T_RECOVER = 2

        # initialize all attributes and initiators
        nx.set_node_attributes(new_graph, "S", name="state")  # S (susceptible), I (infected), R (recovering), D (dead)
        nx.set_node_attributes(new_graph, False, name="initiator")
        nx.set_node_attributes(new_graph, "none", name="protection")  # none, shelter, vaccine
        nx.set_node_attributes(new_graph, 0, name="I_count")
        nx.set_node_attributes(new_graph, 0, name="R_count")
        
        for node in initiators:
            new_graph.nodes[node]["state"] = "I"
            new_graph.nodes[node]["initiator"] = True
            new_graph.nodes[node]["I_count"] = T_INFECT
        
        # save the initial graph, where just the initiators adopted
        tracker.append(copy.deepcopy(new_graph))

        for i in lifespan:
            last_step_graph = copy.deepcopy(new_graph)
            
            # for every node in the graph, get its neighbors
            for node in last_step_graph:
                # if the node is susceptible or dead, the node has nothing to do, so skip it

                # if the node is recovering, decrement how much time it has left in recovery
                if last_step_graph.nodes[node]["state"] == "R":
                    new_graph.nodes[node]["R_count"] -= 1

                    # if it recovered, make the node susceptible again
                    if new_graph.nodes[node]["R_count"] < 1:
                        new_graph.nodes[node]["state"] = "S"

                elif last_step_graph.nodes[node]["state"] == "I":
                    neighbors = list(last_step_graph.successors(node))

                    for neighbor in neighbors:
                        # if the neighbor is not susceptible, then skip it
                        if last_step_graph.nodes[neighbor]["state"] in ["I", "R", "D"]:
                            continue
                        
                        # TODO: add checks for vaccinated and sheltered
                        
                        if random.random() <= prob_infect:
                            new_graph.nodes[neighbor]["state"] = "I"
                            new_graph.nodes[neighbor]["I_count"] = T_INFECT

                        # check if node died
                        # check if node recovered

            # save the current state of the graph for interactive/plot
            tracker.append(copy.deepcopy(new_graph))

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