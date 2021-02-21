"""
@BY: Yang LIU
@DATE: 04-09-2020
"""


# find a position in a genome where the skew diagram attains a minimum
def minimum_skew(text):
    count = 0
    d = { 0:0 }
    for i in range(len(text)):
        if text[i] == "C":
            count = count - 1
        elif text[i] == "G":
            count = count + 1
        d[i+1] = count
    return [x for x in d.keys() if d[x] == min(d.values())]


if __name__ == "__main__":
    text = 'ACCG'
    print(minimum_skew(text))
