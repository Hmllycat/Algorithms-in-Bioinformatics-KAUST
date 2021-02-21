"""
@BY: Yang LIU
@DATE: 13-09-2020
"""

import math


# form a profile of given motifs
def form_profile(motifs):

    lis = []      
    for i in range(len(motifs[0])):
        lis.append('')
        for j in range(len(motifs)):
            lis[i] += motifs[j][i]    # form a list in which each element refers to element collection of a given position of each motif, e.g motifs = ["ACG", "TCA"]->["AT", "CC", "GA"]

    profile = [[0], [0], [0], [0]]
    count = 0
    for i in range(len(lis)):
        d = {"A":0, "C":0, "G":0, "T":0}
        for x in lis[i]:
            d[x] += 1      # count frequency of "ACGT" in each position
        
        if  count == 0:
            profile[0][0] = d["A"]/len(lis[i])
            profile[1][0] = d["C"]/len(lis[i])
            profile[2][0] = d["G"]/len(lis[i])
            profile[3][0] = d["T"]/len(lis[i])
            count += 1

        else:
            profile[0].append(d["A"]/len(lis[i]))
            profile[1].append(d["C"]/len(lis[i]))
            profile[2].append(d["G"]/len(lis[i]))
            profile[3].append(d["T"]/len(lis[i]))

    return profile
        

# calculate the sum of given index of value (value is a list of number)
def sum_self(value, index):
    score_self = 1
    for i in index:
        score_self = value[i] * score_self
    return score_self


# calculate the probability of a given pattern  
def pr(pattern, profile):

    find_all = lambda data, s: [r for r in range(len(data)) if data[r] == s]  #return all the index of which the pattern matches the string
    A = profile[0]
    C = profile[1]
    G = profile[2]
    T = profile[3]
    Aindex = find_all(pattern, "A")
    Tindex = find_all(pattern, "T")
    Gindex = find_all(pattern, "G")
    Cindex = find_all(pattern, "C")
    scores = sum_self(A, Aindex) * sum_self(C, Cindex) * sum_self(G, Gindex) * sum_self(T, Tindex)
    
    return scores    


# find a profile-most probable k-mer in text
def most_probable_kmers(text, k, profile):
    
    initial = -1
    
    for i in range(len(text) - k + 1):   #traver the text to find all the k-mers and calculate the total probability of the k-mers
        pattern = text[i: i + k]
        score = pr(pattern, profile)
        
        if score > initial:    # find the pattern whose probability is the largest
            initial = score
            fragment = pattern

    return fragment


def entropy(number):
    result = 0
    
    if(len(number)>0):
        result=0
        
    for x in number:
        if x != 0:
            result+=(-x)*math.log(x,2)
        
    return result


# score the motifs(the difference between consensus motif and each of the string of Dna)
def score_motif(motifs):

    profile = form_profile(motifs)
    sco = 0
    for i in range(len(profile[0])):
        large = max([profile[0][i], profile[1][i], profile[2][i], profile[3][i]])
        sco += (1 - large) * len(motifs)
    
    return sco


def greedy_motif_search(Dna, k, t):

    best_motifs = []
    
    for dna in Dna:
        best_motifs.append(dna[0:k])

    first_str = Dna[0]
    for i in range(len(first_str) - k + 1):
        motif1 = first_str[i : i+k]
        motifs = [motif1]
        
        for j in range(1, t):
            profile = form_profile(motifs)
            patterns = most_probable_kmers(Dna[j], k, profile)
            motifs.append(patterns)

        if score_motif(motifs) < score_motif(best_motifs):
            best_motifs = motifs.copy()

    return best_motifs
        
            
        
if __name__ == "__main__":
    text = "AGCAGCTTTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATCTGAACTGGTTACCTGCCGTGAGTAAAT"
    A = [0.7, 0.2, 0.1, 0.5, 0.4, 0.3, 0.2, 0.1]
    C = [0.2, 0.2, 0.5, 0.4, 0.2, 0.3, 0.1, 0.6]
    G = [0.1, 0.3, 0.2, 0.1, 0.2, 0.1, 0.4, 0.2]
    T = [0.0, 0.3, 0.2, 0.0, 0.2, 0.3, 0.3, 0.1]
    profile = [A, C, G, T]
    k = 8
    print(most_probable_kmers(text, k, profile))

    Dna =["GGCGTTCAGGCA",
          "AAGAATCAGTCA",
          "CAAGGAGTTCGC",
          "CACGTCAATCAC",
          "CAATAATATTCG"]
    k = 3
    t = 5
    print(greedy_motif_search(Dna, k, t))
