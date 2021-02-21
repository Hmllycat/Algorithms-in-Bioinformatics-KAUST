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
    return trie, node_pairs


# Input: A string Text.
# Output: The edge labels of SuffixTree(Text). You may return these strings in any order.
def suffix_tree_construction(tree, node_pairs, text):
    
    paths = []
    in_nodes = {}
    expanded_nodes = []
    for pair_node in tree.keys():
        if pair_node[0] in in_nodes.keys():
            in_nodes[pair_node[0]] += 1
            expanded_nodes.append(pair_node[0])
        else:
            in_nodes[pair_node[0]] = 1

    root_child_nodes = [0]
    terminal_node = [str(i) for i in range(len(text))]
    # print(terminal_node)
    while len(root_child_nodes) > 0:
        node = root_child_nodes[0]
        root_child_nodes.remove(node)
        edges = [(node, i) for i in node_pairs[node].copy()]
        # print(edges)
        for edge in edges.copy():
            non_branching_path = [edge]
            while edge[1] in in_nodes.keys():
                if edge[1] in expanded_nodes or edge[1] in terminal_node:
                    root_child_nodes.append(edge[1])
                    break                   
                else:
                    extende_edge = node_pairs[edge[1]]
                    edge = (edge[1], extende_edge[0])
                    non_branching_path.append(edge)
            paths.append(non_branching_path)
    output = []
    for path in paths:
        symbol = ""
        # print(paths)
        for edge in path:
            symbol += tree[edge]
        # print(symbol)
        output.append(symbol)
    return output


if __name__ == "__main__":   

    text = "ATAAATG$"
    trie, node_pairs = modified_suffix_trie_construction(text)
    # print(trie)
    print(suffix_tree_construction(trie, node_pairs, text))
    # output = suffix_tree_construction(trie, node_pairs)
    # with open("D:/bioinformatics homework/chapter9/result_9_4_1.txt", "w") as Output:
    #     for symbol in output:
    #         Output.write('%s\n'%(symbol))