"""
@BY: Yang LIU
@DATE: 18-09-2020
"""


# return a collection of all the preffix and suffix of k-mers in a given text
def string_composition(text, k):
    
    kmers = []
    for i in range(len(text) - k + 1):
        kmer = text[i: i + k]
        kmers.append(kmer)
        
    return kmers
    

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
def de_bruijn_graph(text, k):

    kmers = string_composition(text, k)
    dic = form_multidic(kmers)
    for preffix in dic.keys():
        suffixs = dic[preffix]
        if len(suffixs) == 1:
            output = preffix + " -> " + suffixs[0]
            print(output)
        else:
            output = preffix + " -> " 
            for suffix in suffixs:
                output += (suffix + ", ")
            output = output[:-2]
            print(output)
                                                      

if __name__ == "__main__":
    
    text = "AAGATTCTCTAAGA"
    k = 4
    de_bruijn_graph(text, k)