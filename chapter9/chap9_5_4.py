"""
@BY: Yang LIU
@DATE: 15-11-2020
"""


def longest_shared_substring(text1, text2):
    
    trie = {}
    find_next_node = {}
    existed_node = [0]
    node_pairs = {}
    length = len(text1)
    for i in range(length):
        current_node = 0
        for j in range(i, length):
            current_symbol = text1[j]
            if current_node not in node_pairs:
                node_pairs[current_node] = []
            if (current_node, current_symbol) in find_next_node:
                if find_next_node[(current_node, current_symbol)] not in node_pairs[current_node]:
                    node_pairs[current_node].append(find_next_node[(current_node, current_symbol)])
                old_node = current_node
                current_node = find_next_node[(current_node, current_symbol)]
                # print(current_node)
            else:
                new_node = existed_node[-1] + 1
                # print(current_node, new_node, current_symbol)
                existed_node.append(new_node)
                trie[(current_node, new_node)] = current_symbol
                find_next_node[(current_node, current_symbol)] = new_node
                node_pairs[current_node].append(new_node)
                old_node = current_node
                current_node = new_node
    
    trie2 = {}
    length = len(text2)
    for i in range(length):
        current_node = 0
        for j in range(i, length):
            current_symbol = text2[j]
            if current_node not in node_pairs:
                node_pairs[current_node] = []
            if (current_node, current_symbol) in find_next_node:
                if find_next_node[(current_node, current_symbol)] not in node_pairs[current_node]:
                    node_pairs[current_node].append(find_next_node[(current_node, current_symbol)])
                old_node = current_node
                current_node = find_next_node[(current_node, current_symbol)]
                # print(current_node)
            else:
                new_node = existed_node[-1] + 1
                # print(current_node, new_node, current_symbol)
                existed_node.append(new_node)
                trie2[(current_node, new_node)] = current_symbol
                find_next_node[(current_node, current_symbol)] = new_node
                node_pairs[current_node].append(new_node)
                old_node = current_node
                current_node = new_node

            trie2[(old_node, current_node)] = current_symbol
    # print(trie)
    # print(trie2)
    considered_edges = [nodepair for nodepair in trie.keys() if nodepair not in trie2.keys()]
    # print(considered_edges)
    dic = {}
    for edge in considered_edges:
        dic[edge[1]] = edge[0]
    goal_nodes = list(dic.keys())
    paths = []
    # print(dic)
    for node in goal_nodes:
        path = []
        while node in dic.keys():
            path.append((dic[node], node))
            node = dic[node]
        paths.append(path.copy())

    output = text1
    for path in paths:
        symbol = ""
        for edge in path:
            symbol += trie[edge]
        symbol = symbol[::-1]
        # print(symbol)
        if len(symbol) < len(output) and symbol not in text2:
            output = symbol

    return output


if __name__ == "__main__":   

    text1 = "AAAATAAACAAAGAATTAATCAATGAACTAACCAACGAAGTAAGCAAGGATATACATAGATTTATTCATTGATCTATCCATCGATGTATGCATGGACACAGACTTACTCACTGACCTACCCACCGACGTACGCACGGAGAGTTAGTCAGTGAGCTAGCCAGCGAGGTAGGCAGGGTTTTCTTTGTTCCTTCGTTGCTTGGTCTCTGTCCCTCCGTCGCTCGGTGTGCCTGCGTGGCTGGGCCCCGCCGGCGCGGGGAAACGGAAATGATGGGAGTTGCTACATAGCTGTACTGGTGACTGCCCCCGGAAGTCTCTAGCTATCTGAAAACCTCCGTGGACGTCCAGGCTGATTTCCGCCAAAAGTCCCCTCGAACAGATCAAGGCTTTCACTAGATCTTACCTAATTACCGCATCTTATTCGGCTCGCCTGCGCGTATCATCAGCAGGTGCGCCTTGATCCCCTGAGGTCTGAGACGCGACGGCCAGTCCCACGGAATAGCAACCAATGCCCAGCGATGTAAGCCTTCGGCGAAATACAGACTGGCTCTCGCACGTGAAACGTACTCAAAAATTCGCGACTAGCAGTACCTTAAAGGCGGGAGCGGGCGTCGCGGGAACCCCACGAAACACATTCGACGAGCACCTGTCACGGCCAGCTG"
    text2 = "AAAATAAACAAAGAATTAATCAATGAACTAACCAACGAAGTAAGCAAGGATATACATAGATTTATTCATTGATCTATCCATCGATGTATGCATGGACACAGACTTACTCACTGACCTACCCACCGACGTACGCACGGAGAGTTAGTCAGTGAGCTAGCCAGCGAGGTAGGCAGGGTTTTCTTTGTTCCTTCGTTGCTTGGTCTCTGTCCCTCCGTCGCTCGGTGTGCCTGCGTGGCTGGGCCCCGCCGGCGCGGGGAAA"
    print(longest_shared_substring(text1, text2))