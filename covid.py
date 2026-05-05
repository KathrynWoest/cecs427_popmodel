import networkx as nx
import copy
import random
import numpy


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
        nx.set_node_attributes(new_graph, False, name="vaccinated")
        nx.set_node_attributes(new_graph, 0, name="I_count")
        nx.set_node_attributes(new_graph, 0, name="R_count")
        
        for node in initiators:
            new_graph.nodes[node]["state"] = "I"
            new_graph.nodes[node]["initiator"] = True
            new_graph.nodes[node]["I_count"] = T_INFECT
        

        # determine which nodes are vaccinated (can include initiators and sheltered nodes)
        nodes = list(new_graph.nodes())
        node_count = int(numpy.ceil(len(nodes) * vaccination))
        rand_indices = []

        # for the number of nodes that must be vaccinated per the vaccination input
        for i in range(node_count):
            rand_node_index = random.randint(0, len(nodes) - 1)

            # keep randomly selecting nodes until the selected node hasn't been picked yet
            while rand_node_index in rand_indices:
                rand_node_index = random.randint(0, len(nodes) - 1)
        
            # set the node's protection to vaccinated
            rand_indices.append(rand_node_index)
            new_graph.nodes[nodes[rand_node_index]]["vaccinated"] = True
        

        # determine which edges to remove to indicate sheltered nodes, using the same process as for vaccinated nodes
        edges = list(new_graph.edges())
        edge_count = int(numpy.ceil(len(edges) * shelter))
        rand_indices = []

        for i in range(edge_count):
            rand_edge_index = random.randint(0, len(edges) - 1)

            while rand_edge_index in rand_indices:
                rand_edge_index = random.randint(0, len(edges) - 1)
            
            rand_indices.append(rand_edge_index)
            new_graph.remove_edge(*edges[rand_edge_index])
        

        # save the initial graph, where just the initiators adopted
        tracker.append(copy.deepcopy(new_graph))


        # begin the analysis
        for i in range(lifespan):
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

                # if the node is infected, calculate effects on neighbors
                elif last_step_graph.nodes[node]["state"] == "I":
                    neighbors = list(last_step_graph.successors(node))

                    for neighbor in neighbors:
                        # if the neighbor is not susceptible, then skip it
                        if last_step_graph.nodes[neighbor]["state"] in ["I", "R", "D"]:
                            continue
                        
                        # if the node is vaccinated, make the chances of being infected significantly lower
                        if last_step_graph.nodes[neighbor]["vaccinated"]:
                            if random.random() < (prob_infect * vaccination):
                                new_graph.nodes[neighbor]["state"] = "I"
                                new_graph.nodes[neighbor]["I_count"] = T_INFECT
                                                
                        # check to see if the neighbor got infected, and if it did, set its attributes
                        elif random.random() < prob_infect:
                            new_graph.nodes[neighbor]["state"] = "I"
                            new_graph.nodes[neighbor]["I_count"] = T_INFECT

                    # check to see if the node died at the end of the step
                    if random.random() < prob_death:
                        new_graph.nodes[node]["state"] = "D"
                        new_graph.nodes[node]["I_count"] = 0

                    # if it didn't die, decrement its infected count and determine if it recovered
                    else:
                        new_graph.nodes[node]["I_count"] -= 1

                        if new_graph.nodes[node]["I_count"] < 1:
                            new_graph.nodes[node]["state"] = "R"
                            new_graph.nodes[node]["R_count"] = T_RECOVER

            # save the current state of the graph for interactive/plot
            tracker.append(copy.deepcopy(new_graph))

        # determine the final state of the graph
        susceptible = []
        infected = []
        recovering = []
        dead = []
        for node in new_graph:
            if new_graph.nodes[node]["state"] == "S":
                susceptible.append(node)
            elif new_graph.nodes[node]["state"] == "I":
                infected.append(node)
            elif new_graph.nodes[node]["state"] == "R":
                recovering.append(node)
            else:
                dead.append(node)

        # print results
        print("\n-----Covid-----")
        print("Initial nodes:", initiators)
        print("Probability of infection:", prob_infect)
        print("Probability of death:", prob_death)
        print("Probability of sheltered:", shelter)
        print("Probability of vaccinated:", vaccination)
        print("\nFinal State:")
        print("Susceptible:", susceptible)
        print("Infected:", infected)
        print("Recovering:", recovering)
        print("Dead:", dead)
    
    except Exception as e:
        raise Exception("Program terminated due to a failure in covid calculation:", e)

    # return the tracked states
    return tracker