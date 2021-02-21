"""
@BY: Yang LIU
@DATE: 23-10-2020
"""

from math import ceil


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


def cycle_to_chromosome(nodes):

    chromosome = [0]*(int(len(nodes)/2))
    for j in range(int(len(nodes)/2)):
        if nodes[2*j] < nodes[2*j+1]:
            chromosome[j] = ceil(nodes[2*j+1]/2)
        else:
            chromosome[j] = ceil(-nodes[2*j]/2)
    return chromosome


def colored_edge(P):

    edges = []
    for chromosome in P:
        nodes = chromosome_to_cycle(chromosome)
        # print(nodes)
        for j in range(1, len(chromosome)):
            edges.append((nodes[2*j-1], nodes[2*j]))
        edges.append((nodes[-1],nodes[0]))
    return edges


def find_cycle(genome_graph):

    cycles = []
    multi_cycle = []

    for i in range(len(genome_graph)):
        tuple_to_list = list(genome_graph[i])
        multi_cycle.extend(tuple_to_list)

    j = 0
    while len(multi_cycle) > 0:
        print(multi_cycle)
        print(j+1)
        if multi_cycle[0] != j+1:
            idx = multi_cycle.index(j+1)
            sequence = [multi_cycle[idx]]
            sequence.extend(multi_cycle[:idx])
            cycles.append(sequence)
            j += idx+1
            del multi_cycle[:idx+1]
        else:
            idx = multi_cycle.index(j+2)
            sequence = [multi_cycle[idx]]
            sequence.extend(multi_cycle[:idx])
            cycles.append(sequence)
            j += idx+1
            del multi_cycle[:idx+1] 

    return cycles


def graph_to_genome(genome_graph):

    P = []
    cycles = find_cycle(genome_graph)
    for cycle_nodes in cycles:
        chromosome = cycle_to_chromosome(cycle_nodes)
        P.append(chromosome)
    return P


def two_break_distance(P, Q):

    red_edge = colored_edge(P)
    blue_edge = colored_edge(Q)
    edge = red_edge
    edge.extend(blue_edge)
    dic = {}
    for i in edge:
        if i[0] not in dic.keys():
            dic[i[0]] = [i[1]]
        else:
            dic[i[0]].append(i[1])

        if i[1] not in dic.keys():
            dic[i[1]] = [i[0]]
        else:
            dic[i[1]].append(i[0])
    # print(dic)
    cycle_number = 0
    while True:
        key_node = [i for i in dic.keys() if len(dic[i]) > 0]
        if len(key_node) == 0:
            break
        start = key_node[0]
        next = dic[start][0]
        dic[start].remove(next)
        dic[next].remove(start)
        cycle_number += 1
        # print(start, next)
        while next != start:
            # print(dic)
            next1 = dic[next][0]
            dic[next].remove(next1)
            dic[next1].remove(next)
            next = next1
            # print(next)

    twb_distance = len(red_edge)/2 - cycle_number
    return twb_distance
    

if __name__ == "__main__":

    P = [(+1, +2, +3, +4, +5, +6)]
    Q = [(+1, -3, -6, -5),(+2, -4)]
    print(two_break_distance(P, Q))
    