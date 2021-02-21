import numpy as np
from math import ceil, floor
from _5101_globalAlignment import readScoreMatrix

def middleEdge(v,w, indelPenalty):

    # Input: Two amino acid strings.
    # Output: A middle edge in the alignment graph in the form "(i, j) (k, l)", where (i, j) connects to (k, l). To compute scores, use the BLOSUM62 scoring matrix and a (linear) indel penalty equal to 5.

    scoreMatrix = readScoreMatrix('data/BLOSUM62.txt')
    
    n = len(v)
    m = len(w)
    middleColumn = floor((m)/2)
    

    prevCol = np.zeros(n+1)
    # for i in range(1,len(prevCol)):
    #     prevCol[i] = prevCol[i-1] - indelPenalty
    # print('col', prevCol)
    for j in range(1,middleColumn+2):
        currCol =  np.zeros(n+1)
        currCol[0] = prevCol[0] -indelPenalty
       
        for i in range(1,n+1):
            incomingUp = currCol[i-1] - indelPenalty
            incomingLeft = prevCol[i] - indelPenalty

            if middleColumn < len(w):
                indexW =  aminos[w[j-1]]
                indexV = aminos[v[i-1]]
               
                match = scoreMatrix[indexV][indexW]
                # print(match, v[i-1], indexV, w[j-1],indexW)
                incomingDiag = prevCol[i-1] + match
                currCol[i] = max(incomingUp, incomingLeft, incomingDiag)
            else:
                currCol[i] = max(incomingUp, incomingLeft)

        if j < middleColumn+1:
            prevCol = currCol
    # print("jota: ", j, "middle", middleColumn)
  #  print("currCol", prevCol, currCol)
    start_row = np.argmax(prevCol)
    start = (start_row, j-1)

    score = prevCol[start_row]

    right = currCol[start_row]

    if start_row < len(currCol)-1:
        diag  = currCol[start_row+1]
        down  = prevCol[start_row+1]
    else:
        diag = float('-inf')
        down = float('-inf')


    direction = right
    dirStr = 'right'
    end = (start_row, j)

    if diag >= direction:
        direction = diag
        dirStr = 'diag'
        end = (start_row+1,j)

    if down >= direction:
        direction = end
        dirStr = 'down'
        end = (start_row+1,j-1)

 

    return (start, end, score, dirStr)

aminos = {
        'A':  0, 
        'C':  1, 
        'D':  2, 
        'E':  3, 
        'F':  4, 
        'G':  5, 
        'H':  6, 
        'I':  7, 
        'K':  8, 
        'L':  9, 
        'M': 10, 
        'N': 11, 
        'P': 12, 
        'Q': 13, 
        'R': 14, 
        'S': 15, 
        'T': 16, 
        'V': 17, 
        'W': 18, 
        'Y': 19}

if __name__ == "__main__":
    file = open('C:/Users/树下的猫/Downloads/dataset_369321_14.txt', 'r')

    v = file.readline().rstrip('\n')
    w = file.readline().rstrip('\n')

    indelPenalty = 5

    n = len(v)
    print(middleEdge(v,w,indelPenalty))