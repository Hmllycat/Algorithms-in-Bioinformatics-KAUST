"""
@BY: Yang LIU
@DATE: 12-10-2020
"""

from numpy import *
import sys
sys.setrecursionlimit(15000)


score_matrix = array([[4,0,-2,-1,-2,0,-2,-1,-1,-1,-1,-2,-1,-1,-1,1,0,0,-3,-2],
                [0,9,-3,-4,-2,-3,-3,-1,-3,-1,-1,-3,-3,-3,-3,-1,-1,-1,-2,-2],
                [-2,-3,6,2,-3,-1,-1,-3,-1,-4,-3,1,-1,0,-2,0,-1,-3,-4,-3],
                [-1,-4,2,5,-3,-2,0,-3,1,-3,-2,0,-1,2,0,0,-1,-2,-3,-2],
                [-2,-2,-3,-3,6,-3,-1,0,-3,0,0,-3,-4,-3,-3,-2,-2,-1,1,3],
                [0,-3,-1,-2,-3,6,-2,-4,-2,-4,-3,0,-2,-2,-2,0,-2,-3,-2,-3],
                [-2,-3,-1,0,-1,-2,8,-3,-1,-3,-2,1,-2,0,0,-1,-2,-3,-2,2],
                [-1,-1,-3,-3,0,-4,-3,4,-3,2,1,-3,-3,-3,-3,-2,-1,3,-3,-1],
                [-1,-3,-1,1,-3,-2,-1,-3,5,-2,-1,0,-1,1,2,0,-1,-2,-3,-2],
                [-1,-1,-4,-3,0,-4,-3,2,-2,4,2,-3,-3,-2,-2,-2,-1,1,-2,-1],
                [-1,-1,-3,-2,0,-3,-2,1,-1,2,5,-2,-2,0,-1,-1,-1,1,-1,-1],
                [-2,-3,1,0,-3,0,1,-3,0,-3,-2,6,-2,0,0,1,0,-3,-4,-2],
                [-1,-3,-1,-1,-4,-2,-2,-3,-1,-3,-2,-2,7,-1,-2,-1,-1,-2,-4,-3],
                [-1,-3,0,2,-3,-2,0,-3,1,-2,0,0,-1,5,1,0,-1,-2,-2,-1],
                [-1,-3,-2,0,-3,-2,0,-3,2,-2,-1,0,-2,1,5,-1,-1,-3,-3,-2],
                [1,-1,0,0,-2,0,-1,-2,0,-2,-1,1,-1,0,-1,4,1,-2,-3,-2],
                [0,-1,-1,-1,-2,-2,-2,-1,-1,-1,-1,0,-1,-1,-1,1,5,0,-2,-2],
                [0,-1,-3,-2,-1,-3,-3,3,-2,1,1,-3,-2,-2,-3,-2,0,4,-3,-1],
                [-3,-2,-4,-3,1,-2,-2,-3,-3,-2,-1,-4,-4,-2,-3,-3,-2,-3,11,2],
                [-2,-2,-3,-2,3,-3,2,-1,-2,-1,-1,-2,-3,-1,-2,-2,-2,-1,2,7]])  

aa = ["A","C","D","E","F","G","H","I","K","L","M","N","P","Q","R","S","T","V","W","Y"]


def from_source(middle_column, v, w):
    s = zeros([len(v)+1, middle_column+1])
    for i in range(len(v)+1):
        s[i,0] = -5*i
    for j in range(middle_column+1):
        s[0,j] = -5*j
    for i in range(1,len(v)+1):
        for j in range(1, middle_column+1):
            x_index = aa.index(v[i-1])
            y_index = aa.index(w[j-1])
            match = score_matrix[x_index, y_index]
            s[i, j] = max(s[i-1, j] - 5, s[i, j-1] - 5, s[i-1, j-1] + match)
    return s[:, middle_column]


