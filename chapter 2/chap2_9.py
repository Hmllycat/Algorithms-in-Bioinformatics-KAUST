"""
@BY: Yang LIU
@DATE: 18-09-2020
"""


import random


# form a profile of given motifs
def form_profile_laplace(motifs):

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
            profile[0][0] = (d["A"] + 1)/(len(lis[i]) + 4)
            profile[1][0] = (d["C"] + 1)/(len(lis[i]) + 4)
            profile[2][0] = (d["G"] + 1)/(len(lis[i]) + 4)
            profile[3][0] = (d["T"] + 1)/(len(lis[i]) + 4)
            count += 1

        else:
            profile[0].append((d["A"] + 1)/(len(lis[i]) + 4))
            profile[1].append((d["C"] + 1)/(len(lis[i]) + 4))
            profile[2].append((d["G"] + 1)/(len(lis[i]) + 4))
            profile[3].append((d["T"] + 1)/(len(lis[i]) + 4))

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


# randomly choose a k-mer from text
def profile_randomly_generated_kmer(text, k, profile):

    probability_table = {}
    for index in range(len(text) - k + 1):
        pattern = text[index : index + k]
        # print(text," ", pattern)
        probability_table[pattern] = pr(pattern, profile)
    # print(probability_table)
    # print("  ")

    number = random.uniform(0, sum(list(probability_table.values())))
    c = 0
    for key, value in probability_table.items():
        c += value
        if number <= c:
            return key


# score the motifs(the difference between consensus motif and each of the string of Dna)
def score_motif(motifs):

    profile = form_profile_laplace(motifs)
    sco = 0
    for i in range(len(profile[0])):
        large = max([profile[0][i], profile[1][i], profile[2][i], profile[3][i]])
        sco += (1 - large) * (len(motifs) + 4) - 3
    
    return sco


def gibbs_sampler(Dna, k, t, N):

    motif = []
    for string in Dna:  #randomly select k-mers Motifs = (Motif1, …, Motift)
        index = random.randint(0,len(string) - k)
        motif.append(string[index:(index + k)])
    best_motifs = motif.copy()

    for j in range(N):
        i = random.randint(0, t - 1)
        text = Dna[i]
        a = best_motifs.copy()
        a.pop(i)
        profile = form_profile_laplace(a)  # profile matrix constructed from all strings in Motifs except for Motifi
        motif_i = profile_randomly_generated_kmer(text, k, profile)  # Profile-randomly generated k-mer in the i-th sequence
        a.insert(i,motif_i)

        if score_motif(a) < score_motif(best_motifs):
            best_motifs = a.copy()

    return best_motifs


# to run randomized_motif_search(Dna, k, t) multiple times in order to avoid a rather poor set of motifs
def iteration_for_random(Dna, k, t, times, N):
    
    best_motifs = gibbs_sampler(Dna, k, t, N)
    time = 0
    while time < times:
        motifs = gibbs_sampler(Dna, k, t, N)
        if score_motif(motifs) < score_motif(best_motifs):
            best_motifs = motifs.copy()
        time += 1
    for motif in best_motifs:
        print(motif)
    return best_motifs


if __name__ == "__main__":
    Dna =["CGCCCCTCTCGGGGGTGTTCAGTAACCGGCCA",
    "GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG",
    "TAGTACCGAGACCGAAAGAAGTATACAGGCGT",
    "TAGATCAAGTTTCAGGTGCACGTCGGTGAACC",
    "AATCCACCAGCTCCACGTGCAATGTTGGCCTA"]
    k = 8
    t = 5
    N = 100
    times = 20
    iteration_for_random(Dna, k, t, times, N)
