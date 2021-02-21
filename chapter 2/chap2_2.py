"""
@BY: Yang LIU
@DATE: 11-09-2020
"""


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


# compute the Hamming distance between two strings
# Hanming distance is the number of mismatches between strings
def hamming_distance(text1, text2):
    count = 0
    for i in range(len(text1)):
        if text1[i] != text2[i]:
            count = count + 1
    return count


# count the number of which pattern appears as a substring of text with at most d mismatches
def approximate_pattern_count(text, pattern, d):
    count = 0
    for i in range(len(text) - len(pattern) + 1):
        fragment = text[i:i + len(pattern)]
        if hamming_distance(pattern, fragment) <= d:
            count = count + 1
    return count


# find all (k, d)-motifs in Dna
# Given a collection of strings Dna and an integer d, a k-mer is a (k,d)-motif if it appears in every string from Dna with at most d mismatches
def motif_enumeration(Dna, k, d):

    patterns = []
    for i in Dna:  # traverse each string of the dna collection
        for j in range(len(i) - k + 1):   # collect all k-mer Pattern’ differing from Pattern by at most d mismatches
            pattern = i[j : j + k]
            neighborhood = neighbors2(pattern,d)
            for a in neighborhood:    # check if pattern appears in each string from Dna with at most d mismatches
                count = 0
                for b in Dna:
                    if approximate_pattern_count(b, a, d) > 0:
                        count += 1
                if count == len(Dna):
                    patterns.append(a)
                        
    result = sorted(set(patterns),key = patterns.index)   #remove duplicates from patterns

    return result


if __name__ == "__main__":
    Dna = ["AAAAA","AAAAA","AAAAA"]
    k = 3
    d = 3
    print(motif_enumeration(Dna, k, d))
