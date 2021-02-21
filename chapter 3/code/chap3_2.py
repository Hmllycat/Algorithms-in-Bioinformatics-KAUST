"""
@BY: Yang LIU
@DATE: 17-09-2020
"""


def string_composition(text, k):
    output = []
    for i in range(len(text) - k + 1):
        output.append(text[i:i+k])        
    return output


if __name__ == "__main__":
    text = "CAATCCAAC"    
    k = 5
    print(string_composition(text, k))