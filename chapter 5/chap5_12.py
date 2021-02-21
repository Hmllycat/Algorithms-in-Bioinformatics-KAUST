"""
@BY: Yang LIU
@DATE: 11-10-2020
"""

from numpy import *
import sys
sys.setrecursionlimit(15000)


score_matrix = array([[4,0,-2,-1,-2,0,-2,-1,-1,-1,-1,-2,-1,-1,-1,1,0,0,-3,-2],
                [0,9,-3,-4,-2,-3,-3,-1,-3,-1,-1,-3,-3,-3,-3,-1,-1,-1,-2,-2],
                [-2,-3,6,2,-3,-1,-1,-3,-1,-4,-3,1,-1,0,-2,0,-1,-3,-4,-3],
                [-1,-4,2,5,-3,-2,0,-3,1,-3,-2,0,-1,2,0,0,-1,-2,-3,-2],
                [-2,-2,-3,-3,6,-3,-1,0,-3,0,0,-3,-4,-3,-3,-2,-2,-1,1,3],
                [0,-3,-1,-2,-3,6,-2,-4,-2,-4,-3,0,-2,-2,-2,0,-2,-3,-2,-3],
                [-2,-3,-1,0,-1,-2,8,-3,-1,-3,-2,1,-2,0,0,-1,-2,-3,-2,2],
                [-1,-1,-3,-3,0,-4,-3,4,-3,2,1,-3,-3,-3,-3,-2,-1,3,-3,-1],
                [-1,-3,-1,1,-3,-2,-1,-3,5,-2,-1,0,-1,1,2,0,-1,-2,-3,-2],
                [-1,-1,-4,-3,0,-4,-3,2,-2,4,2,-3,-3,-2,-2,-2,-1,1,-2,-1],
                [-1,-1,-3,-2,0,-3,-2,1,-1,2,5,-2,-2,0,-1,-1,-1,1,-1,-1],
                [-2,-3,1,0,-3,0,1,-3,0,-3,-2,6,-2,0,0,1,0,-3,-4,-2],
                [-1,-3,-1,-1,-4,-2,-2,-3,-1,-3,-2,-2,7,-1,-2,-1,-1,-2,-4,-3],
                [-1,-3,0,2,-3,-2,0,-3,1,-2,0,0,-1,5,1,0,-1,-2,-2,-1],
                [-1,-3,-2,0,-3,-2,0,-3,2,-2,-1,0,-2,1,5,-1,-1,-3,-3,-2],
                [1,-1,0,0,-2,0,-1,-2,0,-2,-1,1,-1,0,-1,4,1,-2,-3,-2],
                [0,-1,-1,-1,-2,-2,-2,-1,-1,-1,-1,0,-1,-1,-1,1,5,0,-2,-2],
                [0,-1,-3,-2,-1,-3,-3,3,-2,1,1,-3,-2,-2,-3,-2,0,4,-3,-1],
                [-3,-2,-4,-3,1,-2,-2,-3,-3,-2,-1,-4,-4,-2,-3,-3,-2,-3,11,2],
                [-2,-2,-3,-2,3,-3,2,-1,-2,-1,-1,-2,-3,-1,-2,-2,-2,-1,2,7]])  

aa = ["A","C","D","E","F","G","H","I","K","L","M","N","P","Q","R","S","T","V","W","Y"]


# store backtracking pointers
def lsc_backtrack(v, w, score_matrix, openning_penalty, extension_penalty):

    s = zeros([len(v)+1,len(w)+1])
    lower = zeros([len(v)+1,len(w)+1])
    middle = zeros([len(v)+1,len(w)+1])
    upper = zeros([len(v)+1,len(w)+1])
    backtrack = full(shape=(len(v),len(w)),fill_value='XXX')
    for i in range(1,len(v)+1):
        for j in range(1, len(w)+1):
            x_index = aa.index(v[i-1])
            y_index = aa.index(w[j-1])
            match = score_matrix[x_index, y_index]
            lower[i, j] = max(lower[i-1, j] - extension_penalty, middle[i-1, j] - openning_penalty)
            upper[i, j] = max(upper[i, j-1] - extension_penalty, middle[i, j-1] - openning_penalty)
            middle[i, j] = max(lower[i, j], upper[i, j], middle[i-1, j-1] + match)
            s[i, j] = max(lower[i, j], middle[i, j], upper[i, j])
            if s[i,j] == lower[i, j]:
                backtrack[i-1, j-1] = "del"
            elif s[i, j] == upper[i, j]:
                backtrack[i-1, j-1] = "ins"
            elif s[i, j] == middle[i, j]:
                backtrack[i-1, j-1] = "mat"
    i = len(v)
    j = len(w)
    print(s[i, j])
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


if __name__ == "__main__":   

    v = "GWWQPIYEMESLWIQCEHPYAGCTWRWFCMDSLQKSFIRVCHDVIRCMLSVIRQIHWPVIYRVGTQHKTEECAW"
    w = "GWCQPIYEMESAWIQCEHPYAGCTWRWFCMDSLQKSFIRQCHDVIRQIHWPVIYRVCRSTQHSTEECSW"
    openning_penalty = 11
    extension_penalty = 1
    first_string = ""
    second_string = ""
    backtrack = lsc_backtrack(v, w, score_matrix, openning_penalty, extension_penalty)
    # print(backtrack)
    i = len(v)
    j = len(w)
    output_lsc(backtrack, v, w, i, j)   
    print(first_string[::-1])
    print(second_string[::-1])