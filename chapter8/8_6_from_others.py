import numpy as np
import pandas as pd


def format_matrix(n, string):
    matrix = np.zeros((n, n), dtype=int)
    rows = string.split("\n")
    for i, elements in enumerate(rows):
        for k, element in enumerate(elements.split()):
            matrix[i][k] = int(element)
    return matrix


def closest_clusters(d):
    min_dist = float("inf")
    index = ()
    for i in d.keys():
        for j in d.keys():
            if i != j:
                if d[i][j] < min_dist:
                    min_dist = d[i][j]
                    index = (i, j)
    return index


def upgma(d, n):
    inner = n
    clusters = {i: 1 for i in range(n)}
    age = {i: 0 for i in range(n)}
    adj_list = {i: [] for i in range(n)}
    weights = {}
    d = pd.DataFrame(d)
    d.columns = list(range(n))
    d.index = list(range(n))
    # print(d)
    # print(clusters, age, adj_list)
    while len(clusters) > 1:
        # print("NEW")
        # print(d)
        i, j = closest_clusters(d)
        c_i = clusters[i]
        c_j = clusters[j]
        elements_count = c_i + c_j
        # print(i, j, c_i, c_j, elements_count, d[i][j])
        adj_list[inner] = [i, j]
        adj_list[i].append(inner)
        adj_list[j].append(inner)

        weights[(inner, i)] = 0
        weights[(inner, j)] = 0
        weights[(i, inner)] = 0
        weights[(j, inner)] = 0

        # print(adj_list, weights)
        age[inner] = d[i][j] / 2
        # print(age)
        # print(d)
        del clusters[i]
        del clusters[j]
        # print(clusters)
        new_addition = []
        for m in clusters.keys():
            # print(m)
            # print("C", d[i][c_m], c_i[1], d[j][c_m], c_j[1], elements_count)
            new_di = (d[i][m] * c_i + d[j][m] * c_j) / elements_count
            new_addition.append(new_di)

        # print(d, (i, j))
        # print(new_addition)
        # d = np.delete(d, (j, i), axis=0)
        # d = np.delete(d, (i, j), axis=1)

        d = d.drop([i, j])
        d = d.drop([i, j], axis=1)
        d[inner] = new_addition

        # print(d)
        # d = np.append(d, [new_addition], axis=0)
        # print(d)
        new_addition.append(0)
        d.loc[inner] = new_addition
        # d = np.append(d, np.reshape(new_addition, (np.shape(d)[0], 1)), axis=1)

        # print(d)
        clusters[inner] = elements_count

        inner += 1
    # print(age)
    for edge, weight in weights.items():
        if weight == 0:
            v = edge[0]
            w = edge[1]
            # print(edge, weight, age[v], age[w])
            weights[(v, w)] = abs(age[v] - age[w])
            weights[(w, v)] = abs(age[v] - age[w])

    return adj_list, weights


def solve_upgma(n, string):
    matrix = format_matrix(n, string)
    # print(matrix)
    weights = upgma(matrix, n)[1]
    for edge, w in weights.items():
        print(f"{edge[0]}->{edge[1]}:{w:.3f}")


if __name__ == "__main__":
#     string = """0	20	17	11
# 20	0	20	13
# 17	20	0	10
# 11	13	10	0"""
#     string = """0	3	4	3
#     3	0	4	5
#     4	4	0	2
#     3	5	2	0"""
#     solve_upgma(4, string)

    # with open("../data/dataset_369352_8.txt") as file:
    #     solve_upgma(30, file.read())

    string = """0 898 1181 643 974 1066 956 647 1184 748 1021 688 1121 744 758 1022 927 686 1130 638 880 653 691 864 677 
898 0 1172 820 732 1011 1093 1202 969 698 913 858 1243 756 1180 1003 1064 1062 887 656 811 814 798 954 1155 
1181 1172 0 904 941 1035 829 836 1182 1177 1105 1099 625 1144 996 734 1213 936 815 1069 731 1136 695 944 1024 
643 820 904 0 700 830 661 961 827 807 963 981 810 929 669 938 727 1233 1150 1033 787 867 920 890 1055 
974 732 941 700 0 884 989 1071 1053 891 1199 1042 665 1087 629 952 751 924 780 737 1190 710 718 997 725 
1066 1011 1035 830 884 0 742 883 673 932 817 1079 706 903 1023 894 786 1045 1057 772 984 876 768 1131 870 
956 1093 829 661 989 742 0 824 833 1111 788 863 791 1203 942 726 766 1122 687 697 918 979 808 738 1249 
647 1202 836 961 1071 883 824 0 851 716 704 1096 1072 922 1123 859 1201 908 1016 939 986 1240 953 916 703 
1184 969 1182 827 1053 673 833 851 0 1052 1222 1223 759 746 803 1109 1013 1166 1153 866 1050 834 1110 1246 1104 
748 698 1177 807 891 932 1111 716 1052 0 1113 770 1116 1029 736 1082 1134 774 972 1049 990 994 1037 892 690 
1021 913 1105 963 1199 817 788 704 1222 1113 0 885 1126 694 1244 671 1228 769 934 782 970 650 843 998 764 
688 858 1099 981 1042 1079 863 1096 1223 770 885 0 1026 1040 877 743 632 1114 752 1028 1047 648 654 713 1120 
1121 1243 625 810 665 706 791 1072 759 1116 1126 1026 0 1247 1167 950 1073 663 781 948 1102 957 1209 925 1135 
744 756 1144 929 1087 903 1203 922 746 1029 694 1040 1247 0 729 784 962 1101 1015 1207 871 701 840 753 987 
758 1180 996 669 629 1023 942 1123 803 736 1244 877 1167 729 0 1036 821 1245 719 977 1007 1032 714 1159 995 
1022 1003 734 938 952 894 726 859 1109 1082 671 743 950 784 1036 0 797 992 1119 906 637 988 850 762 865 
927 1064 1213 727 751 786 766 1201 1013 1134 1228 632 1073 962 821 797 0 1127 1124 801 1210 705 1147 715 882 
686 1062 936 1233 924 1045 1122 908 1166 774 769 1114 663 1101 1245 992 1127 0 1204 966 889 1115 1084 1171 1173 
1130 887 815 1150 780 1057 687 1016 1153 972 934 752 781 1015 719 1119 1124 1204 0 1200 1142 664 1068 818 805 
638 656 1069 1033 737 772 697 939 866 1049 782 1028 948 1207 977 906 801 966 1200 0 1208 1236 696 825 796 
880 811 731 787 1190 984 918 986 1050 990 970 1047 1102 871 1007 637 1210 889 1142 1208 0 750 1051 1189 844 
653 814 1136 867 710 876 979 1240 834 994 650 648 957 701 1032 988 705 1115 664 1236 750 0 999 878 1014 
691 798 695 920 718 768 808 953 1110 1037 843 654 1209 840 714 850 1147 1084 1068 696 1051 999 0 1081 1217 
864 954 944 890 997 1131 738 916 1246 892 998 713 925 753 1159 762 715 1171 818 825 1189 878 1081 0 741 
677 1155 1024 1055 725 870 1249 703 1104 690 764 1120 1135 987 995 865 882 1173 805 796 844 1014 1217 741 0 """
    solve_upgma(25, string)