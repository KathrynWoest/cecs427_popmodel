## NOTE: this file reuses a lot of code from Projects 1-5

import sys
import file_i
import cascade
import covid
#import plot
#import interactive


def main():
    # get arguments from command line
    args = sys.argv
    end = len(args)

    if end < 3:
        raise Exception(f"Program was terminated because there are not enough arguments to upload a graph or select an action. Minimum required arguments: 3. Arguments provided: {end}.")

    if "--action" in args:
        user_graph, directed = file_i.parse_graph(args[1])
        action = args[args.index("--action") + 1]
        if action not in ["cascade", "covid"]:
            raise Exception(f"Program was terminated because the action provided was not 'cascade' or 'covid'. Action provided:", action)
    else:
        raise Exception("Program terminated because no action argument ('--action') was provided.")
    
    # both cascade and covid use the initiators, so define here
    # default to the first node defined in the graph if not provided initiator(s)
    initiators = args[args.index("--initiator") + 1].split(",") if "--initiator" in args else [next(iter(user_graph.nodes))]
    
    if action == "cascade":
        # initialize cascade threshold with provided value, using default of 0.5
        threshold = args[args.index("--threshold") + 1] if "--threshold" in args else 0.5
        
        # call the cascade analysis
        track = cascade.cascade(user_graph, initiators, threshold)

    else:
        # check if the graph is directed for covid
        if not directed:
            raise Exception("Program terminated because graph is undirected. For the covid simulation, the graph must be directed.")
        
        # initialize covid values with provided values, using defaults of 0.2, 20, and 0 if not given
        prob_infect  =  args[args.index("--probability_of_infection") + 1]  if "--probability_of_infection" in args  else 0.2
        prob_death   =  args[args.index("--probability_of_death") + 1]      if "--probability_of_death" in args      else 0
        lifespan     =  args[args.index("--lifespan") + 1]                  if "--lifespan" in args                  else 20
        shelter      =  args[args.index("--shelter") + 1]                   if "--shelter" in args                   else 0
        vaccination  =  args[args.index("--vaccination") + 1]               if "--vaccination" in args               else 0
        
        # call the covid analysis
        track = covid.covid(user_graph, initiators, prob_infect, prob_death, lifespan, shelter, vaccination)


    # call the interactive function
    #if "--interactive" in args:
        #interactive.interactive(user_graph, track, action)


    # call the plotting function
    #if "--plot" in args:
        #plot.plot(user_graph, track, action)

main()