def to_sink(middle_column, v, w):
    
    middle_column_reverse = len(w)-middle_column
    v_reverse = v[::-1]
    w_reverse = w[::-1]
    s = zeros([len(v)+1, middle_column_reverse+1])
    for i in range(len(v)):
        s[i,0] = -5*i
    for j in range(middle_column_reverse+1):
        s[0,j] = -5*j
    for i in range(1,len(v)+1):
        for j in range(1, middle_column_reverse+1):
            x_index = aa.index(v[i-1])
            y_index = aa.index(w[j-1])
            match = score_matrix[x_index, y_index]
            s[i, j] = max(s[i-1, j] - 5, s[i, j-1] - 5, s[i-1, j-1] + match)
    return s[:, middle_column_reverse]   


def find_middle_node(top, bottom, left, right, v, w):

    middle_column = int((right+left)/2)
    longest_length = float('-inf')
    source_score = from_source(middle_column, v, w)
    sink_score = to_sink(middle_column, v, w)
    if bottom-top > 1:
        for i in range(top, bottom+1):
            length = source_score[i] + sink_score[i]
            if length >= longest_length:
                longest_length = length
                middle_row = i-1
    else:
        middle_row = top
    return (middle_row, middle_column)


def find_middle_edge(top, bottom, left, right, v, w):
 
    middle_node = find_middle_node(top, bottom, middle_column, v, w)
    x_index = aa.index(v[middle_node[0]])
    y_index = aa.index(w[middle_node[1]])
    match = score_matrix[x_index, y_index]
    if middle_node[0] == bottom:
        delete = float('-inf')
        mat = float('-inf')
        if middle_node[1] == right:
            return
    else:
        delete = to_sink(middle_node[1]+1, v, w)[len(v)-middle_node[0]+1] - 5
    if middle_node[1] == right:
        insert = float('-inf')
        mat = float('-inf')
    else:
        insert = to_sink(middle_node[1], v, w)[len(v)-middle_node[0]] - 5
    if middle_node[0] != bottom and middle_node[1] != right:
        mat = to_sink(middle_node[1]+1, v, w)[middle_node[0]] + match
    if max(delete, insert, mat) == mat:
        middle_edge = (middle_node[0]+1, middle_node[1]+1)
    elif max(delete, insert, mat) == insert:
        middle_edge = (middle_node[0]+1, middle_node[1])
    else:
        middle_edge = (middle_node[0], middle_node[1]+1)
    
    return middle_node, middle_edge


def linear_space_alignment(v, w, top, bottom, left, right):
    if left == right:
        return("down"*(top-bottom))
    if top == bottom:
        return("right"*(right-left))
    middle = int((right+left)/2)
    # print(middle)
    # print(top, bottom)
    midedge = find_middle_edge(top, bottom, left, right, v, w)
    print(midedge)
    midnode = midedge[0][0]
    linear_space_alignment(v, w, top, midnode, left, middle)
    # print(midedge)
    if midedge[0][0] == midedge[1][0] or (midedge[1][0] - midedge[0][0] == 1 and midedge[1][1] - midedge[0][1] == 1):
        middle += 1
    if midedge[0][1] == midedge[1][1] or (midedge[1][0] - midedge[0][0] == 1 and midedge[1][1] - midedge[0][1] == 1):
        midnode += 1
    linear_space_alignment(v, w, midnode, bottom, middle, right)


