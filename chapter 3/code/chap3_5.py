"""
@BY: Yang LIU
@DATE: 18-09-2020
"""


# the key is the first (k-1)elements and value is the last (k-1)elements of given kmer, a key could have many values.
def form_multidic(kmers):

    dic = {}
    for kmer in kmers:
        a = kmer[0:len(kmer)-1]
        b = kmer[1:len(kmer)]
        if a in dic.keys():
            dic[a].append(b)
        else:
            dic[a] = [b]

    return dic


# The overlap graph Overlap(Patterns), in the form of an adjacency list.    
def de_bruijn_graph_from_kmers(kmers):

    dic = form_multidic(kmers)
    output = []
    for preffix in dic.keys():
        suffixs = dic[preffix]
        if len(suffixs) == 1:
            output.append(preffix + " -> " + suffixs[0])
        else:
            result = preffix + " -> " 
            for suffix in suffixs:
                result += (suffix + ", ")
            result = result[:-2]
            # print(result)
            output.append(result)       
    return output


if __name__ == "__main__":
    kmers = ["AGGT","GGCT","AGGC"]
    print(de_bruijn_graph_from_kmers(kmers))
    # with open("../data/dataset_369270_8.txt") as file:
    #     kmers = []
    #     for line in file:
    #         kmer = line.replace("\n", "")
    #         kmers.append(kmer)

    # result = de_bruijn_graph_from_kmers(kmers) 
    # for i in result:
    #     print(i)     