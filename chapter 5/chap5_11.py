"""
@BY: Yang LIU
@DATE: 09-10-2020
"""

from numpy import *
import sys
sys.setrecursionlimit(15000)


# store backtracking pointers
def lsc_backtrack(v, w):
    s = zeros([len(v)+1,len(w)+1])
    for i in range(len(v)+1):
        s[i,0] = i
    for j in range(len(w)+1):
        s[0,j] = j
    # print(s)
    backtrack = full(shape=(len(v),len(w)),fill_value='XXX')
    for i in range(1,len(v)+1):
        for j in range(1, len(w)+1):
            match = 1
            if v[i-1] == w[j-1]:
                match = 0
            s[i, j] = min(s[i-1, j] + 1, s[i, j-1] + 1, s[i-1, j-1] + match)
            if s[i, j] == s[i, j-1] + 1:
                backtrack[i-1, j-1] = "ins"
            elif s[i,j] == s[i-1,j] + 1:
                backtrack[i-1, j-1] = "del"
            else: 
                backtrack[i-1, j-1] = "mat"
                
    return backtrack  


# Input: Two strings s and t.
# Output: A longest common subsequence of s and t. (Note: more than one solution may exist, in which case you may output any one.)
def output_lsc(backtrack, v, w, i, j):
    global first_string
    global second_string
    if i == 0 and j == 0:
        first_string += ""
        second_string += ""
        return ""
    elif j == 0:
        first_string += v[i-1]
        second_string += "-"
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


def hamming_distance(text1, text2):
    count = 0
    for i in range(len(text1)):
        if text1[i] != text2[i]:
            count = count + 1
    return count


if __name__ == "__main__":   

    v = "PLEASANTLY"
    w = "MEANLY"
    first_string = ""
    second_string = ""
    backtrack = lsc_backtrack(v, w)
    # print(backtrack)
    i = len(v)
    j = len(w)
    # print(i,j)
    q = output_lsc(backtrack, v, w, i, j)
    # print(len(q))
    # print(first_string[::-1], len(first_string[::-1]))
    # print(second_string[::-1], len(second_string[::-1]))    
    print(hamming_distance(first_string, second_string))