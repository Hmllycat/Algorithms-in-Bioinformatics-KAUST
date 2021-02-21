"""
@BY: Yang LIU
@DATE: 03-09-2020
"""



# count the times for which the k-mer substring match the text
def pattern_count(text, pattern):
        count = 0
        for i in range(len(text) - len(pattern)):
            fragment = text[i:i + len(pattern)]  # k-mer window of text
            if fragment == pattern:
                count = count + 1
        return count


# find all frequent k-mers
def frequency_table(text, k):
    freqmap = {}
    n = len(text)
    for i in range(n - k):
        pattern = text[i:i + k]
        if pattern not in freqmap.keys():
            freqmap[pattern] = 1
        else:
            freqmap[pattern] = freqmap[pattern] + 1
    return freqmap


# return the lagest frequecy value of the frequency table
def max_map(freqmap):
    return max(freqmap.values())


# find all the most frequent k-mers of a given text
def better_frequent_words(text, k):
    frequentpatterns = []
    freqmap = frequency_table(text, k)
    max = max_map(freqmap)
    for pattern in freqmap.keys():
        if freqmap[pattern] == max:
            frequentpatterns.append(pattern)
    return frequentpatterns


if __name__ == "__main__":
    text = 'ACGTACGTACGT'
    pattern = "CG"
    print(pattern_count(text, pattern))
    text = "TGGTAGCGACGTTGGTCCCGCCGCTTGAGAATCTGGATGAACATAAGCTCCCACTTGGCTTATTCAGAGAACTGGTCAACACTTGTCTCTCCCAGCCAGGTCTGACCACCGGGCAACTTTTAGAGCACTATCGTGGTACAAATAATGCTGCCAC"
    k = 3
    print(better_frequent_words(text, k))
