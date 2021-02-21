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


if __name__ == "__main__":
    Dna = ["AAACT","AAAC","AAAG"]
    pattern = 'AAA'
    print(distance_between_pattern_and_strings(pattern, Dna))
