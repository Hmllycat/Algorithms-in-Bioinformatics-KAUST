
from copy import deepcopy
from reprlib import recursive_repr
from functools import reduce
from operator import itemgetter


class Node():

    def __init__(self, label=None, score =0, daughter=None, son=None, tag = False, value = -1):
        self.__label     = label
        self.__score     = score
        self.__daughter  = daughter
        self.__son       = son
        self.__tag       = tag
        self.__scores    = {i: float('inf') for i in "ACTG"}
        self.__value     = value

    @recursive_repr()
    def __repr__(self):
        if self.isLeaf():
            return ""
        else:
            string = ""        
            if self.__daughter != None:
                daughter = self.daughter
                weightDau = hammingDistance(self.label, daughter.label)
                
                string += str(self.__label) + '->' + str(daughter.label) + ':' + str(weightDau) + '\n'
                string += str(daughter.label) + '->' + str(self.__label) + ':' + str(weightDau) + '\n'

                son = self.son
                weightSon = hammingDistance(self.label, son.label)
                string += str(self.__label) + '->' + str(son.label) + ':' + str(weightSon) + '\n'
                string += str(son.label) + '->' + str(self.__label) + ':' + str(weightSon) + '\n'

                string += str(daughter)
                string += str(son) 

            return string

    # def __repr__(self):
    #     if self.isLeaf():
    #         return str(self.__value) + ':' + str(self.__label) + '\n'
    #     if self != None:
    #         string = ""        
    #         if self.__daughter != None:
    #             string = str(self.__value) + ':' + str(self.__label) + '->'
    #             string += str(self.__daughter.__value) + ',' + str(self.__son.__value) + '\n'
    #             string += str(self.__daughter)
    #             string += str(self.__son)
    #         return string
    #     else:
    #         return ""

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, label):
        self.__label = label

   
    @property
    def daughter(self):
        return self.__daughter
    
    @daughter.setter
    def daughter(self, daughter):
        self.__daughter = daughter
    
    @property
    def son(self):
        return self.__son

    @son.setter
    def son(self, son):
        self.__son = son

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        self.__score = score

    @property
    def scores(self):
        return self.__scores

    @property
    def value(self):
        return self.__value
        
    @property
    def tag(self):
        return self.__tag

    @tag.setter
    def tag(self, tag):
        self.__tag = tag

    # @score.setter
    # def score(self, score):
    #     self.__score = score


    def totalScore(self):
        if self.isLeaf():
            return self.__score
        else:
            return self.__score #+ self.__daughter.totalScore() + self.__son.totalScore()
    
    def isLeaf(self):
        if self.__daughter == None and self.__son == None:
            return True
        else:
            return False

    def isRipe(self):
        if self.__daughter == None or self.__son == None:
            return False
        else:
            if self.__tag == False and self.__daughter.__tag == True and self.__son.__tag == True:
                return True
            else:
                return False

    def initialScores(self):
        if self.isLeaf():
            self.__scores = {i: float('inf') for i in "ACTG"}
            self.__scores[self.__label] = 0
            self.__tag = True
        else:
            return "Error in Node:initialScores: this function can be applied only to leaves"

    # O(2n) n is the number of leaves
    def processLeaves(self):
        if self.isLeaf():
            self.initialScores()
        else:
            if self.__daughter != None:
                self.__daughter.processLeaves()
            if self.__son != None:
                self.__son.processLeaves()

    def updateScores(self):
        scores = self.__scores
        for nucl in scores.keys():

            daughterPart = float('inf')
            daughterScores =  self.__daughter.__scores

            for dau_nucl in daughterScores.keys():
                alpha =  0 if nucl == dau_nucl else 1
                score = daughterScores[dau_nucl] + alpha
                daughterPart = min(daughterPart, score)

            sonPart = float('inf')
            sonScores =  self.__son.__scores

            for son_nucl in sonScores.keys():
                alpha =  0 if nucl == son_nucl else 1
                score = sonScores[son_nucl] + alpha
                sonPart = min(sonPart, score)

            scores[nucl] = daughterPart + sonPart
        
        self.__scores = scores

        # self.__label, self.__score = min(scores.items(), key=itemgetter(1))

        # print(self.__label)

        self.__tag = True
    
    def singleCharTree(self, idx):
        if self.isLeaf():
            self.__label = self.__label[idx]
            return self.__label
        else:
            if self.__daughter != None:
                dauStr = self.__daughter.singleCharTree(idx)
            else:
                dauStr = ''
            if self.__son != None:
                sonStr = self.__son.singleCharTree(idx)
            else:
                sonStr = ''
            return dauStr + sonStr

    # O(2n) n is the number of leaves
    def getRipeNode(self):
        if self.isLeaf():
            return None
        if self.__tag == 1:
            return None
        if self.isRipe():
            self.updateScores()
            return 0

        else:

            if self.__daughter != None:
                lookInDaughter =  self.__daughter.getRipeNode()

                if lookInDaughter != None:
                    return lookInDaughter
        
            if self.__son != None:
                lookInSon =  self.__son.getRipeNode()

                if lookInSon != None:
                    return lookInSon


