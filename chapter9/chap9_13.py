"""
@BY: Yang LIU
@DATE: 16-11-2020
"""


# Input: A string Text followed by a collection of strings Patterns.
# Output: All starting positions in Text where a string from Patterns appears as a substring.
def multi_pattern_match_text(patterns, text):
    
    trie = {}
    find_next_node = {}
    existed_node = [0]
    node_pairs = {}
    leaves = []
    pattern_length = len(patterns[0])
    for i in range(len(patterns)):    # build a tree for patterns
        pattern = patterns[i]
        current_node = 0
        for j in range(pattern_length):
            current_symbol = pattern[j]
            if current_node not in node_pairs:
                node_pairs[current_node] = []
            if (current_node, current_symbol) in find_next_node:
                current_node = find_next_node[(current_node, current_symbol)]
                # print(current_node)
            else:
                new_node = existed_node[-1] + 1
                # print(current_node, new_node, current_symbol)
                existed_node.append(new_node)
                trie[(current_node, new_node)] = current_symbol
                find_next_node[(current_node, current_symbol)] = new_node
                node_pairs[current_node].append(new_node)
                current_node = new_node
        leaves.append(current_node)
    # print(trie)
    positions = []
    text_length = len(text)
    for i in range(text_length - pattern_length + 1):
        current_fragment = text[i:i+pattern_length]
        current_node = 0
        for j in range(pattern_length):
            current_symbol = current_fragment[j]
            if (current_node, current_symbol) in find_next_node:
                current_node = find_next_node[(current_node, current_symbol)]
            else:
                break
            if current_node in leaves:
                positions.append(i)
        
    return positions


if __name__ == "__main__":   

    text = "AATCGGGTTCAATCGGGGT"
    patterns = ["ATCG", "GGGT"]
    print(multi_pattern_match_text(patterns, text))
