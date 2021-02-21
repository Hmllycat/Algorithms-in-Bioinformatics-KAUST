"""
@BY: Yang LIU
@DATE: 23-11-2020
"""

from numpy import *
import sys
sys.setrecursionlimit(15000)


emission_matrix = array([[2/3, 1/3],
                         [1/3, 2/3]])  
alphabet = ["H", "T"]
states = ["A", "B"]
transition_matrix = array([[3/4, 1/4],
                           [1/4, 3/4]]) 


# store backtracking pointers
def lsc_backtrack(path_x):

    s = zeros([2, len(path_x)])
    x_index = alphabet.index(path_x[0])
    for i in range(2):
        s[i,0] = emission_matrix[i, x_index]
    backtrack = zeros([2, len(path_x)-1])
    
    for j in range(1, len(path_x)):
        for i in range(2):
            x_index = alphabet.index(path_x[j])
            s[i, j] = max(s[0, j-1]*transition_matrix[0,i]*emission_matrix[i,x_index], s[1, j-1]*transition_matrix[1,i]*emission_matrix[i,x_index])
            # print(s)
            if s[i, j] == s[1, j-1]*transition_matrix[1,i]*emission_matrix[i,x_index]:
                backtrack[i, j-1] = 1
    last_column = max(s[0, len(path_x)-1], s[1, len(path_x)-1])        
    if last_column == s[1, len(path_x)-1]:
        backtrack_start = 1
    else:
        backtrack_start = 0
    # print(s)
    return backtrack, backtrack_start 


# Input: Two strings s and t.
# Output: A longest common subsequence of s and t. (Note: more than one solution may exist, in which case you may output any one.)
def output_lsc(backtrack_start, backtrack):
    path = ""
    state_choice = backtrack_start
    count = len(backtrack[0,]) + 1
    while count != 0:
        path += states[state_choice]
        count -= 1
        state_choice = int(backtrack[state_choice, count-1])
    return path[::-1]


if __name__ == "__main__":   
    path_x = "HTTH"
    backtrack, backtrack_start = lsc_backtrack(path_x)
    # print(backtrack)
    print(output_lsc(backtrack_start, backtrack))