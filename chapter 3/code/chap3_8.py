"""
@BY: Yang LIU
@DATE: 21-09-2020
"""

import itertools


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
    
    start_point = list(adjacency_list.keys())[0]
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
def form_multidic(kmers):

    dic = {}
    for kmer in kmers:
        a = kmer[0:len(kmer)-1]
        b = kmer[1:len(kmer)]
        if a in dic.keys():
            dic[a].append(b)
        else:
            dic[a] = [b]

    return dic


# The overlap graph Overlap(Patterns), in the form of an adjacency list.    
def de_bruijn_graph_from_kmers(kmers):

    dic = form_multidic(kmers)
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


# reconstruct the genome sequence given a sequential kmers
def path_to_genome(path):
    text = path[0]
    length = len(path)
    for i in range(1, length):
        text += path[i][-1]
    return text


def string_reconstruction(patterns):
    read_in_relations()
    balance_list()
    path = euler_path()
    text = path_to_genome(path)
    return text


# return the set of all 2^k binary k-mers
def binary_string_k(k):
    a = []
    for i in itertools.product("10", repeat = k):
        a.append("".join(i))
    return a


def k_universal_circular(k):
    read_in_relations()
    path = find_euler()
    text = path_to_genome(path)[:-(k-1)]
    return text


if __name__ == "__main__":

    # with open("../data/dataset_369273_2.txt") as file:
    #     input_relations = []
    #     for line in file:
    #         line = line.replace('\n','')
    #         input_relations.append(line)
    # read_in_relations()
    # euler_cycle = find_euler()
    # for index in range(len(euler_cycle) - 1):
    #     print(euler_cycle[index], end="->")
    # print(euler_cycle[-1])    


    # with open("../data/dataset_369273_6.txt") as file:
    #     input_relations = []
    #     for line in file:
    #         line = line.replace('\n','')
    #         input_relations.append(line)
    # read_in_relations()
    # balance_list()
    # path = euler_path()
    # for index in range(len(path) - 1):
    #     print(path[index], end="->")
    # print(path[-1])


    # with open("../data/dataset_369273_7.txt") as file:
    #     patterns = []
    #     for line in file:
    #         line = line.replace('\n','')
    #         patterns.append(line)
    # input_relations = de_bruijn_graph_from_kmers(patterns)
    # print(string_reconstruction(patterns))


    k = 8
    patterns = binary_string_k(k)
    input_relations = de_bruijn_graph_from_kmers(patterns)
    print(k_universal_circular(k))