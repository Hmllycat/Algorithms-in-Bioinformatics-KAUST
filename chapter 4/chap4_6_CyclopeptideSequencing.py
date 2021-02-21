"""
@BY: Yang LIU
@DATE: 27-09-2020
"""

mass_code = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]


# each time add a number(aa) into exited protein sequence 
# e.g. candidate_peptides = [[1],[2],[3]]    mass = [1,2] 
# the result will be [[1,1],[1,2],[2,1],[2,2],[3,1],[3,2]]
def expand(candidate_peptides, mass):
    
    expand_candidates = []
    for peptide in candidate_peptides:        
        for i in mass:
            extension = peptide.copy()
            extension.append(i)
            expand_candidates.append(extension)

    return expand_candidates


# return the spectrum of a circular peptide(mass-represented), the peptide is [113,114,128] rather than "LNQ"
# the return result is [0, 113, 114, 128, 227, 241, 242, 355]
def circular_spectrum(peptide):

    candidate_spectrum = peptide.copy()
    candidate_spectrum.extend(candidate_spectrum[:len(peptide)])
    masses = [0, sum(peptide)]
    for i in range(len(peptide)):
        for j in range(1, len(peptide)):
            masses.append(sum(candidate_spectrum[i:i+j]))

    return sorted(masses)        


# return the spectrum of a linear peptide(mass-represented), the peptide is [113,114,128] rather than "LNQ"
# the return result is [0, 113, 114, 128, 227, 242, 355]
def linear_spectrum(peptide):

    masses = peptide.copy()
    masses.append(0)
    for i in range(len(peptide)-1):
        for j in range(i+2, len(peptide)+1):
            masses.append(sum(peptide[i:j]))

    return sorted(masses)


# to determine whether the spectrum of peptide is a part of given spectrum or not
def inconsistant(spectrum, peptide):
    for value in peptide:
        if value not in spectrum:
            return True
    return False


# given a theoretical spectrum, return all possible circular peptide whose spectrum matches the given spectrum well.
def cyclopeptide_sequencing(spectrum):

    candidate_peptides = [[]]
    mass = [ i for i in mass_code if i in spectrum]
    final_peptide = []
    while len(candidate_peptides) > 0:
        candidate_peptides = expand(candidate_peptides, mass)
        for peptide in candidate_peptides.copy():            
            peptide_linear_spectrum = linear_spectrum(peptide)
            if sum(peptide) == max(spectrum):
                peptide_circ_spectrum = circular_spectrum(peptide)
                if peptide_circ_spectrum == spectrum and peptide not in final_peptide:
                    final_peptide.append(peptide)
                candidate_peptides.remove(peptide)
            elif inconsistant(spectrum, peptide_linear_spectrum):            
                candidate_peptides.remove(peptide)
        
    return final_peptide
        

if __name__ == "__main__":
    spectrum = [0, 113, 128, 186, 241, 299, 314, 427]
    print(cyclopeptide_sequencing(spectrum))