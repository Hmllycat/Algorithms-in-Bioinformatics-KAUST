"""
@BY: Yang LIU
@DATE: 23-10-2020
"""


def number_of_breakpoints(P):

    count = 0
    for i in range(len(P)+1):
        if i == 0:
            if P[i] != 1:
                count += 1
        elif i == len(P):
            if P[i-1] != len(P):
                count += 1
        else:
            if P[i] - P[i-1] != 1:
                count += 1
        
    return count
    

if __name__ == "__main__":
    P = [+3,+4,+5,-12,-8,-7,-6,+1,+2,+10,+9,-11,+13,+14]
    print(number_of_breakpoints(P))