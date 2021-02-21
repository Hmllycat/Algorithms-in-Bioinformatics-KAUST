"""
@BY: Yang LIU
@DATE: 15-09-2020
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


# form a new motifs by selecting most probable k-mer in each string of Dna
def motifs(profile, Dna, k):
    
    d = []
    for text in Dna:
        d.append(most_probable_kmers(text, k, profile))

    return d


# score the motifs(the difference between consensus motif and each of the string of Dna)
def score_motif(motifs):

    profile = form_profile_laplace(motifs)
    sco = 0
    for i in range(len(profile[0])):
        large = max([profile[0][i], profile[1][i], profile[2][i], profile[3][i]])
        sco += (1 - large) * (len(motifs) + 4) - 3
    
    return sco


# begin from a new randomly selected set of k-mers
def randomized_motif_search(Dna, k, t):

    motif = []
    for string in Dna:  #randomly select k-mers Motifs = (Motif1, …, Motift)
        index = random.randint(0,len(string) - k)
        motif.append(string[index:(index + k)])
    best_motifs = motif
    
    while True:
        profile = form_profile_laplace(motif)
        motif = motifs(profile, Dna, k)
        if score_motif(motif) < score_motif(best_motifs):
            best_motifs = motif
        else:
            return best_motifs
        

# to run randomized_motif_search(Dna, k, t) multiple times in order to avoid a rather poor set of motifs
def iteration_for_random(Dna, k, t, times):
    
    best_motifs = randomized_motif_search(Dna, k, t)
    time = 0
    while time < times:
        motifs = randomized_motif_search(Dna, k, t)
        if score_motif(motifs) < score_motif(best_motifs):
            best_motifs = motifs
            # print(score_motif(best_motifs))
        time += 1
    for motif in best_motifs:
        print(motif)
    return best_motifs




if __name__ == "__main__":
    Dna =["GCGATTGGGTGTAGCTTTGAGCGTAACGTTCAGTAATCGTGGCTGGCAGCTGCATCCTTAGCAAGTACCGAATGTGCACGGCTCTGAAGAATTGGCGTAAAATAGGCTTCGTACACCGCGGATCATGTAGCACGACGAGCTGTAGAAAAACCCGGGATGGCAAGCCTGACATAGGCGATTGGGTGTAGC",
"TTTGAGCGTAACGTTCAGTAATGCCAAATAGCATTCTCGTGGCTGGCAGCTGCATCCTTAGCAAGTACCGAATGTGCACGGCTCTGAAGAATTGGCGTAAAATAGGCTTCGTACACCGCGGATCATGTAGCACGACGAGCTGTAGAAAAACCCGGGATGGCAAGCCTGACATAGGCGATTGGGTGTAGC",
"AGAGAACGTACTGACCTGGCGGCAAAATGCCCTGCTATCAGGTGGTGACAGCCGGTGGGCATTCTATGCGTGGGAAATCTGTATGTGGATTCCTCTTCCACGTCCAAGTCGGTTGGTTTACGCAGGTAGGTCGGTGAATAGGAGCTTAGTATGCGCAGCGCGCAGGCACATTTCGCATTTTCTGTCAAG",
"GGGTTGCCACTTCCTGCTTGGGTCGTTAGCCGATCCAGTAAGTGACACAGTAGGGGCCGGGAGTCATTCTGGTATGGAACAGCAAGCTACAGTCAAAACTTCTTAGCACCCCAGGACTAATGGTTCTTGCAAGATCGTTTTTCTATAGCCAAAGCGAGTCCAACTTGCACACTCTGCATTCAATTAGAT",
"TCAATGGGCTATAACGTCTCGGCGCGTACTATGCCTCTTGATACTACAACGGCCGGTTTGAAATCCTACGTTGTCGGCAATAACGGAGTGAGGATGCCGGGTAGCAGCATCACTAGAGACTAGTAGGCATCGGGATTCATGAACTGCAGCCAGAAAAGGCTTGGTCGCCACTTATGTAGAGAGCTTCCT",
"CCCGTGCATATAGTAATAGGGTTGAATTAAAATCACCCGCACGCACCGATTAAATATACGACACTATAAGGGCCTTAATTCTTCGCAAATACTAGACCGTAACTGACGCCGTGGGGCCGGGTAGCATCAATCTGTGCAAGAAGAACTTAGATACATATCGTCATTGTAGTGCCAAGGACCGGCAATTCC",
"ATTCGAGAGCATAATTTGACGCCAACTCATACACCAGTGCGCCACAGGATAGATCGCTTAGCTTTCGAAATACCGTGTTCAGGGAGGTATTAGCACGTTGGGTGGGTACCAGCGGGAGACTGCCGGGTAAAGTTCTCCAGTCGTACCGAATGAAAAACCTAGCCCTGTTAAGGGTAGTAATGTTGTTGA",
"ATGATCCGGCGGATGTAAACTTTGACGGATTATGATAGATCTCGCGGGTTAGCCGGGTAGTCCTCTCAAGGTGTCTAGGGGCTTGGCAGACGAATACTATGAATCTACCCTGAAAATGTCATCAGAAAACATTCCAGTGATCTGTCCCACGTGTGCACCCCCCGATTCAAGAGCCCACACAGAAACAGC",
"GGCTCTTCGGTCCTGCAGATTTCATACCGTAACCCCTGCCGGTTTCCAGATGAAGCGCTAGCCGGGTGTTATTCTATTTCAACAGATAACTAAAAGTGCGATCAAGTCAATCGCTTGGACTAACCAGCTGTGGGTTGTAGGATGTATCTCTGACGCTTTCACTTCAGCAACTTGTTCGCACTATGGTAG",
"AGAAAACCCTGTGGCCGACGTGTGACTCCTCGCGGGCGCACATTTCCCGCGAAAACTTTATGTCCAACCCCGAGTTACGGTAGTGGTAGAATTAAGATTCCCGCCTGATTGGTTGGCACGTCATCGATAAGGCACCGTGACATCGCCGGGTAGCCCACTATTCGTTGATTGTGTCTAATTGTCAAATAA",
"CTGTCCGCTACTTGCCTTCAACACGCCGGATGGCACACGTTCCTCGCGTTTCGAATAGTGGACTAGCGTGGTCTGCAATCACGGTGATATAATTCCTCATTATTTGTGGTATATTTGCAGATTCCCGCCCTGCACGGCCGGATTCCCAGTGACTAGCTAAGTAGCATTCTAGCGGTCCCCCCCTTCGCA",
"TGCCAACGACTAGCTGCTGGAGTCCGACATACTATTAATTCTCCGCAGAGCATAGTTTATCCGCGCAAAGTAATGACGAATGTTCGCATGAGCCACGGAGTGCATTCGGACATAGCATCAACTAGAAGCAGCTCCTAGGCCGTCGATCGTCACCCCGGGTAGCATTGCGCGGCAAGAGAAAAGCCTTCA",
"AGTATTTGCAAGCATATCTAAAAGATGAATTGACCTGTGAAGACCAGCGGTTCGACGCCTTAACTCACCGTCCTTATGTAATACATGAGGTCCTACTACGGGGCTCACCCGGCACTTCCGCGGGTGGCGATATTAGACGGCTTGTGAGTCCGCCGCTCAGCATTCTCCCCGTCCAACGTATATCTGTGA",
"GTTATGACGTGACTTAGACTCGGAAAGATTAGGGCCTCTAGGGAGTGAGGGCTAAGTTTGCCGTATCGCTATGCGATCGCCTGATTACCTCTATTACCAACATGTTTAGTAGTGGCTTTATTCATTCAGGTTCACTATGTTCGCCAGCGAGCCTACTAGCATTCTTGTGTGCCAAAGCCAGTGTGTTAG",
"GAGGTAATCAAATTCTCCGGTTGTCCGGTCGGTGTAGGGGGAACTCTTGAGTACTCATACGACCCTTGCCGGCCGGCATTCTGCTCGCCATTTTCGTGTCGGAAACGTTAAGCCCCGGTCCTCTGGTATCCATCTCCGCCAGCCGTAGCTGGCGATATCGTTGTACTTTCCTCCCGTTCCCATTTTCGC",
"CCCCAGTTAGGTAGCATTCTAATCCAACCCGCTGTTTCTAATCGCCGTCAGTATGACGATATGGGCAGACTTACTCATTCTTTGGAGTCGAAGGGAGTAGTTAATATAGACTAACTGAGCGTCTTCTCTTCGACATCACGCTCGGTGGTGCTACCACGAAGAAAATGAAAAATTACTTCGCTAGCGTGC",
"TCCCCGATATCGACGGTTCTTGTGGTAATCTAAACAGAAGCAGACAGCCTCGTGCTGTTTATCGATGCACTGCGTTTTGTTTGTTATCCTTCTGCACGGAGGCGCGTATGATCGCAATCCACATGACCGTGGGTAGCATTCTGATGATAGGGGGGCTTATCCTACATACAGAGGTTATGTCCGTTCGCG",
"TGAGTCAGGGGAATCTAAATAAGTATTGGGTGCATTTACTTCTGCGGTCGTTCGATTTGGATTTTGCGCACTCCCTGCGATGCCGACAAGCATTCTTAGCGATTCGATTCTCCCTTTGCTTCTCTTGCTGCTTGACACGTCTGCTTCCGCGCACAGCTCGATTTTCCATTAACGTAACCGCGATACAGC",
"GGATGTACTCCAGGCGCCTGGAGCTAAGCCATTGGGTCAAATGTGGCTTCTAGCAACACAAGCCGGGATCCATTCTACTCGAAGAGCCGGTTGTATCTATGCGGATAGGTAATATCGCGCACACGTCGTGGGACAGCGTACAGATGTCACTATATTCGACGCTGGGCAAGGAAGCACACAGATCAAATT",
"TTAAACGGGTAGCATTCATGCGTAGCAAACCCCCTATGCTCTCACCTTAATAATCGCAATCAAGTCCAGGTATGGCGGCAAAGATGGCCAAGGATAAAACCTCCCGGCAGAGCAATGCCGTATTCGAGACCTGGTGGCCTAAGCGCGAGACGCTTCCGCTAATCCTCGGATCTCCTTGATGCCAGGCGA"]
          
    k = 15
    t = 20
    times = 1000
    iteration_for_random(Dna, k, t, times)
