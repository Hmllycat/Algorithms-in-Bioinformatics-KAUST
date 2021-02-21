"""
@BY: Yang LIU
@DATE: 07-10-2020
"""

# Input: The adjacency list of a graph (with nodes represented by integers).
# Output: A topological ordering of this graph.
def topological_ordering(graph):
    lis = []
    outgoing_edge = []
    for i in graph.values():
        outgoing_edge.extend(i)
    candidates = [i for i in graph.keys() if i not in outgoing_edge]

    while len(candidates) > 0:
        # print(candidates)
        # print(graph)
        a = candidates[0]
        lis.append(a)
        candidates.pop(0)
        if a in graph.keys():
            out_node = graph[a].copy()
            for b in out_node:
                graph[a].remove(b)
                outgoing_edge = []
                for i in graph.values():
                    outgoing_edge.extend(i)
                    # print(i)
                if b not in outgoing_edge:
                    candidates.append(b)
    if len(outgoing_edge) > 0:
        return "the input is not a DAG"
    else:
        return lis


if __name__ == "__main__":   

    # graph = {0:[1],1:[2],3:[1],4:[2]}
    # print(topological_ordering(graph))
    with open("C:/Users/树下的猫/Downloads/dataset_369325_3 (1).txt") as file:
        graph = {}
        for line in file:
            info = line.replace("\n",'').split(" -> ")
            key = info[0]
            value = info[1].split(",")
            graph[key] = value
    print(topological_ordering(graph))   