"""
@BY: Yang LIU
@DATE: 10-10-2020
"""

from numpy import *
import sys
sys.setrecursionlimit(15000)


aa = ["A","C","D","E","F","G","H","I","K","L","M","N","P","Q","R","S","T","V","W","Y"]

pam250_score_matrix = array([ 
                        [2,-2,0,0,-3,1,-1,-1,-1,-2,-1,0,1,0,-2,1,1,0,-6,-3],
                        [-2,12,-5,-5,-4,-3,-3,-2,-5,-6,-5,-4,-3,-5,-4,0,-2,-2,-8,0],
                        [0,-5,4,3,-6,1,1,-2,0,-4,-3,2,-1,2,-1,0,0,-2,-7,-4],
                        [0,-5,3,4,-5,0,1,-2,0,-3,-2,1,-1,2,-1,0,0,-2,-7,-4],
                        [-3,-4,-6,-5,9,-5,-2,1,-5,2,0,-3,-5,-5,-4,-3,-3,-1,0,7],
                        [1,-3,1,0,-5,5,-2,-3,-2,-4,-3,0,0,-1,-3,1,0,-1,-7,-5],
                        [-1,-3,1,1,-2,-2,6,-2,0,-2,-2,2,0,3,2,-1,-1,-2,-3,0],
                        [-1,-2,-2,-2,1,-3,-2,5,-2,2,2,-2,-2,-2,-2,-1,0,4,-5,-1],
                        [-1,-5,0,0,-5,-2,0,-2,5,-3,0,1,-1,1,3,0,0,-2,-3,-4],
                        [-2,-6,-4,-3,2,-4,-2,2,-3,6,4,-3,-3,-2,-3,-3,-2,2,-2,-1],
                        [-1,-5,-3,-2,0,-3,-2,2,0,4,6,-2,-2,-1,0,-2,-1,2,-4,-2],
                        [0,-4,2,1,-3,0,2,-2,1,-3,-2,2,0,1,0,1,0,-2,-4,-2],
                        [1,-3,-1,-1,-5,0,0,-2,-1,-3,-2,0,6,0,0,1,0,-1,-6,-5],
                        [0,-5,2,2,-5,-1,3,-2,1,-2,-1,1,0,4,1,-1,-1,-2,-5,-4],
                        [-2,-4,-1,-1,-4,-3,2,-2,3,-3,0,0,0,1,6,0,-1,-2,2,-4],
                        [1,0,0,0,-3,1,-1,-1,0,-3,-2,1,1,-1,0,2,1,-1,-2,-3],
                        [1,-2,0,0,-3,0,-1,0,0,-2,-1,0,0,-1,-1,1,3,0,-5,-3],
                        [0,-2,-2,-2,-1,-1,-2,4,-2,2,2,-2,-1,-2,-2,-1,0,4,-6,-2],
                        [-6,-8,-7,-7,0,-7,-3,-5,-3,-2,-4,-4,-6,-5,2,-2,-5,-6,17,0],
                        [-3,0,-4,-4,7,-5,0,-1,-4,-1,-2,-2,-5,-4,-4,-3,-3,-2,0,10]
                    ])


# store backtracking pointers
def lsc_backtrack(v, w, pam250_score_matrix):

    global max_position
    s = zeros([len(v)+1,len(w)+1])
    for i in range(len(v)+1):
        s[i,0] = -5*i
    for j in range(len(w)+1):
        s[0,j] = -5*j
    max_score = 0
    backtrack = full(shape=(len(v),len(w)),fill_value='XXX')
    for i in range(1,len(v)+1):
        for j in range(1, len(w)+1):
            x_index = aa.index(v[i-1])
            y_index = aa.index(w[j-1])
            match = pam250_score_matrix[x_index, y_index]
            s[i, j] = max(s[i-1, j] - 5, s[i, j-1] - 5, s[i-1, j-1] + match, 0)
            if s[i, j] >= max_score:
                max_score = s[i, j]
                max_position = [i, j]
            if s[i,j] == s[i-1,j] - 5:
                backtrack[i-1, j-1] = "del"
            elif s[i, j] == s[i, j-1] - 5:
                backtrack[i-1, j-1] = "ins"
            elif s[i, j] == 0:
                backtrack[i-1, j-1] = "cut"
            elif s[i, j] == s[i-1, j-1] + match:
                backtrack[i-1, j-1] = "mat"
    print(max_score)
    return backtrack 


# Input: Two strings s and t.
# Output: A longest common subsequence of s and t. (Note: more than one solution may exist, in which case you may output any one.)
def output_lsc(backtrack, v, w, i, j):
    
    global first_string
    global second_string
    if (i == 0 and j == 0) or backtrack[i-1, j-1] == "cut":
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

    v = "MEANLY"
    w = "PENALTY"
    first_string = ""
    second_string = ""
    max_position = [0, 0]
    backtrack = lsc_backtrack(v, w, pam250_score_matrix)
    # print(backtrack, max_position)
    i = max_position[0]
    j = max_position[1]
    output_lsc(backtrack, v, w, i, j)   
    print(first_string[::-1])
    print(second_string[::-1])