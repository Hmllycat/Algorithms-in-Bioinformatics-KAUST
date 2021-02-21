"""
@BY: Yang LIU
@DATE: 09-10-2020
"""

from numpy import *
import sys
sys.setrecursionlimit(15000)


emission_matrix = array([[0.117, 0.691, 0.192],
                         [0.097, 0.42, 0.483]])  
alphabet = ["x", "y", "z"]
states = ["A", "B"]
transition_matrix = array([[0.641, 0.359],
                           [0.729, 0.271]]) 


# store backtracking pointers
def lsc_backtrack(path_x, emission_matrix, transition_matrix):

    s = zeros([2, len(path_x)])
    x_index = alphabet.index(path_x[0])
    for i in range(2):
        s[i,0] = emission_matrix[i, x_index]
    backtrack = full(shape=(2,len(path_x)-1),fill_value='XXX')
    for i in range(2):
        for j in range(1, len(path_x)):
            x_index = alphabet.index(path_x[j])
            s[i, j] = max(s[0, j-1]*transition_matrix[0,i]*emission_matrix[0,x_index], s[1, j-1]*transition_matrix[1,i]*emission_matrix[1,x_index])
            # print(s[i, j])
            if s[i, j] == s[0, j-1]*transition_matrix[0,i]*emission_matrix[0,x_index]:
                backtrack[i-1, j-1] = "A"
            elif s[i, j] == s[1, j-1]*transition_matrix[1,i]*emission_matrix[1,x_index]:
                backtrack[i-1, j-1] = "B"
            
    i = 1
    j = len(path_x)-1
    print(s[i, j])
    return backtrack 


# Input: Two strings s and t.
# Output: A longest common subsequence of s and t. (Note: more than one solution may exist, in which case you may output any one.)
def output_lsc(backtrack, v, w, i, j):
    
    global first_string
    global second_string
    if i == 0 and j == 0:
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
    path_x = "xyxzzxyxyy"
    lsc_backtrack(path_x, emission_matrix, transition_matrix)