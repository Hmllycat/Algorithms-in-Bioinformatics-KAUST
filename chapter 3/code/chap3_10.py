"""
@BY: Yang LIU
@DATE: 26-09-2020
"""


adjacency_list = {}


def read_in_relations():
    
    for item in input_relations:
        source, neighbors = item.split(" -> ")        # example: source: 2, neighbors = [1, 6] 
        neighbors = neighbors.split(",")

        adjacency_list[source] = neighbors        # the key, value are node and its destination nodes
        

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


# return the list collection of all one-in-one-out nodes
def one_one_node():

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

    one_one_nodes = []
    for key in adjacency_list.keys():
        if len(adjacency_list[key]) == 1 and out[key] == 1:
            one_one_nodes.append(key)
    
    return one_one_nodes


# return the list of all the nodes of a graph
def node():
    nodes = list(adjacency_list.keys())
    for out_edges in adjacency_list.values():
        for out_edge in out_edges:
            nodes.append(out_edge)
    return nodes


# Generate the contigs from a collection of reads (with imperfect coverage)
def cotig_generation():
    read_in_relations()
    paths = []
    visited = []
    one_one_nodes = one_one_node()

    for v in adjacency_list.keys():
        if v not in one_one_nodes:
            visited.append(v)
            for w in adjacency_list[v]:
                nonbranchingpath = [v, w]
                while w in one_one_nodes:
                    nonbranchingpath.append(adjacency_list[w][0])
                    visited.append(w)
                    w = adjacency_list[w][0]
                paths.append(nonbranchingpath)
            
    for v in adjacency_list.keys():
        if (v not in visited) and (v in one_one_nodes):
            visited.append(v)
            isolated_cycle = [v]
            w = adjacency_list[v][0]
            while w in one_one_nodes:
                isolated_cycle.append(w)
                if w == v:
                    break
                w = adjacency_list[w][0]
            paths.append(isolated_cycle)
    
    output = []
    for path in paths:
        string = path[0]
        for i in range(1, len(path)):
            string += path[i][-1]
        output.append(string)

    return output 


if __name__ == "__main__":

    # with open("../data/dataset_369275_5.txt") as file:
    #     patterns = []
    #     for line in file:
    #         line = line.replace('\n','')
    #         patterns.append(line)
    patterns = ["ATG","ATG","TGT","TGG","CAT","GGA","GAT","AGA"]
    input_relations = de_bruijn_graph_from_kmers(patterns)
    print(cotig_generation())