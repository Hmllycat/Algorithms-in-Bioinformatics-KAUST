"""
@BY: Yang LIU
@DATE: 28-10-2020
"""

import numpy as np


# Input:  An integer n followed by the adjacency list of a weighted tree with n leaves.
# Output: An n x n matrix (di,j), where di,j is the length of the path between leaves i and j.
def limb_length(n, j, D):

    limblength = float("inf")
    for i in range(n):
        for k in range(n):
            if i != j and k != j:
                length = (D[j, k] + D[i, j] - D[i, k])/2
                if length < limblength:
                    limblength = length
    return limblength


if __name__ == "__main__":   

    n = 4
    j = 1
    D = np.array([  [0,13,21,22],
                    [13,0,12,13],
                    [21,12,0,13],
                    [22,13,13,0]])
    print(limb_length(n, j, D))