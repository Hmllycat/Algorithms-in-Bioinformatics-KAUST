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


def add(P):
    string = ""
    for i in P:
        if i < 0:
            string += str(i) + " "
        else:
            string += "+" + str(i) + " "
    return string


if __name__ == "__main__":

    # chromosome = (-1,-2,-3,+4,+5,+6,+7,-8,-9,-10,+11,+12,-13,+14,-15,-16,-17,+18,-19,-20,-21,-22,+23,+24,+25,+26,+27,+28,-29,+30,+31,+32,-33,+34,-35,-36,-37,+38,-39,-40,-41,-42,+43,-44,-45,+46,-47,+48,+49,-50,-51,+52,+53,+54,-55,+56,-57,-58,-59,+60,-61,-62,+63,-64,-65,-66)
    # print(chromosome_to_cycle(chromosome))

    # nodes = (1, 2, 4, 3, 6, 5, 7, 8)
    # print(cycle_to_chromosome(nodes))

    # P = [(+1, -2, -3),(+4, +5, -6)]
    # print(colored_edge(P))

    genome_graph = [(2, 4), (3, 6), (5, 1), (7, 9), (10, 12), (11, 8)]
    print(graph_to_genome(genome_graph))
    # result = graph_to_genome(genome_graph)
    # with open("D:/bioinformatics homework/chapter 7/7_12_result.txt","w") as output:
    #     for reversal in result:
    #         string = add(reversal)
    #         string = string[:-1]
    #         output.write("%s)("%string)