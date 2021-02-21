"""
@BY: Yang LIU
@DATE: 02-10-2020
"""

from numpy import *


# Input: Integers n and m, followed by an n × (m + 1) matrix Down and an (n + 1) × m matrix Right. The two matrices are separated by the "-" symbol.
# Output: The length of a longest path from source (0, 0) to sink (n, m) in the rectangular grid whose edges are defined by the matrices Down and Right.
def man_hattan_tourist(n, m, down, right):
    s = zeros([n+1, m+1])
    for i in range(1, n+1):
        s[i, 0] = s[i-1, 0] + down[i-1, 0]
    for j in range(1, m+1):
        s[0, j] = s[0, j-1] + right[0, j-1]
    for i in range(1, n+1):
        for j in range(1, m+1):
            s[i, j] = max(s[i-1, j] + down[i-1, j], s[i, j-1] + right[i, j-1])
    return s[n,m]


if __name__ == "__main__":   

    n = 4
    m = 4
    down = array([[1, 0, 2, 4, 3],[4, 6, 5, 2, 1],[4, 4, 5, 2, 1],[5, 6, 8, 5, 3]])
    right = array([[3, 2, 4, 0],[3, 2, 4, 2],[0, 7, 3, 3],[3, 3, 0, 2],[1, 3, 2, 2]])
    print(man_hattan_tourist(n, m, down, right))