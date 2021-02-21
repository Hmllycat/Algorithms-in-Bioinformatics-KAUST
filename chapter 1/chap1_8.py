"""
@BY: Yang LIU
@DATE: 04-09-2020
"""


# compute the Hamming distance between two strings
# Hanming distance is the number of mismatches between strings
def hamming_distance(text1, text2):
    count = 0
    for i in range(len(text1)):
        if text1[i] != text2[i]:
            count = count + 1
    return count


# find all starting positions where pattern appears as a substring of text with at most d mismatches
def approximate_pattern_matching(pattern, text, d):
    L = len(text)
    l = len(pattern)
    position = []
    for i in range(L - l + 1):
        if hamming_distance(pattern, text[i:i+l]) <= d:
            position.append(i)
    return position


# count the number of which pattern appears as a substring of text with at most d mismatches
def approximate_pattern_count(text, pattern, d):
    count = 0
    for i in range(len(text) - len(pattern) + 1):
        fragment = text[i:i + len(pattern)]
        if hamming_distance(pattern, fragment) <= d:
            count = count + 1
    return count


# find the collection of all k-mers that has Hamming distance at most d from pattern
def neighbors(pattern, d):
    chars = "ACGT"
    if d == 0:
        return [pattern]
    r2 = neighbors(pattern[1:], d-1)
    r = [c + r3 for r3 in r2 for c in chars if c != pattern[0]]
    if (d < len(pattern)):
        r2 = neighbors(pattern[1:], d)
        r += [pattern[0] + r3 for r3 in r2]
    return r

def neighbors2(pattern, d):
    return sum([neighbors(pattern, d2) for d2 in range(d + 1)], [])


def max_map(freqmap):
    return max(freqmap.values())


# find all most frequent k-mers with up to d mismatches in text
def frequent_words_with_mismatches(text, k, d):
    patterns = []
    freqmap = {}
    n = len(text)
    for i in range(n - k + 1):
        count = 0
        pattern = text[i : i + k]
        neighborhood = neighbors2(pattern, d)
        for j in range(len(neighborhood)):
            neighbor = neighborhood[j]
            if neighbor not in freqmap.keys():
                freqmap[neighbor] = 1
            else:
                freqmap[neighbor] += 1
    m = max_map(freqmap)
    for k in freqmap.keys():
        if freqmap[k] == m:
            patterns.append(k)
    return patterns


def reverse_complement(text):
    complement = ''
    for item in text:
        if item == "A":
            value = "T"
        elif item == "T":
            value = "A"
        elif item == "C":
            value = "G"
        else:
            value = "C"
        complement = complement + value
    complement = complement[::-1]
    return complement


# find all k-mers pattern maximizing the sum countd(text, pattern)+ countd(text, patternrc) over all possible k-mers
def frequent_words_mismatches_and_rc(text, k, d):
    patterns = []
    
    freqmap = {}   # return the freqmap of all k-mers with up to d mismatches in text
    n = len(text)
    for i in range(n - k + 1):
        count = 0
        pattern = text[i : i + k]
        neighborhood = neighbors2(pattern, d)
        for j in range(len(neighborhood)):
            neighbor = neighborhood[j]
            if neighbor not in freqmap.keys():
                freqmap[neighbor] = 1
            else:
                freqmap[neighbor] += 1

    freqmap_merge = {}
    for i in freqmap.keys():
        if reverse_complement(i) in freqmap.keys():
            freqmap_merge[i] = freqmap[i] + freqmap[reverse_complement(i)]
        else:
            freqmap_merge[i] = freqmap[i]

    m = max_map(freqmap_merge)
    for k in freqmap_merge.keys():
        if freqmap_merge[k] == m:
            patterns.append(k)
    return patterns

    
if __name__ == "__main__":
    text1 = "AAAA"
    text2 = "TTTT"
    print(hamming_distance(text1, text2))
    
    text = 'TTTTTTAAATTTTAAATTTTTT'
    pattern = "AAA"
    d = 2
    print(approximate_pattern_matching(pattern, text, d))
    
    text = "AAA"
    pattern = "AA"
    k = 0
    print(approximate_pattern_count(text, pattern, d))

    text = "AAAAAAAAAA"
    k = 2
    d = 1
    print(frequent_words_with_mismatches(text, k, d))

    text = "AGTCAGTC"
    k = 4
    d = 2
    print(frequent_words_mismatches_and_rc(text, k, d))
