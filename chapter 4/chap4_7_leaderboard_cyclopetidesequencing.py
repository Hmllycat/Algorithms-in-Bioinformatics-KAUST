"""
@BY: Yang LIU
@DATE: 27-09-2020
"""

mass_code = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]
peptide_code = {    "G":57, "A":71, "S":87, "P":97, "V":99, "T":101, "C":103,
                    "I":113, "L":113, "N":114, "D":115, "K":128, "Q":128, 
                    "E":129, "M":131, "H":137, "F":147, "R":156, "Y":163, "W":186   }


# Generate the theoretical spectrum of a cyclic peptide, the peptides is character, not number
def generating_theoretical_specctrum(peptide):

    extend_linear = peptide + peptide[:len(peptide)-2]
    masses = [peptide]
    for i in range(len(peptide)):
        for j in range(1, len(peptide)):
            masses.append(extend_linear[i:i+j])
    
    result = [0]
    for mass in masses:
        value = 0
        for aa in mass:
            value += peptide_code[aa]
        result.append(value)

    result = sorted(result)
    return result


# Compute the score of a cyclic peptide against a spectrum.
def cyclopeptide_score(peptide, spectrum):

    theoretical_spectrum = generating_theoretical_specctrum(peptide)
    score = 0
    for mass in theoretical_spectrum:
        if mass in spectrum:
            spectrum.remove(mass)
            score += 1
    
    return score


# return the spectrum of a linear peptide(mass-represented), the peptide is [113,114,128] rather than "LNQ"
# the return result is [0, 113, 114, 128, 227, 242, 355]
def linear_spectrum(peptide):

    masses = peptide.copy()
    masses.append(0)
    for i in range(len(peptide)-1):
        for j in range(i+2, len(peptide)+1):
            masses.append(sum(peptide[i:j]))

    return sorted(masses)


# each time add a number(aa) into exited protein sequence 
# e.g. candidate_peptides = [[1],[2],[3]]    mass_code = [1,2] 
# the result will be [[1,1],[1,2],[2,1],[2,2],[3,1],[3,2]]
def expand(candidate_peptides):
    
    expand_candidates = []
    for peptide in candidate_peptides:        
        for i in mass_code:
            extension = peptide.copy()
            extension.append(i)
            expand_candidates.append(extension)

    return expand_candidates


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
def leaderboard_cyclopetidesequencing(spectrum, n):

    leaderboard = [[]]
    leaderpeptide = []
    while len(leaderboard) > 0:
        leaderboard = expand(leaderboard)
        for peptide in leaderboard.copy():
            if sum(peptide) == max(spectrum):
                if linearpeptide_score(peptide, spectrum) > linearpeptide_score(leaderpeptide, spectrum):
                    leaderpeptide = peptide
            elif sum(peptide) > max(spectrum):
                leaderboard.remove(peptide)
        leaderboard = trim(leaderboard, spectrum, n)
    return leaderpeptide


if __name__ == "__main__":
    peptide = "NQEL"
    spectrum = [0, 99, 113, 114, 128, 227, 257, 299, 355, 356, 370, 371, 484]
    print(cyclopeptide_score(peptide, spectrum))

    n = 10
    spectrum = [0, 71, 113, 129, 147, 200, 218, 260, 313, 331, 347, 389, 460]    
    print(leaderboard_cyclopetidesequencing(spectrum, n))   