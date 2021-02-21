"""
@BY: Yang LIU
@DATE: 23-11-2020
"""

from numpy import *
import sys
sys.setrecursionlimit(15000)


emission_matrix = array([[0.236,0.181,0.583],
                        [0.259,0.614,0.127],
                        [0.602,0.304,0.094],
                         [0.635,0.06,0.305]])  
alphabet = ["x", "y", "z"]
states = ["A", "B", "C", "D"]
transition_matrix = array([[0.409,0.179,0.3,0.112],
                           [0.429,0.187,0.181,0.203],
                           [0.387,0.044,0.036,0.533],
                           [0.369,0.095,0.372,0.164]]) 


# Input: A string x, followed by the alphabet from which x was constructed, followed by the states States, transition matrix Transition, and emission matrix Emission of an HMM (Σ, States, Transition, Emission).
# Output: The probability Pr(x) that the HMM emits x.
def outcome_likelihood(path_x):

    s = zeros([4, len(path_x)])
    x_index = alphabet.index(path_x[0])
    for i in range(4):
        s[i,0] = emission_matrix[i, x_index]*1/4
    
    for j in range(1, len(path_x)):
        for i in range(4):
            x_index = alphabet.index(path_x[j])
            s[i, j] = s[0, j-1]*transition_matrix[0,i]*emission_matrix[i,x_index] + s[1, j-1]*transition_matrix[1,i]*emission_matrix[i,x_index] + s[2, j-1]*transition_matrix[2,i]*emission_matrix[i,x_index] + s[3, j-1]*transition_matrix[3,i]*emission_matrix[i,x_index]
    last_column = s[0, len(path_x)-1] + s[1, len(path_x)-1] + s[2, len(path_x)-1] + s[3, len(path_x)-1]    

    return last_column


if __name__ == "__main__":   
    path_x = "xzzyyxyzyyzzyxzzzyxyyyyyyxzyxzyyxzzyxzyzxzzzxxyzxyxyxzzyxyzzyyyyzxxxxxxyxzzyxzzxyzyzzxxyxxyyxyzxyyyz"
    print(outcome_likelihood(path_x))