"""
@BY: Yang LIU
@DATE: 30-09-2020
"""

# Input: A collection of integers Spectrum. 
# Output: The list of elements in the convolution of Spectrum. If an element has multiplicity k, it should appear exactly k times; you may return the elements in any order. the output should not include any zero.
# sample input: [0, 137, 186, 323]   sample output: [137, 137, 186, 186, 323, 49]
def special_convolution(spectrum):
    
    masses = []
    for i in range(1, len(spectrum)):
        for j in range(len(spectrum)-i):
            masses.append(spectrum[-i]-spectrum[j])
    while 0 in masses:
        masses.remove(0)

    return masses


# input a experimental spectrum and integer m. output the m highest convolution masses
def count_convolution(spectrum, m):

    freq_table = {}
    convolution = special_convolution(spectrum)
    frequency = []
    for i in set(convolution):
        freq = convolution.count(i)
        if i >= 57 and i < 200:
            freq_table[i] = freq
            frequency.append(freq)
    frequency = sorted(frequency)
    if len(frequency) >= m:
        top_m = frequency[-m]
        result = []
        for key in freq_table.keys():
            if freq_table[key] >= top_m:
                result.append(key)
        return result
    else:
        return list(freq_table.keys())


# each time add a number(aa) into exited protein sequence 
# e.g. candidate_peptides = [[1],[2],[3]]    mass_code = [1,2] 
# the result will be [[1,1],[1,2],[2,1],[2,2],[3,1],[3,2]]
def expand(candidate_peptides, mass_code):
    
    expand_candidates = []
    for peptide in candidate_peptides:        
        for i in mass_code:
            extension = peptide.copy()
            extension.append(i)
            expand_candidates.append(extension)

    return expand_candidates


# return the spectrum of a linear peptide(mass-represented), the peptide is [113,114,128] rather than "LNQ"
# the return result is [0, 113, 114, 128, 227, 242, 355]
def linear_spectrum(peptide):

    masses = peptide.copy()
    masses.append(0)
    for i in range(len(peptide)-1):
        for j in range(i+2, len(peptide)+1):
            masses.append(sum(peptide[i:j]))

    return sorted(masses)


# Compute the score of a linear peptide against a spectrum.
def linearpeptide_score(peptide, spectrum):
    
    theoretical_spectrum = linear_spectrum(peptide)
    score = 0
    new_spectrum = spectrum.copy()
    for mass in theoretical_spectrum:
        if mass in new_spectrum:
            new_spectrum.remove(mass)
            score += 1
    
    return score    


# leaderboard is a list of multiple candidate peptides, e.g. [[57,71],[71,81]...]  spectrum is a numeric spectrum. e.g. [0, 99, 113, 114, 128, 227, 257, 299, 355, 356, 370, 371, 484]
# return back the top n peptides with highest score.
def trim(leaderboard, spectrum, n):
    
    if len(leaderboard) < n:
        return leaderboard
    else:
        scores = []
        for peptide in leaderboard:
            score = linearpeptide_score(peptide, spectrum)
            scores.append(score)
        
        scores = sorted(scores)
        top_n = scores[-n]
        n_highest_score_peptides = []
        for peptide in leaderboard:
            if linearpeptide_score(peptide, spectrum) >= top_n:
                n_highest_score_peptides.append(peptide)

        return n_highest_score_peptides


# Input: A collection of integers Spectrum.
# Output: A cyclic peptide Peptide maximizing Score(Peptide, Spectrum) over all peptides Peptide with mass equal to ParentMass(Spectrum).
def convolution_leaderboard_cyclopetidesequencing(m, n, spectrum):

    leaderboard = [[]]
    leaderpeptide = []
    mass_code = count_convolution(spectrum, m)
    while len(leaderboard) > 0:
        leaderboard = expand(leaderboard, mass_code)
        for peptide in leaderboard.copy():
            if sum(peptide) == max(spectrum):
                if linearpeptide_score(peptide, spectrum) > linearpeptide_score(leaderpeptide, spectrum):
                    leaderpeptide = peptide
            elif sum(peptide) > max(spectrum):
                leaderboard.remove(peptide)
        leaderboard = trim(leaderboard, spectrum, n)
    return leaderpeptide  


if __name__ == "__main__":   

    spectrum = [0, 137, 186, 323]
    print(special_convolution(spectrum))
    # result = special_convolution(spectrum)
    # result = [str(i) for i in result]
    # with open("D:/bioinformatics homework/result.txt","w") as output:
    #     for i in result:
    #         output.write("%s "%i)

    m = 19
    n = 363
    spectrum = [
                    0, 57, 87, 97, 103, 103, 113, 115, 129, 131, 131, 137, 137, 
                    160, 188, 190, 212, 218, 234, 240, 240, 242, 244, 246, 247, 
                    266, 291, 303, 321, 331, 337, 343, 349, 369, 373, 377, 378, 
                    378, 379, 400, 406, 434, 452, 460, 474, 480, 482, 491, 493, 
                    503, 506, 509, 510, 537, 563, 583, 589, 590, 597, 603, 613, 
                    619, 620, 622, 624, 640, 640, 700, 700, 716, 718, 720, 721, 
                    727, 737, 743, 750, 751, 757, 777, 803, 830, 831, 834, 837, 
                    847, 849, 858, 860, 866, 880, 888, 906, 934, 940, 961, 962, 
                    962, 963, 967, 971, 991, 997, 1003, 1009, 1019, 1037, 1049, 
                    1074, 1093, 1094, 1096, 1098, 1100, 1100, 1106, 1122, 1128, 
                    1150, 1152, 1180, 1203, 1203, 1209, 1209, 1211, 1225, 1227, 
                    1237, 1237, 1243, 1253, 1283, 1340
                ]
    print (convolution_leaderboard_cyclopetidesequencing(m, n, spectrum))