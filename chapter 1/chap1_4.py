"""
@BY: Yang LIU
@DATE: 03-09-2020
"""


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


# find patterns forming clumps in a string
def find_clumps(text, k, L, t):
    patterns = []
    n = len(text)
    for i in range(n - L):  # form a window with length L and return a frequency table of k-mer in this window
        window = text[i:i + L]
        freqmap = frequency_table(window, k)
        for key in freqmap.keys():
            if freqmap[key] >= t:   # screen out the k-mers with frequency more than t
                patterns.append(key)
    result = sorted(set(patterns),key = patterns.index)   # remove duplicates from patterns
    return result


if __name__ == "__main__":
    text = 'CGGACTCGACAGATGTGAAGAACGACAATGTGAAGACTCGACACGACAGAGTGAAGAGAAGAGGAAACATTGTAA'
    k = 5
    L = 50
    t = 4
    print(find_clumps(text, k, L, t))
    
