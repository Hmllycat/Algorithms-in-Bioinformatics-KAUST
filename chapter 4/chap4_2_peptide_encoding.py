"""
@BY: Yang LIU
@DATE: 27-09-2020
"""


def protein_translation(rna_string, genetic_code):

    protein = ""
    number = int(len(rna_string)/3)
    for i in range(number):
        codon = rna_string[3*i: 3*i+3]
        if genetic_code[codon] == "*":
            return protein
        else:
            protein += genetic_code[codon]

    return protein


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


# Find substrings of a genome encoding a given amino acid sequence.
# We say that a DNA string Pattern encodes an amino acid string Peptide if the RNA string transcribed from either Pattern or its reverse complement Pattern translates into Peptide. 
def peptide_encoding(dna_string, protein_sequence, genetic_code):

    result = []
    k = len(protein_sequence)*3

    for i in range(len(dna_string) - k + 1):
        pattern = dna_string[i: i+k]
        reverse_pattern = reverse_complement(pattern)
        rna = pattern.replace("T","U")
        reverse_rna = reverse_pattern.replace("T","U")
        if protein_translation(rna, genetic_code) == protein_sequence or protein_translation(reverse_rna, genetic_code) == protein_sequence:
            result.append(pattern)
    
    return result


if __name__ == "__main__":
    rna_string = "AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA"    
    genetic_code = {    "AAA": "K", "AAC": "N", "AAG": "K", "AAU": "N", "ACA": "T",
                        "ACC": "T", "ACG": "T", "ACU": "T", "AGA": "R", "AGC": "S",
                        "AGG": "R", "AGU": "S", "AUA": "I", "AUC": "I", "AUG": "M",
                        "AUU": "I", "CAA": "Q", "CAC": "H", "CAG": "Q", "CAU": "H",
                        "CCA": "P", "CCC": "P", "CCG": "P", "CCU": "P", "CGA": "R",
                        "CGC": "R", "CGG": "R", "CGU": "R", "CUA": "L", "CUC": "L",
                        "CUG": "L", "CUU": "L", "GAA": "E", "GAC": "D", "GAG": "E",
                        "GAU": "D", "GCA": "A", "GCC": "A", "GCG": "A", "GCU": "A",
                        "GGA": "G", "GGC": "G", "GGG": "G", "GGU": "G", "GUA": "V",
                        "GUC": "V", "GUG": "V", "GUU": "V", "UAA": "*", "UAC": "Y",
                        "UAG": "*", "UAU": "Y", "UCA": "S", "UCC": "S", "UCG": "S",
                        "UCU": "S", "UGA": "*", "UGC": "C", "UGG": "W", "UGU": "C",
                        "UUA": "L", "UUC": "F", "UUG": "L", "UUU": "F"}
    print(protein_translation(rna_string, genetic_code))

    dna_string = "ATGGCCATGGCCCCCAGAACTGAGATCAATAGTACCCGTATTAACGGGTGA"
    protein_sequence = "MA"
    print(peptide_encoding(dna_string, protein_sequence, genetic_code))