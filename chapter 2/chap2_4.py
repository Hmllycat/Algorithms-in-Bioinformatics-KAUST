"""
@BY: Yang LIU
@DATE: 11-09-2020
"""

# compute the Hamming distance between two strings
# Hanming distance is the number of mismatches between strings
def hamming_distance(text1, text2):
    count = 0
    for i in range(len(text1)):
        if text1[i] != text2[i]:
            count = count + 1
    return count


# compute the sum of distances between Pattern and each string in Dna = {Dna1, ..., Dnat}
def distance_between_pattern_and_strings(pattern, Dna):
    
    k = len(pattern)
    distance_sum = 0
    
    for string in Dna:
        distance = k  #randomly assign a large number, which could be the value of the length of pattern
        for i in range(len(string) - k + 1):      # find the minimum distance between the pattern and given string
            fragment = string[i: i+k]
            if distance > hamming_distance(pattern, fragment):
                distance = hamming_distance(pattern, fragment)
        distance_sum += distance
        
    return distance_sum


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


# generate an array containing all strings of length k
def all_strings(k):
    
    pattern = "A"*k
    return neighbors2(pattern, k)


# find a k-mer pattern that minimizes d(pattern, Dna) among all possible choices of k-mers
def median_string(Dna, k):
    
    distance = k
    patterns = all_strings(k)  # collect all the k-mers
    
    for i in range(len(patterns)):   # traverse to find all the 
        pattern = patterns[i]
        
        if distance > distance_between_pattern_and_strings(pattern, Dna):   # traverse all the k-mers to find the one that minimizes sum of distance between all the strings and given pattern
            distance = distance_between_pattern_and_strings(pattern, Dna)
            median = pattern

    return median



if __name__ == "__main__":
    k = 3
    Dna = ['AAATTGACGCAT','GACGACCACGTT','CGTCAGCGCCTG','GCTGAGCACCGG','AGTTCGGGACAG']
    print(median_string(Dna, k))