if __name__ == "__main__":   

    # v = "TWLNSACYGVNFRRLNPMNKTKWDCWTWVPMVMAAQYLCRIFIPVMDHWEFFGDWGLETWRLGIHDHVKIPNFRWSCELHIREHGHHFKTRFLKHNQFTQCYGLMPDPQFHRSYDVACQWEVTMSQGLMRFHRQNQIEKQRDRTSTYCMMTIGPGFTSNGYDPFVTITITPVQEPVENWFTPGGSMGFMIISRYMQMFFYLTRFSDMTYLVGVHCENYVCWNNVAKFLNGNLQGIFDQGERAYHQFVTWHSYSQYSRCSVGRYACEQAMSRVNSKMTWHWPIRDQGHEHFSEQYLSEKRNPPCNPRIGNAGQHFYEIHRIAHRVAMCNWAPQGQHPGGPTPHDVETCLWLWSLCLKGSDRGYVDRPWMFLADQLGEANLTLITMFHGCTRGCLMWFMDWEECVCSYSVVNPRCHGSEQWSVQNLGWRTCDTLISLWEPECDKHNTPPCLHWEFEDHPSQLRPVMMCDKYVQSIPTDAKWAWTYSKDFVISHWLIWTPIKLEECVFPQINRLWGTACNQGSQKIVIQNVWLRPSSFFQERSKCSDSSCILNVGGSNVNITGKETRTHVPILHMHEIDLISTASSGMRHNLILPHGMLMLHMNWHHSTRAMNPYSSLKLIPWTFQVCETDDRDQNVATHVADPCHKGEDQEIRCCKGGVDHQWKGDRMWMMCMPDMNYVKQDQAPSGTCEGACENYPADKDKCYMIFTIVFDYRRCTKKVCIWISGFPVDAFNLISIANAGFFCCWLEPTELKWRRTFYLGKGTQGWMCTFPHRNIIPVIICAGFGRWVQGEVPFRPVAQISAHSSDRRQGHHPPGTNMCHDYGDQYPIKRVGMQVEEDDGASYCDCAADWKLADMYEADHLSIGVIDFTDWIYPKNGGIWSEIIKSHFHWYHWETPQNTVGAFNTIVGINGSDMCIYHGNTQWEFGWCWKWLNHGHMRNQGPCHLGILEGRISKFAQVTSWWWQTKHDKDWSIEPYGRHWGEAGRPYTYNYCWMRWAIVYNHGNVISVELVPFMDEYPGKCNKEDVQFELFSPMQA"    
    # w = "LWFKFLQCIFQYFKDQQETNCIWTFSPFSEHICQRVCQVYWNWNTPSSRTSDPRELFANSTIHNNRCGEWRYMFYHTRTLVQTAPLMKETLHSDGKHSMYCEQRHFFRSSYLIKVNYDVSHYLELYTFSEIPWKLTTHGWDGFSWFLLVNSCCTFDIDGKCGILSQCGMSRAFRTRQEDAYHFQTSLMHLHLHLHVQEGKHEKADLFAQFYNMLPMHGGTCGRNTEPSDLFDSATMNKYMAEHPASCKACPNVSKECFVYWWSHDFTKKHKLIEFSCGRDTGQTTQRTWNVDENEGGKWIWRFHYFMRAKALQIDPKFKPYWNEPRAIMRPGHVTAAPCICAQHSQNETAVCNRDQMHIHAIEFQQYHSRAFGEVQTWCDIGKENENDFIYEQHWWLVGGTEGMAGVIWKFVCARCRTQDCDFWKTCLTYSAQPMMKVYDTIFYVNSINPWEFEDHPSQCDKCVQSIPTDAKYAICGKFVISHWLYWTPQKFEECVHNNVRCAPMGNRLWGTACMVIQNVWLRPSMGSHFSCILNVGGSNINIQGKETWTHVPILHMHEIDLISTASSGMETCKPCFLSGPTIHMGFSYEIRAQPYSRDYFCMDWMQEADEVDHNRCETVQPTLPLLQQFEWKTSCMGQRWITIFCDHCQIVCFSTFFCVMPTFLPNTSILDKFYCIYLSISWTHYCNVHALGFIMRLHYSYMGWKEHKRMHAWDIGLDELWAQEGIQRAQLWCGDEFEVAKYPEWITEARTAIATRPWFHNCYIKPWWIREKHLWFGKESKLDHGHRGAMFTPVANDNTEWMHHWYMFCWAGSKNRLKRQIKEKLIFIIKFMITEFGLFLMIDYTQCYIAWMWAYTGIACYIDWEKCLKHDLTTTDLGCCVYRLFKWYEVRHRAPPQVNTRLPWSQIPMVAIQCNIVDECKEQWHFSYKASFVVEYLCPGCCTNGNRWQWYQVKETPFMYAFAASIFGFHHENLVVFITGSVTIPNGLFGCIAWTSPKPVQKTPASANTIIAYDKCILMG"
    # top = len(v)
    # bottom = 0
    # middle_column = int(len(w)/2)
    # print(find_middle_edge(top, bottom, middle_column, v, w, score_matrix))

    v = "PLEASANTLY"
    w = "MEASNLY"
    top = 0
    bottom = len(v)
    right = len(w)
    left = 0
    # print(find_middle_edge(top, bottom, left, right, v, w))
    print(linear_space_alignment(v, w, top, bottom, left, right))