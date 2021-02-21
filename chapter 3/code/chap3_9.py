"""
@BY: Yang LIU
@DATE: 21-09-2020
"""

import random


adjacency_list = {}
if_edge_visited = {}

def check_edge_visited():
    """check if all the edges have been visited"""
    for value in if_edge_visited.values():
        if 0 in value:
            return False
    return True


def read_in_relations():
    
    for item in input_relations:
        source, neighbors = item.split(" -> ")        # example: source: 2, neighbors = [1, 6] 
        neighbors = neighbors.split(",")

        adjacency_list[source] = neighbors        # the key, value are node and its destination nodes
        if_edge_visited[source] = [0] * len(neighbors)        # 0 represent that the edge has not been visited


def find_cycle(start_point):
    
    node_list = [start_point]    # store nodes
    while True:
        cur_node = node_list[-1]        # current node
        neighbors = adjacency_list[cur_node]        # the neighbors leaves from the current nodes
        for neighbor_idx in range(len(neighbors)):        # for each child node, there is a index, visit accordingly
            if if_edge_visited[cur_node][neighbor_idx] == 0:            # if not visited, take it as the next node
                if_edge_visited[cur_node][neighbor_idx] = 1                # change the visited stage
                node_list.append(neighbors[neighbor_idx])                # add this node to node sequence
                break                # leave for cycle
        
        if node_list[-1] == start_point:        # the added node is the start node, use it to explore a cycle, return
            return node_list


def find_node(node_list):
    """find another start node"""
    last_start_point = node_list[0]

    for i in range(len(node_list)):    # find the index of next start node 
        if 0 in if_edge_visited[node_list[i]]:
            return i


def find_euler():
    
    idx = random.randint(0, len(adjacency_list)-1)
    start_point = list(adjacency_list.keys())[idx]
    node_list = []

    while True:    # until all the edges have been visited, finish
        node_list.extend(find_cycle(start_point))        # continue find other cycles
        
        if check_edge_visited() == True:
            return node_list

        restart_index = find_node(node_list)        # find next start node
        start_point = node_list[restart_index]

        if restart_index == 0:        # store the results
            node_list = node_list[:-1]
        node_list = node_list[restart_index : ] + node_list[1 : restart_index]
        

# find out the unbalanced prenode and unbalanced nextnode, update the dic to enable a eulerian_cycle
def balance_list():

    global unbalanced_next_node, unbalanced_pre_node
    out = {}   # form a dict to store the number of edges get into a node
    for key in adjacency_list.keys():
        for value in adjacency_list[key]:
            if value not in out:
                out[value] = 1
            else:
                out[value] += 1

    for key in adjacency_list.keys():
        if key not in out.keys():
            out[key] = 0

    for key in out.keys():
        if key not in adjacency_list.keys():
            adjacency_list[key] = []
            if_edge_visited[key] = []

    for key in out.keys():
        if key not in adjacency_list.keys():
            unbalanced_pre_node = key   # if no edge leaves the node, the node is a unbalanced prenode.
        elif len(adjacency_list[key]) < out[key]:
            unbalanced_pre_node = key    # if the number of edges go into a node is more than the number of edges leave the node, the node is a unbalanced prenode.
        elif len(adjacency_list[key]) > out[key]:
            unbalanced_next_node = key   # if the number of edges go into a node is more than the number of edges leave the node, the node is a unbalanced nextnode.

    adjacency_list[unbalanced_pre_node].append(unbalanced_next_node)  # add the unbalance value for dict so that the dict is balanced
    if_edge_visited[unbalanced_pre_node].append(0)    # add an edge check accordingly 
    return


# find the eulerian path of a given dict
def euler_path():

    cycle = find_euler()
    index_list = []  # this list is used to store all the index that unbalanced prenode occur
    for index, nodes in enumerate(cycle):
        if (nodes == unbalanced_pre_node) and (index != len(cycle) - 1):
            index_list.append(index)
    for index in index_list:
        if cycle[index + 1] == unbalanced_next_node:
            idx = index    # idx is the index of the unbalanced prenode that have edge leave for unbalanced nextnode
    path = cycle[idx + 1 : ] + cycle[1 : idx + 1]

    return path


# the key is the first (k-1)elements and value is the last (k-1)elements of given kmer, a key could have many values.
def form_multidic(kmers, k):

    dic = {}
    for kmer in kmers:
        a = kmer[0][0:k-1] + kmer[1][0:k-1]
        b = kmer[0][1:k] + kmer[1][1:k]
        if a in dic.keys():
            dic[a].append(b)
        else:
            dic[a] = [b]

    return dic


# The overlap graph Overlap(Patterns), in the form of an adjacency list.    
def de_bruijn_graph_from_kmers(kmers, k):

    dic = form_multidic(kmers, k)
    output = []
    for preffix in dic.keys():
        suffixs = dic[preffix]
        if len(suffixs) == 1:
            output.append(preffix + " -> " + suffixs[0])
        else:
            result = preffix + " -> " 
            for suffix in suffixs:
                result += (suffix + ",")
            result = result[:-1]
            # print(result)
            output.append(result)       
    return output


# basically take the first as it is, then take the "new" addition (the last letter) from the rest
def string_reconstruction(patterns):
    string = patterns[0]
    for i in range(1, len(patterns)):
        string += patterns[i][-1]
    return string


def string_spelled_by_gapped_patterns(gappedpattens, k, d):
    first_patterns = []
    second_patterns = []
    for pattern in gappedpattens:
        first_patterns.append(pattern[0])   # the sequence of initial k-mers from GappedPatterns
        second_patterns.append(pattern[1])   # the sequence of terminal k-mers from GappedPatterns
    prefix_string = string_reconstruction(first_patterns)
    suffix_string = string_reconstruction(second_patterns)
    for i in range(k+d+1, len(prefix_string)):
        if prefix_string[i] != suffix_string[i-k-d]:
            prefix_string[i] = suffix_string[i-k-d]
    prefix_string = ''.join(prefix_string)
    suffix_string = ''.join(suffix_string)
    return  prefix_string+suffix_string[-(k+d):]


if __name__ == "__main__":

    with open("../data/dataset_369274_16.txt") as file:
        patterns = []
        for line in file:
            line = line.replace('\n','').split("|")
            patterns.append(line)
    k = 50
    d = 200
    input_relations = de_bruijn_graph_from_kmers(patterns, k)
    read_in_relations()
    balance_list()
    gappedpattens = []
    path = euler_path()
    for i in path:
        gappedpattens.append([i[:k-1],i[k-1:]])
    print(string_spelled_by_gapped_patterns(gappedpattens, k, d))