def hammingDistance(string1, string2):
    if (len(string1) != len(string2)):
        return -1
    hamm = 0
    for i in range(len(string1)):
        if string1[i] != string2[i]:
            hamm += 1
    return hamm


def mergeTrees(trees):
    tree =  deepcopy(trees[0])


    tree.label = (reduce(lambda a, b: a+b, [t.label for t in trees] , '')) 
    tree.score = (reduce(lambda a, b: a+b, [t.score for t in trees] , 0)) 

    if tree.daughter != None:
        tree.daughter = mergeTrees([t.daughter for t in trees])

    if tree.son != None:
        tree.son = mergeTrees([t.son for t in trees])
    
    return tree

# O(n^2)
def smallParsimonySingle(tree):
    # O(2n) n is the number of leaves
    tree.processLeaves()

    # O(2n)
    ripe = tree.getRipeNode()
    
    # O(n) * O(2n)
    while ripe != None:
        ripe =  tree.getRipeNode()


    tree.label, tree.score = min(tree.scores.items(), key=itemgetter(1))

    # O(n)
    backtrackScores(tree)

    return tree

# O(n) n is the number of leaves
def backtrackScores(tree):

    if not tree.isLeaf():
        parentLabel =  tree.label

        if tree.daughter != None:
            dauScores =  tree.daughter.scores
            minScore = float('inf')
            for nucl, value in dauScores.items():
                alpha =  0 if nucl == parentLabel else 1
                score = value + alpha

                if score < minScore:
                    minScore = score
                    dauLabel = nucl

            tree.daughter.label = dauLabel
            tree.daughter.score = minScore
            backtrackScores(tree.daughter)


        if tree.son != None:
            sonScores =  tree.son.scores
            minScore = float('inf')
            for nucl, value in sonScores.items():
                alpha =  0 if nucl == parentLabel else 1
                score = value + alpha

                if score < minScore:
                    minScore = score
                    sonLabel = nucl

            tree.son.label = sonLabel
            tree.son.score = minScore
            backtrackScores(tree.son)


# O(m*n^2) where m is the length of the strings and n is the number of leaves
def smallParsimony(tree, m):
    # m is the length of the string
    trees =  []
    for i in range(m):
        tree_i = deepcopy(tree)
        column = tree_i.singleCharTree(i)
        trees.append((column, tree_i))

    computed = {}
    newTrees = []

    # This for is O(m) * O(n^2)
    for i in range(len(trees)):

        column, tree_i = trees[i]
        if column in computed:
            newTrees.append(computed[column])
        else:
            newTrees.append(smallParsimonySingle(tree_i))


    return mergeTrees(newTrees)



if __name__ == "__main__":
    
    file =  open('C:/Users/树下的猫/Downloads/dataset_369355_10 (2).txt', 'r')

    n = int(file.readline().rstrip('\n'))

    edges =  [tuple(line.rstrip('\n').split('->')) for line in file]

    parent = -1
    m = len(edges[0][1])
    nodes = {}
    for i in range(0,len(edges),2):
        if i < n:
            value, stringDau = edges[i]
            _, stringSon = edges[i+1]

            value = int(value)
            
            nodeDau =  Node(label=stringDau, value = i)
            nodeSon =  Node(label=stringSon, value = i+1)

            nodes[value] = Node(value = value, daughter=nodeDau, son=nodeSon)
            
        else:
            parent, dau = edges[i]
            parent, son = edges[i+1]

            dau = int(dau)
            son = int(son)
            parent = int(parent)

            nodes[parent] =  Node(value = parent, daughter=nodes[dau], son=nodes[son])

            del nodes[dau]
            del nodes[son]


    tree =  nodes[parent]

    tree = smallParsimony(tree,m)
    score =  tree.totalScore()

    print(score)
    print(tree)