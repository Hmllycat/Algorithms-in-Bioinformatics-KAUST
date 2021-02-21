"""
@BY: Yang LIU
@DATE: 18-09-2020
"""


# the key is the first (k-1)elements and value is the last (k-1)elements of given kmer
def form_dic(kmers):

    dic = {}
    for kmer in kmers:
        a = kmer[0:len(kmer)-1]
        b = kmer[1:len(kmer)]
        dic[a] = b   

    return dic
    

# String Reconstruction as a Walk in the Overlap Graph
def genome_path(kmers):

    dic = form_dic(kmers)
    for key in dic.keys():
        if key not in dic.values():
            first = key[0] + dic[key]   # only the first (k-1)elements of first k-mer won't match any of the last (k-1)elements of any other kmers

    k = len(kmers[0])
    for i in range(len(kmers) - 1):
        key = first[i+1:i+k]
        first += dic[key][-1]

    return first
    

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
    for key in dic.keys():
        value = dic[key]
        value = sorted(set(value),key = value.index)   #remove duplicates from patterns
        # print(value)
        dic[key] = value
    # print(dic)
    return dic


# find the key of a value in a dict which a value refers to a list
def find_key(dic, suffix):
    keys = []
    for key in dic.keys():
        if suffix in dic[key]:
            keys.append(key)
    return keys


# The overlap graph Overlap(Patterns), in the form of an adjacency list.    
def overlap_graph(kmers):

    dic = form_multidic(kmers)
    all_suffixs = []
    for values in dic.values():
        for value in values:
            all_suffixs.append(value)   #   find all the suffixs of kmers
    for preffix in dic.keys():
        suffixs = dic[preffix]
        # print(suffixs)
        if preffix in all_suffixs:      
            # print(preffix)
            preffixs = find_key(dic, preffix)       # find the preffix0s that take given preffix as its suffix
            # print(preffixs)
            for preffix0 in preffixs:   
            # print(index)           
                if len(suffixs) == 1:
                    output = preffix0[0] + preffix + " -> " + preffix[0] + suffixs[0]
                    print(output)
                else:
                    output = preffix0[0] + preffix + " -> "
                    for suffix in suffixs:
                        output += (preffix[0] + suffix + ", ")
                    output = output[:-2]
                    print(output)
                           
                           
if __name__ == "__main__":
    kmers = ["ACCGA","CCGAA","CGAAG","GAAGC","AAGCT"]
    print(genome_path(kmers))
    # with open("../data/dataset_369268_10.txt") as file:
    #     kmers = []
    #     for kmer in file:
    #         kmer = kmer[:-1]
    #         kmers.append(kmer)
    # overlap_graph(kmers)