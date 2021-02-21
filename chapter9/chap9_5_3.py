"""
@BY: Yang LIU
@DATE: 14-11-2020
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
    considered_edges = [nodepair for nodepair in trie2.keys() if nodepair in trie.keys()]
    dic = {}
    for edge in considered_edges:
        dic[edge[1]] = edge[0]
    goal_nodes = [i for i in dic.keys() if i not in dic.values()]
    longest_path = []
    # print(dic)
    for node in goal_nodes:
        path = []
        while node in dic.keys():
            path.append((dic[node], node))
            node = dic[node]
        if len(path) > len(longest_path):
            longest_path = path.copy()

    longest_path = longest_path[::-1]
    symbol = ""
    for edge in longest_path:
        symbol += trie2[edge]
        
    return symbol


if __name__ == "__main__":   

    text1 = "TGAATCGCATGCTCATACAATTGTGTATCATATGAAAACAAATATGTCGTGTCACTAAGGGGGTGCTGGATGATACAGAAGACACGACCCTCCCTTCGCCACGCACGCTTTTATCGGGAGGTAAGACGACTTCTAGAACCTAATGGATCCGGGTCCGAGCACCCGCAAGTTAGGTGGCTTATTAACCGTCGCATGGTAGACTAGTCAAGAAAGAGAAATAATCGCTATGAAGTACTCTCCACCGCAAGTGTAGGATACTTCTATGGCTCGCGTACGGCGCGGACTTGCAATAATCTCCCCGTCGTTCATTGTTTTGGTCCGCGCAGTCAGACGTGACCAATTATGATCTTTGAACTCTTTTTCATACAATCTCAGGGGCTCCTGCGCCGTTGTCAAGGTCGCATTCTGCACGTGGCTTGCTGTGGCTAACGAGGTCGGGCATACTCGTCTCGAGATATATTGGCAGATTACCAACGGTTATCGGTTGAGCCATGATAAGTATCCACGGAGAGGGATTGGCAGGATGTACATAGCTTAGTAACGCCCTTTGTGTACGGCTATAGAGGAATTATCACCAACACTCGATAGCCGCTAAGATATCGACGCACTCGACCAGTATCAAGCAAGGGTAAGCGACTTAGTTCAGTCGTGACACTATCTGCTGTAATGTTTATCTCAAGGTTACTTGACAAGTCGGATTCCCACACGGATTATGTCGTGGTTTAACCTGCGTCCGCGGTTGCCGTGTGAAGATCCCAGTCCCCGGCGAACATCCTCTCCAGAAGTATAGGGGGGTCTATTAGTGCCTTGCGAGATGCTAGGTGCAAGGCATCACTCCGTCTGCCGTCAATTAACGAGAAATTTTTCACAGGCCGTTAGATACCGGATACTCTCATCCCTTAGCGATAAGAGATGTAGATATCCACCCCCAATTTATTATAATTCAGACAGCCTCAAAGGTCTTCAAGCCAAAGCCAGGCCAAAGACCACTTGGGTATGT"
    text2 = "ACAAAGAACCTCCACTCGGGACGGTGTTGGGTGTCGAACATTTTGTACAATTTGGATACAACGTCTGGGCAACGGCCCGGATTGAATACAGTAGATCTCTGATCATTTGCATCGTGTGTTATCATTTAAACGCCGTGAGTCGGCTCCGGCAAACGTTACTTAGAGGCAGGGCTAATAAAGCGGCTCTGTCGGATTATTTACAAACGCTTGACATTCGCTTTAAAGTATGACCCTTGATTATTAGGAAGCACAAGGATTGTTTAAGGCAACCGGGCAGATCGCATATTTATAGAGGGTGTGTATCTTATCCTCTACAGTAACCCCAGTGCGGGCACGATCGGCGCTGGGTGTCCTACGTGAGAGGGGTTACTGCAAACTCTGTACCGGCTTTCTGCCACTTTCCCGCGGTATCGAAGAGCTCCTGAAATCAAACTCTTGTGTTCCTACCTCAAGGGCAGCTTCCGGCTGTAGTTCGATGAAGCGAACGCGGACTATAAACTTCCTTGCTCACGCTCACAGGAGTGTGAGGATAGGTAAATCGATCCGAGTTGCTCTCTGGAAGGCTTACTTCTCCTGAACCGATTTATATCACGGTTCAACCAACTATGGCTCCTAGCTGCCTGCGTCCTCGATGTATTTAATCAACTTTGCGAGAATCATTTGACTGATGTCACGCGCACCGTAAGCGGGAAGAGCTCATCTTCCAGTAGAATCCTCATTGTAAACTGGGTTGGCTATAAGAAAATCTCTCATCGCCACTTCCGCAGGTTTGCCGACATATATCGTCTGTTTTCCCCTCACTCTACATTTGTGAGGAGTTGTTATGAATTGTGAGACTTCTTAGCTGCCTGCGGTTACGGATACTCTGCAAGACGCCTAGAGGTGGACAAAGCTCGCACACTGGACTGTTTGTGCTTAGGCAGAAGGTAGCCATAACGGGGGGAGAGATCGCTCCGCAGACTATCCGATGGTACGAAATAACAATAGCCTCCCCTAATAA"
    print(longest_shared_substring(text1, text2))