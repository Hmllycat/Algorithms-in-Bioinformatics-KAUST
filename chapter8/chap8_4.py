"""
@BY: Yang LIU
@DATE: 03-11-2020
"""

import numpy as np
import sys
sys.setrecursionlimit(15000)


class Tree(object):

## public code for the data structure Tree

    def __init__(self,N=-1,bidirectional=True):
        self.nodes=list(range(N))
        self.edges={}
        self.bidirectional=bidirectional
        self.N = N
        
    def link(self,start,end,weight=1): 
        self.half_link(start,end,weight)
        if self.bidirectional:
            self.half_link(end,start,weight)
        
    def unlink(self,i,k):
        try:
            self.half_unlink(i,k)
            if self.bidirectional:
                self.half_unlink(k,i)
        except KeyError:
            print ('Could not unlink {0} from {1}'.format(i,k))
            self.print()        
        
    def half_link(self,a,b,weight=1):
        if not a in self.nodes:
            self.nodes.append(a)        
        if a in self.edges:               
            self.edges[a]=[(b0,w0) for (b0,w0) in self.edges[a] if b0 != b] + [(b,weight)]
        else:
            self.edges[a]=[(b,weight)]

    def half_unlink(self,a,b):
        links=[(e,w) for (e,w) in self.edges[a] if e != b]
        if len(links)<len(self.edges[a]):
            self.edges[a]=links
        else:
            print ('Could not unlink {0} from {1}'.format(a,b))
            self.print()

    def are_linked(self,a,b):
        return len([e for (e,w) in self.edges[a] if e == b])>0
        
    def AdjList(self,includeNodes=False):
        print('AdjList')
        self.nodes.sort()
        if includeNodes:
            print (self.nodes)
        for node in self.nodes:
            if node in self.edges:
                for edge in self.edges[node]:
                    end,weight=edge
                    print ('%i->%i:%.0f'%(node,end,weight))


# Input:  An integer n followed by the adjacency list of a weighted tree with n leaves.
# Output: An n x n matrix (di,j), where di,j is the length of the path between leaves i and j.
def limb_length(n, j, D):

    limblength = float("inf")
    for i in range(n):
        for k in range(n):
            if i != j and k != j:
                length = (D[j, k] + D[i, j] - D[i, k])/2
                if length < limblength:
                    limblength = length
    return limblength


def breadth_first(t, x, i, k):
    # find the two nodes in the path from i to k with cost x to break
    # ex: 0->1:13, make it 0->x:11 and 1->x:2, find 0, 1, 11, and 2

    queue = [[i]]
    visited = set([i])
    actual_path = []
    while len(queue) > 0:
        path = queue.pop()
        node = path[-1]
        visited.add(node)
        if node == k:
            actual_path = path
            break
        for next_node in t.edges[node]:
            if next_node[0] not in visited:
                queue.append(path + [next_node[0]])

    cost = 0
    for k in range(len(actual_path) - 1):
        i, j = actual_path[k], actual_path[k + 1]
        w = [x for x in t.edges[i] if x[0] == j][0][1]
        if cost + w > x:
            return (i, j, x - cost, cost + w - x)
        cost += w


def two_leaves_condition(d, n):
    for i in range(n):
        for k in range(i + 1, n):
            if d[i, k] == d[i, -1] + d[-1, k]:
                return i, k


def additive_phylogeny(inner_start, d):
    n = np.shape(d)[0]
    if n == 2:
        tree = Tree()
        tree.link(0, 1, d[0, 1])
        return tree, inner_start
    limb = limb_length(n, n - 1, d)
    for j in range(n-1):
        d[j, -1] -= limb
        d[-1, j] = d[j, -1]
    i, k = two_leaves_condition(d, n)
    x = d[i, - 1]
    d = d[:-1, :-1]

    t, inner_start = additive_phylogeny(inner_start, d)
    i_near, k_near, i_x, n_x = breadth_first(t, x, i, k)
    v = i_near

    if i_x != 0:
        v = inner_start
        inner_start += 1
        t.link(k_near, v, n_x)
        t.link(i_near, v, i_x)
        t.unlink(i_near, k_near)

    t.link(v, n - 1, limb)
    return t, inner_start


if __name__ == "__main__":   

    inner = 4
    D = np.array([  [0,13,21,22],
                    [13,0,12,13],
                    [21,12,0,13],
                    [22,13,13,0]])
    print(additive_phylogeny(inner, D)[0].AdjList())