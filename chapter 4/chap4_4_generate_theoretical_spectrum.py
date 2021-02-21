"""
@BY: Yang LIU
@DATE: 27-09-2020
"""


# Generate the theoretical spectrum of a cyclic peptide
def generating_theoretical_specctrum(peptide, peptide_code):

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


if __name__ == "__main__":
    peptide = "CAPGSAKHVDYKI"    
    peptide_code = {    "G":57, "A":71, "S":87, "P":97, "V":99, "T":101, "C":103,
                        "I":113, "L":113, "N":114, "D":115, "K":128, "Q":128, 
                        "E":129, "M":131, "H":137, "F":147, "R":156, "Y":163, "W":186   }
    print(generating_theoretical_specctrum(peptide, peptide_code))