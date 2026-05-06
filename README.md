# CECS 427 Project 6: Dynamic Population Model
Completed By: Kathryn Woest (030131541) and Grace Flores (030169163)


## Usage Instructions
1. Clone this repo and open it on your IDE

2. DEPENDENCIES: This program relies on two external libraries. To install them, ensure you are inside the project directory and run these commands:
    1. **NetworkX**, a library that provides `.gml` file parsing and writing, graph support, and analysis functions. To install, run: `pip install networkx[default]`
    2. **Matplotlib**, a library used for creating and plotting graphs. To install, run: `pip install matplotlib`

3. Run this program with: `python dynamic_population.py input_file.gml --action [covid | cascade] --initiator n1,n2,... --threshold q --probability_of_infection p --probability_of_death q --lifespan l --shelter s --vaccination r --plot --interactive`
    1. The first argument after `python dynamic_population.py` MUST be `input_file.gml`.
    2. All other arguments can be provided in any order. For example, `python dynamic_population.py input_file.gml --action covid --shelter 0.3` returns the same results as `python dynamic_population.py input_file.gml --shelter 0.3 --action covid`.
    3. However, parameters to those arguments must follow the arguments. For example, `--action` MUST be directly followed by either `covid` or `cascade` or the command will be skipped and an error message printed.
    4. `--initiator` can take multiple nodes that are initial adopters or initially infected, but they must be formatted as `n1,n2,n3`, not `n1, n2, n3`, `n1 n2 n3`, or something else.
    5. With the exception of `input_file.gml`, all other commands are optional. For example, you could just input an action and plot the results. All of the probability/initiator/threshold arguments have default values and will run the program with those if you don't provide a value.


## Implementation Description
1. **Overall Program:** `dynamic_population.py` calls functions from all the below files to compute either the results of a cascade or covid infection throughout a given network. It will read the file in and, if directed, plot and/or show an interactive display of the results.
2. **MAIN - dynamic_population.py:** Calls functions from all other files. Allows for arguments to be in any order, as described above. Robust error handling. Provides default values for most of the inputs: `initiator=first_node_in_graph`, `threshold=0.5`, `probability_of_infection=0.2`, `probability_of_death=0`, `lifespan=20`, `shelter=0`, and `vaccination=0`. If both `cascade` and `covid` are provided to `--action`, then the program will only run the first one listed. A lot of code in this file is reused from Projects 1-5.
3. **cascade.py:** Traces a cascade through the provided network by making a copy of the prior state and updating the graph for the current state based off the values in the copy. Tracks the adopters and initiators with boolean attributes. A node adopts if at least `threshold` neighbors also adopted. Stops once the current state is the same as the prior state, which either occurs when the cascade is halted OR when every node adopts. Prints the results and returns a list of copies of the graph at every step.
4. **covid.py:** Traces a covid infection through the provided network by making a copy of the prior state and updating the graph for the current state based off the values in the copy. Tracks initiators and vaccinated nodes with boolean attributes and the current state with a state attribute. Also tracks how long a node has been infected or in recovery to appropriately switch its state after `t` steps, which was set as `2` for this program. Determines the number of nodes vaccinated by finding the ceiling of the percentage of nodes equal to the vaccine float provided, and marks them as vaccinated by a boolean attribute. Uses the same process to find the number of edges to remove to indicate sheltering nodes, and completely removes the edges from the graph before the first step. Moves through each node every step, only acting if the node is infected or recovering. If recovering, decreases how long its been recovering and switches it to susceptible if it was in recovery for two steps. If infected, collects its neighbors and randomly generates a float. It infects a neighbor if the float is less than the probability of infection. If the neighbor was vaccinated, it uses the same process but compares the float to the probability of infection multiplied by the vaccination float provided. It then checks to see if the node died or leaves the infected state. It stops once it completes `lifespan` steps. Prints the results and returns a list of copis of the graph at every step.
5. **plot.py:** Plots the number of new infections per day after the simulation has completed. Takes in the user's graph 
6. **interactive.py:**
7. **file_i.py:** Defines `parse_graph()`, which takes a `.gml` file in and parses it into a NetworkX graph. Checks for an empty graph and determines if the graph is directed, as `covid` requires a directed graph but `cascade` does not. Reuses a lot of code from Projects 1-5.


## Example Commands and Outputs
1. Command: `python3 dynamic_population.py cascadebehaviour.gml --action cascade --initiator 6 --threshold 0.3 --plot`
2. Command: `python3 dynamic_population.py cascadebehaviour.gml --action covid --interactive`
3. Command: `python3 dynamic_population.py cascadebehaviour.gml --action covid --initiator 1,5,6 --probability_of_infection 0.5 --probability_of_death 0.2 --lifespan 5 --shelter 0.1 --vaccination 0.3`

Outputs for all are annotated in this PDF: 