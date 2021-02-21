"""
@BY: Yang LIU
@DATE: 24-11-2020
"""

from numpy import *
import sys
sys.setrecursionlimit(15000)


def profile_HMM_multialign(multi_alignment, thre):

    border = len(multi_alignment)*thre
    droped_column = []
    for i in range(len(multi_alignment[0])):
        i_pos_del = [multi_alignment[k][i] for k in range(len(multi_alignment))]
        if i_pos_del.count("-") > border:
            droped_column.append(i)     

    transition_matrix = zeros([(len(multi_alignment[0])-len(alignment_star[0])+1)*3, (len(multi_alignment[0])-len(alignment_star[0])+1)*3])
    transition_dic = {}
    count = 1
    for i in range(len(multi_alignment[0])):
        if i == 0:
            if i in droped_column:
                for j in range(len(multi_alignment)):
                    if multi_alignment[j][i] != "-":
                        if ("S","I0") not in transition_dic:
                            transition_dic[("S","I0")] = 1
                        else:
                            transition_dic[("S","I0")] += 1
                        
            else:
                for j in range(len(multi_alignment)):
                    if multi_alignment[j][i] == "-":
                        if ("S","D1") not in transition_dic:
                            transition_dic[("S","D1")] = 1
                        else:
                            transition_dic[("S","D1")] += 1
                    else:
                        if ("S","M1") not in transition_dic:
                            transition_dic[("S","M1")] = 1
                        else:
                            transition_dic[("S","M1")] += 1
        elif                 







if __name__ == "__main__":   
    multi_alignment = ["EBA", "E-D", "EB-", "EED", "EBD", "EBE", "E-D", "E-D"]
    thre = 0.289
    profile_HMM_multialign(multi_alignment, thre)