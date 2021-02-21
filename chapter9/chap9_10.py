"""
@BY: Yang LIU
@DATE: 15-11-2020
"""


def last_to_first(first_column, last_column, idx):
    
    symbol = last_column[idx]
    return_idx = first_column.index(symbol)
    return return_idx


# Input: A string BWT(Text), followed by a collection of Patterns.
# Output: A list of integers, where the i-th integer corresponds to the number of substring matches of the i-th member of Patterns in Text.
def bw_matching(first_column, last_column, bwt, pattern):
    top = 0
    bottom = len(bwt) - 1
    while top <= bottom:
        if len(pattern) > 0:
            symbol = pattern[-1]
            # print(symbol)
            pattern = pattern[:-1]
            # print(pattern)
            if symbol in bwt[top:bottom + 1]:
                top_idx = bwt[top:bottom + 1].index(symbol) + top
                bottom_idx = bottom - bwt[top:bottom + 1][::-1].index(symbol)
                # print(top_idx, bottom_idx)
                top = last_to_first(first_column, last_column, top_idx)
                bottom = last_to_first(first_column, last_column, bottom_idx)
            else:
                return 0
            
        else:
            return bottom - top + 1


def form_first_last(bwt):

    set0 = set(bwt)
    dic = {}
    for value in set0:
        value_array = [i for i in bwt if i == value]
        old_text = [value+str(i) for i in range(1, len(value_array)+1)]
        dic[value] = old_text

    symbols = [i for i in set0]
    symbols.sort()

    first_column = []
    for symbol in symbols:
        first_column.extend(dic[symbol])

    last_column = []
    for symbol in bwt:
        last_column.append(dic[symbol][0])
        dic[symbol].pop(0)

    return first_column, last_column
    
if __name__ == "__main__":   

    bwt = "TCCTCTATGAGATCCTATTCTATGAAACCTTCA$GACCAAAATTCTCCGGC"
    first_column, last_column = form_first_last(bwt)
    patterns = ["CCT","CAC","GAG","CAG","ATC"]
    result = ""
    for pattern in patterns:
        result = result + " " + str(bw_matching(first_column, last_column, bwt, pattern))
    print(result)