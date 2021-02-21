"""
@BY: Yang LIU
@DATE: 09-10-2020
"""

from numpy import *
import sys
sys.setrecursionlimit(15000)


# store backtracking pointers
def lsc_backtrack(v, w, match_score, mis_penalty, indel_penalty):

    global max_position
    s = zeros([len(v)+1,len(w)+1])
    for i in range(len(v)+1):
        s[i,0] = 0
    for j in range(len(w)+1):
        s[0,j] = -indel_penalty*j
    max_score = 0
    backtrack = full(shape=(len(v),len(w)),fill_value='XXX')
    for i in range(1, len(v)+1): 
        for j in range(1, len(w)+1):
            match = -mis_penalty
            if v[i-1] == w[j-1]:
                match = match_score
            s[i, j] = max(s[i-1, j] - indel_penalty, s[i, j-1] - indel_penalty, s[i-1, j-1] + match)
            if j == len(w):
                if s[i, j] >= max_score:
                    max_position = [i, j]
                    max_score = s[i, j]
            if s[i,j] == s[i-1,j] - indel_penalty:
                backtrack[i-1, j-1] = "del"
            elif s[i, j] == s[i, j-1] - indel_penalty:
                backtrack[i-1, j-1] = "ins"
            elif s[i, j] == s[i-1, j-1] + match:
                backtrack[i-1, j-1] = "mat"

    print(max_score)
    return backtrack 


# Input: Two strings s and t.
# Output: A longest common subsequence of s and t. (Note: more than one solution may exist, in which case you may output any one.)
def output_lsc(backtrack, v, w, i, j):
    
    global first_string
    global second_string
    if j == 0:
        # first_string += v[i-1]
        # second_string += "-"
        return ""
    elif i == 0:
        first_string += "-"
        second_string += w[j-1]
        return ""
    elif backtrack[i-1, j-1] == 'del':
        first_string += v[i-1] 
        second_string += "-"
        return output_lsc(backtrack, v, w, i-1, j)
    elif backtrack[i-1, j-1] == "ins":
        first_string += "-"
        second_string += w[j-1]
        return output_lsc(backtrack, v, w, i, j-1)
    else:
        first_string += v[i-1]
        second_string += w[j-1]
        return output_lsc(backtrack, v, w, i-1, j-1) + v[i-1]


if __name__ == "__main__":   

    v = "CGTTGCTCAAGCGGTGGCCATCGATCAGTACTTGGGTTTAAATCATGGACCTATATTTCGTCGCGTGTCACTATCATGTTGAATCGGTATGTGCAGGATAGGTCGCAATGACGAACACACTTTGCCGCTTTTGGTCTACAGCTGCACTGGTCCATCATTGGCACGGACTGGTTGCCTACTGCATCTAAAAGTATTTGACGAGCAGGTGAAACCCATTAGCAATTATCATCCGAGATTAGTGCTCGGTACCTACAGCTAGAGATAACTTAATGGACATGAGAGCTATTGAGCTTCATTGCTTAGGTATCAGGTCCATCTGGAAGTCTGTGCATTGCGGACAATACATGGCCGGACCCTAATTCCACTTTAGACACGTATTGTACAAGATATCACATGGCGCCTCGACATTCAAAGTAAGTACGCTTAGCTTTCCCCCCTTAGAGTTCGTTTTTACGGCCTTTCTGATGTTCCGGGGCCGAGGCTGTCTTAGGAACATTGGCCTAGTGATCTCAGACTAAATAGACCAATTCTAAGATGGACCAGATTAAGTTCGACAGGTGGTTATAAATGGCCTTTATCCTTGCCTTCTCTAATAGGACCTACCGTCGCGCCGTGTGGGTGCAGCTTCAATAACTTACGCCCGTATGTCTCGCAACCCCGAATACGAGACCGGCTAGGCTCGAAAATTTCCACTACTTCGTGGGATGTCGTGCCCCGGACTCAAGCCCGTTCCCTTTACGCTGGTAAGTAGTGACACAAGGACAATCGAGCAACCTAAAATCGAGGACTCACACGAAATAAAACTCTTAAGTGTTTCTGGGGGCATTATACGGATCGAGCCATTCTCTGGAACTAATACCTTACCGACTCCAGCCCCCACTTCATCTTACCATTGAGCCAACTTATCTCAATCCATGGAGCATTGATAAATAACA"
    w = "TGAATTCCCCCTTTCGGATTTCACAATTTTACGTCTCGGCAGCCAACGAAGGGTGCACGCGACTGTCCCTAAGATGCCTCCGAACCACCACACTAGCT"
    match_score = 1
    mis_penalty = 1
    indel_penalty = 1
    first_string = ""
    second_string = ""
    max_position = [0, 0]
    backtrack = lsc_backtrack(v, w, match_score, mis_penalty, indel_penalty)
    # print(backtrack, max_position)
    i = max_position[0]
    j = max_position[1]
    output_lsc(backtrack, v, w, i, j)   
    print(first_string[::-1])
    print(second_string[::-1])