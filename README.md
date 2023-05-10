**AttAttach** is a python library for generating the attractor landscape of a Boolean network with given number and types of attractors.

The attractor landscape of the deterministic dynamics of a Boolean network with $n$ dynamic nodes possesses the folowing properties:
1) It is a directed graph with $2^n$ nodes (global states of the Boolean network);
2) The out degree of each of its nodes is equal to 1.

Therefore, it is the union of a finite number of disconnet components. Each component includes of a single cycle (a fixed-point when the length of the cycle is equal to 1) with a certain number of converging *branches* (subnetworks with a three topology) attached to it. 

**AttAttach** generates this landscape for a specified number of cycles of given lengths. For each basins, it firsts generates the transitions within the cycle. It then selects a random number of nodes in the basin (according to a uniform distribution) that will directly transition to the cycle. It progressively populates outher shells of nodes until all nodes in the besin are included. 

Notice that, even if the number of nodes in a layer is determined using a uniform distribution between 1 and the number of nodes still available, this algorithm favors layer distributions where layers closer to the cycle are more densily populated. Changing this bias requires modifying the **layer_distribution** function. 

This process is repeated for each basin. These disconnected components are then joined, and the final labels are permutated.


<img src="diagram.png" alt="..." width="630" height="270">
