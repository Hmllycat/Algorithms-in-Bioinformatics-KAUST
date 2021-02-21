"""
@BY: Yang LIU
@DATE: 07-10-2020
"""

from numpy import *
import sys
sys.setrecursionlimit(1500)


# store backtracking pointers
def lsc_backtrack(v, w):
    s = zeros([len(v)+1,len(w)+1])
    backtrack = full(shape=(len(v),len(w)),fill_value='XXX')
    for i in range(1,len(v)+1):
        for j in range(1, len(w)+1):
            match = 0
            if v[i-1] == w[j-1]:
                match = 1
            s[i, j] = max(s[i-1, j], s[i, j-1], s[i-1, j-1]+match)
            if s[i,j] == s[i-1,j]:
                backtrack[i-1, j-1] = "del"
            elif s[i, j] == s[i, j-1]:
                backtrack[i-1, j-1] = "ins"
            elif s[i, j] == s[i-1, j-1] + match:
                backtrack[i-1, j-1] = "mat"

    return backtrack 


# Input: Two strings s and t.
# Output: A longest common subsequence of s and t. (Note: more than one solution may exist, in which case you may output any one.)
def output_lsc(backtrack, v, i, j):

    if i == 0 or j == 0:
        return ""
    elif backtrack[i-1, j-1] == 'del':
        return output_lsc(backtrack, v, i-1, j)
    elif backtrack[i-1, j-1] == "ins":
        return output_lsc(backtrack, v, i, j-1)
    else:
        # print(v[i-1])
        return output_lsc(backtrack, v, i-1, j-1) + v[i-1]


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


# Input: An integer representing the starting node to consider in a graph, followed by an integer representing the ending node to consider, followed by a list of edges in the graph. The edge notation "0->1:7" indicates that an edge connects node 0 to node 1 with weight 7.  You may assume a given topological order corresponding to nodes in increasing order.
# Output: The length of a longest path in the graph, followed by a longest path. (If multiple longest paths exist, you may return any one.)
def lsc_DAG(start, end, graph, graph_lsc):
    max_value = {}
    max_value[start] = 0
    path = {}
    path[start] = "0"
    s = topological_ordering(graph)
    # print(s)
    start_index = s.index(start) + 1
    end_index = s.index(end) + 1
    s = s[start_index : end_index]
    # print(s)
    # for node in s.copy():
    #     if node not in graph_lsc.keys():
    #         s.remove(node)
    # print(graph_lsc['29'])
    for node in s:
        parental_node = [i[0] for i in graph_lsc[node]]
        admissible_parental_node = [i for i in parental_node if i in path.keys()]
        if len(admissible_parental_node) > 0:
            # print(node)
            # print(graph_lsc[node])
            max_value[node] = 0
            for j in graph_lsc[node]:
                if j[0] in admissible_parental_node:
                    if j[1] + max_value[j[0]] > max_value[node]:
                        # print(path)
                        max_value[node] = j[1] + max_value[j[0]]
                        path[node] = path[j[0]] + "->" + node
                        # print(path[node])
                        # print(max_value[node])
    return max_value[end], path[end]


if __name__ == "__main__":   

    v = "AACCTTGG"
    w = "ACACTGTGA"
    backtrack = lsc_backtrack(v, w)
    # print(backtrack)
    i = len(v)
    j = len(w)
    print(output_lsc(backtrack, v, i, j))
    
    # with open("C:/Users/树下的猫/Downloads/dataset_369316_7 (4).txt") as file:
    #     graph = {}
    #     graph_lsc = {}
    #     for line in file:
    #         info = line.replace("\n",'').split("->")
    #         key = info[0]
    #         value = info[1].split(":")[0]
    #         if key not in graph.keys():
    #             graph[key] = [value]
    #         else:
    #             graph[key].append(value)
    #         key1 = info[1].split(":")[0]
    #         weight = int(info[1].split(":")[1])
    #         value1 = [key]
    #         value1.append(weight)
    #         if key1 not in graph_lsc.keys():
    #             graph_lsc[key1] = [value1]
    #         else:
    #             graph_lsc[key1].append(value1)
    # start = "0"
    # end = "49"
    # print(lsc_DAG(start, end, graph, graph_lsc))     