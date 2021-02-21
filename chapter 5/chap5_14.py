"""
@BY: Yang LIU
@DATE: 12-10-2020
"""

from numpy import *
import sys
sys.setrecursionlimit(15000)


# store backtracking pointers
def lsc_backtrack(v, w, u):

    s = zeros([len(v)+1,len(w)+1, len(u)+1])
    backtrack = full(shape=(len(v),len(w),len(u)),fill_value='XXXX')
    for i in range(1,len(v)+1):
        for j in range(1, len(w)+1):
            for k in range(1, len(u)+1):
                match = 0
                if v[i-1] == w[j-1] and w[j-1] == u[k-1]:
                    match = 1
                s[i, j, k] = max(s[i-1, j, k], s[i, j-1, k], s[i, j, k-1], s[i-1, j-1, k], s[i-1, j, k-1], s[i, j-1, k-1], s[i-1, j-1, k-1] + match)
                if s[i, j, k] == s[i, j-1, k-1]:
                    backtrack[i-1, j-1, k-1] = "yizi"
                elif s[i, j, k] == s[i-1, j, k-1]:
                    backtrack[i-1, j-1, k-1] = "sdzi"
                elif s[i, j, k] == s[i-1, j-1, k]:
                    backtrack[i-1, j-1, k-1] = "xdyi"
                elif s[i, j, k] == s[i-1, j-1, k-1] + match:
                    backtrack[i-1, j-1, k-1] = "matc"
                elif s[i, j, k] == s[i-1, j, k]:
                    backtrack[i-1, j-1, k-1] = "xdel"
                elif s[i, j, k] == s[i, j-1, k]:
                    backtrack[i-1, j-1, k-1] = "yins"
                elif s[i, j, k] == s[i, j, k-1]:
                    backtrack[i-1, j-1, k-1] = "zins"

    i = len(v)
    j = len(w)
    k = len(u)
    print(s[i, j, k])
    return backtrack 


# Input: Two strings s and t.
# Output: A longest common subsequence of s and t. (Note: more than one solution may exist, in which case you may output any one.)
def output_lsc(backtrack, v, w, u, i, j, k):

    global first_string
    global second_string
    global third_string
    if i == 0:
        if j == 0:
            if k == 0:
                return ""
            else:
                first_string += "-" 
                second_string += "-"
                third_string += u[k-1]
                return output_lsc(backtrack, v, w, u, i, j, k-1)
        elif k == 0:
            first_string += "-" 
            second_string += w[j-1]
            third_string += "-"
            return output_lsc(backtrack, v, w, u, i, j-1, k)
        else:
            first_string += "-" 
            second_string += w[j-1]
            third_string += u[k-1]            
            return output_lsc(backtrack, v, w, u, i, j-1, k-1)
    elif j == 0:
        if k == 0:
            first_string += v[i-1] 
            second_string += "-"
            third_string += "-"
            return output_lsc(backtrack, v, w, u, i-1, j, k)
        else:
            first_string += v[i-1] 
            second_string += "-"
            third_string += u[k-1]
            return output_lsc(backtrack, v, w, u, i-1, j, k-1)
    elif k == 0:
        first_string += v[i-1] 
        second_string += w[j-1]
        third_string += "-"
        return output_lsc(backtrack, v, w, u, i-1, j-1, k)
    elif backtrack[i-1, j-1, k-1] == "xdel":
        first_string += v[i-1] 
        second_string += "-"
        third_string += "-"
        return output_lsc(backtrack, v, w, u, i-1, j, k)
    elif backtrack[i-1, j-1, k-1] == "yins":
        first_string += "-"
        second_string += w[j-1]
        third_string += "-"
        return output_lsc(backtrack, v, w, u, i, j-1, k)
    elif backtrack[i-1, j-1, k-1] == "zins":
        first_string += "-"
        second_string += "-"
        third_string += u[k-1]
        return output_lsc(backtrack, v, w, u, i, j, k-1)
    elif backtrack[i-1, j-1, k-1] == "xdyi":
        first_string += v[i-1]
        second_string += w[j-1]
        third_string += "-"
        return output_lsc(backtrack, v, w, u, i-1, j-1, k)
    elif backtrack[i-1, j-1, k-1] == "xdzi":
        first_string += v[i-1]
        second_string += "-"
        third_string += u[k-1]
        return output_lsc(backtrack, v, w, u, i-1, j, k-1)
    elif backtrack[i-1, j-1, k-1] == "yizi":
        first_string += "-"
        second_string += w[j-1]
        third_string += u[k-1]
        return output_lsc(backtrack, v, w, u, i, j-1, k-1)
    else:
        first_string += v[i-1]
        second_string += w[j-1]
        third_string += u[k-1]
        return output_lsc(backtrack, v, w, u, i-1, j-1, k-1)

if __name__ == "__main__":   

    v = "CCTGACAG"
    w = "TCCATGTT"
    u = "TGCCTTGG"
    first_string = ""
    second_string = ""
    third_string = ""
    backtrack = lsc_backtrack(v, w, u)
    # print(backtrack)
    i = len(v)
    j = len(w)
    k = len(u)
    output_lsc(backtrack, v, w, u, i, j, k)   
    print(first_string[::-1])
    print(second_string[::-1])
    print(third_string[::-1])