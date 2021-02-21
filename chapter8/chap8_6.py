"""
@BY: Yang LIU
@DATE: 03-11-2020
"""

import numpy as np

# update the cluster_dic
def remove_two_cluster_add_newone(D, min_value, cluster_dic, i, j, new_node):

    new_cluster = [(cluster_dic[i][k] + cluster_dic[j][k])/2 for k in range(len(cluster_dic[i]))]
    cluster_i = cluster_dic[i].copy()
    cluster_j = cluster_dic[j].copy()
    del cluster_dic[i], cluster_dic[j]
    for key in cluster_dic.keys():
        # print(cluster_dic)
        if i < len(D):          
            if j < len(D):
                cluster_dic[key].pop(j)
                cluster_dic[key].append(new_cluster[key])
            else:
                intersect = set(cluster_j) & set(cluster_dic[key])
                for value in intersect:
                    if value != 0:
                        cluster_dic[key].remove(value)
                if len(new_cluster) > key+1:
                    cluster_dic[key].append(new_cluster[key])
                else:
                    cluster_dic[key].append(new_cluster[key-1])
            cluster_dic[key].pop(i)
            # print()
            # print(cluster_dic)
        else:
            intersect = set(cluster_j+cluster_i) & set(cluster_dic[key])
            for value in intersect:
                if value != 0:
                    cluster_dic[key].remove(value)
                    
    new_cluster.remove(min_value/2)
    new_cluster.remove(min_value/2)
    new_cluster.append(0)
    cluster_dic[new_node] = new_cluster

    return cluster_dic


def UPGMA(D, n):

    cluster_dic = {}
    age = {}
    existed_node = [i for i in range(n)]
    clusters = [D[i, ] for i in range(n)]
    for idx, cluster in enumerate(clusters):
        cluster_dic[idx] = list(cluster)
    for i in range(len(D)):
        age[i] = 0
    T = {}
    # print(cluster_dic)
    while len(cluster_dic) > 1:
        min_value = float("inf")
        min_position = (0, 0)
        for key in cluster_dic.keys():
            row_value_exceptzero = cluster_dic[key].copy()
            row_value_exceptzero.remove(0)
            # print(row_value_exceptzero, cluster_dic)
            if min(row_value_exceptzero) <= min_value:
                min_value = min(row_value_exceptzero)
                another_key = [i for i in cluster_dic.keys() if i != key and min_value in cluster_dic[i]][0]
                min_position = (key, another_key)
                # print(min_position)
        i = min(min_position)
        j = max(min_position)
        new_node = max(existed_node) + 1
        existed_node.append(new_node)
        # print(min_value)
        age[new_node] = min_value/2
        # print(cluster_dic)
        # print()
        T[new_node] = [i, j]
        # print(cluster_dic)
        cluster_dic = remove_two_cluster_add_newone(D, min_value, cluster_dic, i, j, new_node)
    for key in T.keys():
        for value in T[key]:
            score = abs(age[key] - age[value])   
            print ('%i->%i:%.3f'%(key, value, score))
            print ('%i->%i:%.3f'%(value, key, score))
    return


if __name__ == "__main__":   

    n = 4
    D = np.array([[0, 20, 17, 11], [ 20, 0, 20, 13], [ 17, 20, 0, 10], [ 11, 13, 10, 0]])
    print(UPGMA(D, n))