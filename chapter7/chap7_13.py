"""
@BY: Yang LIU
@DATE: 24-10-2020
"""

from math import ceil


def two_break_on_genomegraph(genome_graph, i1,i2, i3, i4):

    if (i1, i2) in genome_graph:
        idx1 = genome_graph.index((i1, i2))
        genome_graph.remove((i1, i2))
        genome_graph.insert(idx1, (i4, i2))
    else:
        idx1 = genome_graph.index((i2, i1))
        genome_graph.remove((i2, i1))
        genome_graph.insert(idx1, (i2, i4))
    if (i3, i4) in genome_graph:
        idx2 = genome_graph.index((i3, i4))
        genome_graph.remove((i3, i4))
        genome_graph.insert(idx2, (i3, i1))
    else:
        idx2 = genome_graph.index((i4, i3))
        genome_graph.remove((i4, i3))
        genome_graph.insert(idx2, (i1, i3))

    reverse = []
    # print(genome_graph)
    for i in range(idx2+1,idx1+1):
        reverse.append((genome_graph[i][1], genome_graph[i][0]))
    # print(reverse)
    if idx1 < idx2:
        idx3 = idx2
        idx2 = idx1
        idx1 = idx3
    if (i2, i4) in genome_graph:
        reverse = reverse
        genome_graph = [genome_graph[:idx2+1]+genome_graph[idx1+1:], reverse]
    else:
        reverse = genome_graph[idx2:idx1]
        genome_graph = [genome_graph[:idx2]+genome_graph[idx1:], reverse]
    return genome_graph


def cycle_to_chromosome(nodes):

    chromosome = [0]*(int(len(nodes)/2))
    for j in range(int(len(nodes)/2)):
        if nodes[2*j] < nodes[2*j+1]:
            chromosome[j] = ceil(nodes[2*j+1]/2)
        else:
            chromosome[j] = ceil(-nodes[2*j]/2)
    return chromosome


def chromosome_to_cycle(chromosome):

    nodes = [0]*(len(chromosome)*2+1)
    for j in range(1, len(chromosome)+1):
        i = chromosome[j-1]
        if i > 0:
            nodes[2*j-1] = 2*i - 1
            nodes[2*j] = 2*i
        else:
            nodes[2*j-1] = -2*i
            nodes[2*j] = -2*i - 1
    nodes.remove(0)
    return nodes


def colored_edge(P):

    edges = []
    for chromosome in P:
        nodes = chromosome_to_cycle(chromosome)
        # print(nodes)
        for j in range(1, len(chromosome)):
            edges.append((nodes[2*j-1], nodes[2*j]))
        edges.append((nodes[-1],nodes[0]))
    return edges


def graph_to_genome(genome_graph):

    P = []
    cycles = []
    
    for cycle in genome_graph:
        tuple_to_list = []
        for pair in cycle:
            tuple_to_list.append(pair[0])
            tuple_to_list.append(pair[1])
        # print(tuple_to_list)
        tuple_to_list = [tuple_to_list[-1]] + tuple_to_list[:len(tuple_to_list)]
        cycles.append(tuple_to_list)
    # print(cycles)
    for cycle_nodes in cycles:
        chromosome = cycle_to_chromosome(cycle_nodes)
        P.append(chromosome)
    return P


def two_break_on_genome(P, i1, i2, i3, i4):

    genome_graph = colored_edge(P)
    # print(genome_graph)
    genome_graph = two_break_on_genomegraph(genome_graph, i1, i2, i3, i4)
    # print(genome_graph)
    P = graph_to_genome(genome_graph)
    return P

# def add(P):
#     string = ""
#     for i in P:
#         if i < 0:
#             string += str(i) + " "
#         else:
#             string += "+" + str(i) + " "
#     return string


if __name__ == "__main__":

    # genome_graph = [(2, 4), (3, 5), (6, 8), (7, 10), (9, 11), (12, 14), (13, 15), (16, 18), (17, 20), (19, 21), (22, 23), (24, 26), (25, 28), (27, 30), (29, 31), (32, 34), (33, 36), (35, 37), (38, 39), (40, 42), (41, 43), (44, 45), (46, 47), (48, 50), (49, 51), (52, 54), (53, 55), (56, 58), (57, 59), (60, 62), (61, 63), (64, 66), (65, 68), (67, 70), (69, 72), (71, 74), (73, 75), (76, 77), (78, 80), (79, 81), (82, 84), (83, 85), (86, 87), (88, 89), (90, 92), (91, 93), (94, 95), (96, 98), (97, 100), (99, 102), (101, 104), (103, 105), (106, 107), (108, 110), (109, 112), (111, 113), (114, 116), (115, 118), (117, 120), (119, 122), (121, 123), (124, 125), (126, 127), (128, 129), (130, 131), (132, 134), (133, 1)]
    # i1 = 35
    # i2 = 37
    # i3 = 13
    # i4 = 15
    # print(two_break_on_genomegraph(genome_graph, i1, i2, i3, i4))

    P = [(-24,-28,+60,-23,-5,-18,+19,-3,-61,-30,+13,+16,-26,+15,-65,+38,+4,-34,-57,-29,-48,+11,-64,+21,-32,-55,-41,+42,+6,+56,+49,+2,-46,-7,-35,-53,-68,+33,+14,-9,-43,-8,-50,+20,-54,+39,+66,+63,+22,+10,-31,-44,+12,-59,+1,+62,+36,-37,+47,-58,+25,-52,+67,+45,-40,+17,+51,-27)]
    i1 = 4
    i2 = 92
    i3 = 110
    i4 = 63
    print(two_break_on_genome(P, i1, i2, i3, i4))
    # result = two_break_on_genome(P, i1, i2, i3, i4)
    # with open("D:/bioinformatics homework/chapter 7/7_13_result.txt","w") as output:
    #     for reversal in result:
    #         string = add(reversal)
    #         string = string[:-1]
    #         output.write("%s)("%string)