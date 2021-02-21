"""
@BY: Yang LIU
@DATE: 15-11-2020
"""


# Input: A string Text.
# Output: SuffixArray(Text).
def suffix_array_construction(text):
    
    dic = {}
    array = []
    for i in range(len(text)):
        key = text[i:]
        value = i
        dic[key] = value
        array.append(key)

    array.sort()
    suffix_array = []
    for key in array:
        suffix_array.append(dic[key])
    return suffix_array


if __name__ == "__main__":   

    text = "AACGATAGCGGTAGA$"
    print(suffix_array_construction(text))