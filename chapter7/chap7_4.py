"""
@BY: Yang LIU
@DATE: 23-10-2020
"""


def k_sorting_reversal(P, k):

    idx = P.index(k)
    reverse_part = P[abs(k)-1:idx+1]
    after_reverse = [-i for i in reverse_part[::-1]]
    del P[abs(k)-1:idx+1]
    P = P[:abs(k)-1] + after_reverse + P[abs(k)-1:]
    return P    


def add(P):
    string = ""
    for i in P:
        if i < 0:
            string += str(i) + " "
        else:
            string += "+" + str(i) + " "
    return string


def greedy_sorting(P):

    return_list = []
    for k in range(1, len(P)+1):
        if k != abs(P[k-1]):
            if k in P:
                P = k_sorting_reversal(P, k)
                return_list.append(P.copy())
                P[k-1] = k
                return_list.append(P.copy())
            else:
                P = k_sorting_reversal(P, -k)
                return_list.append(P.copy())
        elif -k == P[k-1]:
            P[k-1] = k
            return_list.append(P.copy())
    return return_list


if __name__ == "__main__":   

    P = [-91,+112,+28,-119,+129,-42,-57,+76,-89,+115,-63,+50,-71,-21,-107,-70,-122,+82,+12,-36,-64,+79,-22,+87,+1,+32,-83,+103,+54,-27,-95,-105,+121,-73,+67,+127,+55,-56,+94,+23,+37,+10,+113,-116,+86,-47,+96,-4,-19,+124,+13,-46,-48,-58,-30,+106,-11,+35,+97,-40,+41,+126,+84,-72,-45,+114,-100,+39,-18,-90,+78,+74,+65,+24,+102,+117,+81,-15,-5,-25,+99,-98,+128,-66,+31,-33,-44,+2,+34,+52,-110,+26,-6,+109,-8,+108,-77,+60,-53,+101,+59,-43,-120,-51,+111,+80,+14,+93,-69,-118,+49,+17,+62,-123,-104,+88,-9,-61,+3,-16,-75,+68,-20,-7,-125,-85,+29,+38,+92]
    
    result = greedy_sorting(P)
    with open("D:/bioinformatics homework/chapter 7/7_4_result.txt","w") as output:
        for reversal in result:
            string = add(reversal)
            string = string[:-1]
            output.write("%s\n"%string)