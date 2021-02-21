"""
@BY: Yang LIU
@DATE: 26-09-2020
"""


def string_reconstruction(patterns):
    string = patterns[0]
    for i in range(1, len(patterns)):
        string += patterns[i][-1]
    return string


def string_spelled_by_gapped_patterns(gappedpattens, k, d):
    first_patterns = []
    second_patterns = []
    for pattern in gappedpattens:
        first_patterns.append(pattern[0])
        second_patterns.append(pattern[1])
    prefix_string = string_reconstruction(first_patterns)
    suffix_string = string_reconstruction(second_patterns)
    for i in range(k+d+1, len(prefix_string)):
        if prefix_string[i] != suffix_string[i-k-d]:
            return "there is no string spelled by the gapped patterns"
    return  prefix_string+suffix_string[-(k+d):]


if __name__ == "__main__":

    k = 4
    d = 2
    gappedpattens = [["GACC", "GCGC"], ["ACCG", "CGCC"], ["CCGA", "GCCG"], ["CGAG", "CCGG"], ["GAGC", "CGGA"]]
    print(string_spelled_by_gapped_patterns(gappedpattens, k, d))

    # with open("../data/dataset_369278_4.txt") as file:
    #     gappedpattens = []
    #     for line in file:
    #         line = line.replace('\n','').split("|")
    #         gappedpattens.append(line)
    # k = 50
    # d = 200
    # print(string_spelled_by_gapped_patterns(gappedpattens, k, d))