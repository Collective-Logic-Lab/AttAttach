import random

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
    
    if sum(rel_sizes) != 1:
        return print('The sum of the relative basin sizes is not 1.')
    else:
    
        # generate the individual basins
        t = []
        for i in range(len(landscape_structure)):
            t.append(transitions(lengths[i], sizes[i]))

        # join them with the sequential relabeling 
        all_t = []
        for i in range(len(t)):
            all_t = join_transitions(all_t,t[i])
    
        return labels_permutation (all_t)