import random
import numpy as np
from itertools import combinations
import networkx as nx
from networkx.algorithms import isomorphism

def transitions_between_layers(inner_layer,outher_layer):
    """
    Generate transitions from the outher to the inner layer.
    The inputs are lists of states in the two layers
    """
    edges = []
    for i in outher_layer:
        random.shuffle(inner_layer)
        j = inner_layer[0]
        edges.append((i,j))
    return edges

def core_transitions(length):
    """
    Given the length of the cycle,
    generate its associated transitions.
    These states take labels 0, 1, ..., length 
    """
    return [(i, (i+1)%length) for i in range(length)]

def layer_distribution(length, num_states):
    """
    Generate the distribution of the number of states,
    [n1,n2,n3,...]
    where n1 is the number of states in the innermost layer (i.e. the cycle),
    n2 is the number of states in layer 2, etc.
    """
    layer_widths = [length]
    while sum(layer_widths) < num_states:
        assigned_states = sum(layer_widths)
        m = random.randint(1,num_states-assigned_states)
        layer_widths.append(m)
    return layer_widths

def transitions(length, num_states):
    """
    Generate the list of transitions for a single connected component.
    The states are labeled 0, ..., num_states.
    """
    
    dist = layer_distribution(length, num_states)
    edges = core_transitions(length)

    for i in range(len(dist)-1):
    
        # outher_layer
        layer_id = i+1
        start = sum(dist[:layer_id])
        stop  = sum(dist[:layer_id]) + dist[layer_id]
        outher_layer = list(range(start, stop))
    
        # inner_layer
        layer_id = i
        start = sum(dist[:layer_id])
        stop  = sum(dist[:layer_id]) + dist[layer_id]
        inner_layer = list(range(start, stop))
    
        edges = edges + transitions_between_layers(inner_layer,outher_layer)
    
    return edges

def join_transitions(transitions1,transitions2):
    """
    Joins two lists of transitions after shifting the labels in the second list
    """
    s1 = len(transitions1)
    s2 = len(transitions2)
    #shift the labels in transitions2
    p = list(range(s1,s1+s2))
    new_transitions2 = [(p[i], p[j]) for (i, j) in transitions2]
    return transitions1 + new_transitions2

def labels_permutation (transitions):
    """
    randomly reassign state labels
    """
    # Generate a random permutation of the labels
    s = len(transitions)
    p = list(range(s))
    random.shuffle(p)
    # Create a new list of edges with the updated labels
    new_transitions = [(p[i], p[j]) for (i, j) in transitions]
    sorted_transitions = sorted(new_transitions, key=lambda x: x[0])
    return sorted_transitions

def generate_landscape(num_nodes,landscape_structure):
    """
    Sample landscape structure: [[3,.25],[1,.50],[1,.05],[2,.20]]
    This corresponds to 4 attractors, of lengths 3, 1, 1, and 2,
    with relative basins sizes equal to 25%, 50%, 5%, and 20%
    """
    
    s = 2**num_nodes # total number of states in the attractor landscape

    # Read the structure of the attractor landscape
    lengths = [B[0] for B in landscape_structure]
    rel_sizes = [B[1] for B in landscape_structure]
    sizes = [int(rel_size*s) for rel_size in rel_sizes] # the last one might be wrong
    sizes[-1] = s-(sum(sizes)-sizes[-1]) # this fixes it
    # attractor states in each basin:
    num_att_states = [ landscape_structure[i][0] for i in range(len(landscape_structure)) ]
    
    # CONDITION 1:
    # 'The sum of the relative basin sizes needs to be 1'
    c1 = np.allclose(sum(rel_sizes),1.) 

    # CONDITION 2:
    # All the basins have at least size 1 
    # (For small n and small relative size of a basin, the product might result in zero states)
    c2 = np.prod([sizes[i] > 0 for i in range(len(sizes))])

    # CONDITION3:
    # There are at least as many states as attractor states
    c3 = np.sum(num_att_states) <= s

    # CONDITION4:
    # There are at least as many states as attractor states **in each individual basin**
    c4 = np.prod([ num_att_states[i] <= sizes[i] for i in range(len(landscape_structure)) ])

    # If all conditions are satisfied, proceed:
    if c1*c2*c3*c4:
    
        # generate the individual basins
        t = []
        for i in range(len(landscape_structure)):
            t.append(transitions(lengths[i], sizes[i]))

        # join them with the sequential relabeling 
        all_t = []
        for i in range(len(t)):
            all_t = join_transitions(all_t,t[i])

        return all_t

    else:
        if not c1:
            print('ERROR: The sum of the relative basin sizes is not 1.')
        if not c2:
            print('ERROR: At least one basin has size 0.')
            print('       (relative size is too small for your n).')
        if not c3:
            print('ERROR: There are more attractor states than total states.')
        if not c4:
            print('ERROR: There are more attractor states than total states in at least one basin.')
        return None


def random_labels_permutation (transitions):
    """
    randomly reassign state labels
    """
    # Generate a random permutation of the labels
    s = len(transitions)
    p = list(range(s))
    random.shuffle(p)
    # Create a new list of edges with the updated labels
    new_transitions = [(p[i], p[j]) for (i, j) in transitions]
    sorted_transitions = sorted(new_transitions, key=lambda x: x[0])
    return sorted_transitions


def hamming_distance(v1, v2):
    """
    needed for 'smallH_labels_permutation'
    ...
    """
    return sum(x != y for x, y in zip(v1, v2))

def generate_edges_fixed_H(n, H):
    """
    needed for 'smallH_labels_permutation'
    (Doesn't work with H=0)
    ...
    """
    assert(H>0)
    vertices = [(i, format(i, f'0{n}b')) for i in range(2**n)]
    edges = []
    for v1, v2 in combinations(vertices, 2):
        if hamming_distance(v1[1], v2[1]) == H:
            edges.append((v1[0], v2[0]))
    return edges

def generate_edges_maximum_H(n, Hmax):
    """
    needed for 'smallH_labels_permutation'
    ...
    """
    edges = [ (i,i) for i in range(2**n) ]
    for H in range(1,Hmax+1):
        edges = edges + generate_edges_fixed_H(n,H)
    return edges + [ (j,i) for (i,j) in edges ] # may want to clean up here (remove i,i edges)


def smallH_labels_permutation (transitions):
    """
    Reassign state labels in a way that minimizes 
    the Hamming beween input and output states.
    """
    Hmax = 0
    mapping = {}
    while len(mapping) == 0:
        Hmax = Hmax + 1
        GT = nx.DiGraph(transitions)
        n = int(np.log2(len(transitions))) # only for boolean network transitions
        GH = nx.DiGraph(generate_edges_maximum_H(n,Hmax))
        DiGM = isomorphism.DiGraphMatcher(GH, GT)
        if DiGM.subgraph_is_monomorphic():
            mapping = DiGM.mapping
    
    # Create a new list of edges with the updated labels
    new_transitions = [(mapping[i], mapping[j]) for (i, j) in transitions]
    sorted_transitions = sorted(new_transitions, key=lambda x: x[0])

    return Hmax, sorted_transitions
