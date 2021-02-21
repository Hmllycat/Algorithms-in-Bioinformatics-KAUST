"""
@BY: Yang LIU
@DATE: 11-11-2020
"""


def modified_suffix_trie_construction(text):
    
    trie = {}
    find_next_node = {}
    existed_node = [0]
    node_pairs = {}
    length = len(text)
    for i in range(length):
        current_node = 0
        for j in range(i, length):
            current_symbol = text[j]
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
        key = (old_node, current_node)
        # print(key)
        trie[(key[0], str(i))] = trie[key]
        node_pairs[key[0]].remove(key[1])
        node_pairs[key[0]].append(str(i))
        # print(trie, node_pairs)
        # print(key[1])
        if key[1] in node_pairs:
            # print(node_pairs[key[1]])
            for next_node in node_pairs[key[1]].copy():
                trie[(str(i), next_node)] = trie[(key[1], next_node)]
                # print(key[1], next_node, trie[(key[1], next_node)])
                find_next_node[(str(i), trie[(key[1], next_node)])] = next_node
                del find_next_node[(key[1], trie[(key[1], next_node)])]
                del trie[(key[1], next_node)]
            node_pairs[str(i)] = node_pairs[key[1]].copy()
            del node_pairs[key[1]]
        existed_node.remove(key[1])
        del trie[key]
        # print(trie)
    return trie


# Input: A string Text.
# Output: A longest substring of Text that appears in Text more than once.
def longest_repeat_problem(text):

    tree = modified_suffix_trie_construction(text)
    paths = []
    in_nodes = {}
    expanded_nodes = []
    for pair_node in tree.keys():
        if pair_node[0] in in_nodes.keys():
            in_nodes[pair_node[0]] += 1
            if pair_node[0] != 0:
                expanded_nodes.append(pair_node[0])
        else:
            in_nodes[pair_node[0]] = 1

    internal_terminal_node = [str(i) for i in range(len(text)) if str(i) in in_nodes]
    considered_nodes = internal_terminal_node + expanded_nodes
    considered_nodes = set(considered_nodes)
    # print(considered_nodes)
    backtrack_trie = {}
    backtrack_nodepairs = {}
    for key, value in tree.items():
        backtrack_trie[(key[1], key[0])] = value
        backtrack_nodepairs[key[1]] = key[0]
    # print(edges)
    for goal_node in considered_nodes.copy():
        edge = (goal_node, backtrack_nodepairs[goal_node])
        single_path = [edge]
        while edge[1] != 0:
            edge = (edge[1], backtrack_nodepairs[edge[1]])
            single_path.append(edge)
        if len(single_path) > len(paths):
            paths = single_path.copy()

    symbol = ""
    for edge in paths:
        symbol += backtrack_trie[edge]
    # print(symbol)
    symbol = symbol[::-1]
        
    return symbol


if __name__ == "__main__":   

    text = "ATTTACACCTTTCTTCAGCTGTGGCCCGCTACCTACGATGCGCGGCAGTAGACCGGTGACGATACATATAGCGCCTGCGTAGAAGTTATCTGGACTAGTACAGGACACATGTTAGCGAACGGTCTCCCTAACACACTTGCCGCTGGAAGGGAGGGGTAGCTCCTATTGCCCCGAGGCATGCCTGCCCGATGTAATCCGGCAGGAGTCCTGCAGCCACGAAGTAATGAATACCTCCCAACTATGGCGAAATCCAGTTAGGCAGATTGCGCGGACACGATCGTGGGAGAAACGTCTTTCTGTTTTGCTAGACCTATATAGTCAATAGCTCCTATTGCCCCGAGGCATGCCTGCCCGATGTAATCCGGCAGGAGTCCTGCAGCCACGAAGTAATGAATACCTCCCAACTATGGCGTCGAGCAGGTGGGGTTATGAGTTCGACTCTCTGGGCGTTCAGATAAAGCGGTTATTGGAATTACAGCGCCTGGCTCGAGTCGGGCCGCCAAACTCCGAGGTCAACACACGCTCGATTCGAAGAGGGGCGATCAATGTTGCGCGTTCAAGGGTCTTTATTCTCACGTACTAGTCGGGCGAGACTCAAGTGAGTATGGCTTCCGGTGGTCAAACCATCCCTATACGTGGAAGACGCAGAAGGTCTCTAGCTGTTCGGCGTGTGCCCTCCGGTAAATCTGCCTCTCCTACCTCGCTGCAACACGTCTCTACTAAAAGATAAAGTAACAAGGACGGGAAAGATCACTCTCAATATGTCACGGAGGCATTTACCGTCCCGTCTCAAGTGGGCCGGACAAATCTATTAAGTCGGTAAAGCATCTTAGCTCCTATTGCCCCGAGGCATGCCTGCCCGATGTAATCCGGCAGGAGTCCTGCAGCCACGAAGTAATGAATACCTCCCAACTATGGCGACTAGACTATTATTGGGATGATGGGATAACCCCTTCTCGGCTATTGCATGTATGCTCTATAGATCGTAGGTAATGTTGAAAATCTTCATATGCGGTCCGTCTGGGATACACCCCAGAAATACTGGGTACATCCGGCACATCACAAAATTTAAGCAACTCCGATTTGCATACAAATCGCCGAGCTCGACGCGTCACAATAGAGGTTGTTCGTAGCAGGCGCTGGGCCCTACTGCTAAATGGAATTATCCTATCGCGATTGCGTTGTGGGTTGGCTCACCAAGTAGTACCCCCCAGAAGGTTACGAAGAAGTACGTTCCGGCGATAATCGTAGCAGCGATTCTTGAGAC"
    print(longest_repeat_problem(text))