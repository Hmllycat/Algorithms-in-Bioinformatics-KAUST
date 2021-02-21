"""
@BY: Yang LIU
@DATE: 03-09-2020
"""


# find the complementary strand
def reverse_complement(text):
    complement = ''
    for item in text:    # first complement the text
        if item == "A":
            value = "T"
        elif item == "T":
            value = "A"
        elif item == "C":
            value = "G"
        else:
            value = "C"
        complement = complement + value
    complement = complement[::-1]    # then reverse the complementary text
    return complement


# find the starting position where pattern appears as a substring of genome
def pattern_matching(pattern, text):
    position = ''
    for i in range(len(text) - len(pattern)):
            fragment = text[i:i + len(pattern)]
            if fragment == pattern:
                position = position + " " + str(i)
    return position


if __name__ == "__main__":
    text = 'ACACAC'
    print(reverse_complement(text))
    text = "TTTTACACTTTTTTGTGTAAAAA"
    pattern = "ACAC"
    print(pattern_matching(pattern, text))

