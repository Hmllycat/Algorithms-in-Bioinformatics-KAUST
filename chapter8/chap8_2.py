"""
@BY: Yang LIU
@DATE: 27-10-2020
"""

import numpy as np


# Input:  An integer n followed by the adjacency list of a weighted tree with n leaves.
# Output: An n x n matrix (di,j), where di,j is the length of the path between leaves i and j.
def distances_between_leaves(n, leaves, graph_lsc):

    score_dic = {}
    for start_leaf in leaves.copy():
        leaves.remove(start_leaf)
        start_child = [i[0] for i in graph_lsc[start_leaf]]
        visited_internal_node = start_child.copy()
        visited_internal_node.append(start_leaf)
        scores = [i[1] for i in graph_lsc[start_leaf]]
        while len(start_child) > 0:
            # print(start_child)
            for node in start_child.copy():
                # print(node)
                idx = start_child.index(node)
                start_child.remove(node)
                if node in leaves:                    
                    score_dic[(start_leaf, node)] = scores[idx]
                    scores.pop(idx)
                else:
                    next_child = [i[0] for i in graph_lsc[node] if i[0] not in visited_internal_node]
                    # print(next_child)
                    next_score = [i[1] + scores[idx] for i in graph_lsc[node] if i[0] not in visited_internal_node]
                    start_child.extend(next_child)
                    scores.pop(idx)
                    scores.extend(next_score)
                    visited_internal_node.append(node)

    score_matrix = np.zeros([n, n])
    for key in score_dic.keys():

        i = int(key[0])
        j = int(key[1])
        score_matrix[i, j] = score_dic[key]
        score_matrix[j, i] = score_dic[key]
    return score_matrix


if __name__ == "__main__":   

    with open("C:/Users/树下的猫/Downloads/dataset_369348_12 (2).txt") as file:
        graph_lsc = {}
        for line in file:
            info = line.replace("\n",'').split("->")
            key = info[0]
            key1 = info[1].split(":")[0]
            weight = int(info[1].split(":")[1])
            value1 = [key]
            value1.append(weight)
            if key1 not in graph_lsc.keys():
                graph_lsc[key1] = [value1]
            else:
                graph_lsc[key1].append(value1)
        leaves = [i for i in graph_lsc.keys() if len(graph_lsc[i]) == 1]

    n = 32
    result = distances_between_leaves(n, leaves, graph_lsc)
    with open("D:/bioinformatics homework/chapter8/8_2result.txt", "w") as output:
        for i in result:
            print(i)
            output.write("%s\n"%i)