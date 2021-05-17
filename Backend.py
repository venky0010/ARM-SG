import csv
import pandas as pd
from collections import defaultdict
import pydotplus


class DecisionTree:
    """ Binary tree implementation with true and false branch. """
    def __init__(self, col=-1, value=None, trueBranch=None, falseBranch=None, results=None, summary=None):
        self.col = col
        self.value = value
        self.trueBranch = trueBranch
        self.falseBranch = falseBranch
        self.results = results # None for nodes, not None for leaves
        self.summary = summary


def divideSet(rows, column, value):
    splittingFunction = None
    if isinstance(value, int) or isinstance(value, float): # for int and float values
        splittingFunction = lambda row : row[column] >= value
    else: # for strings
        splittingFunction = lambda row : row[column] == value
    list1 = [row for row in rows if splittingFunction(row)]
    list2 = [row for row in rows if not splittingFunction(row)]
    return (list1, list2)


def uniqueCounts(rows):
    results = {}
    for row in rows:
        #response variable is in the last column
        r = row[-1]
        if r not in results: results[r] = 0
        results[r] += 1
    return results


def entropy(rows):
    from math import log
    log2 = lambda x: log(x)/log(2)
    results = uniqueCounts(rows)

    entr = 0.0
    for r in results:
        p = float(results[r])/len(rows)
        entr -= p*log2(p)
    return entr


def gini(rows):
    total = len(rows)
    counts = uniqueCounts(rows)
    imp = 0.0

    for k1 in counts:
        p1 = float(counts[k1])/total
        for k2 in counts:
            if k1 == k2: continue
            p2 = float(counts[k2])/total
            imp += p1*p2
    return imp

def tpfn(rows):
    
    cons = [row[-1] for row in rows]
    tp = sum(cons)
    fn = len(rows)-tp
    return tp, fn
  
  
def Fast_Forward(rows, dictionary, nodes, node_number, evaluationFunction=entropy):
    print(node_number)
    if len(rows) == 0: return DecisionTree()
    currentScore = evaluationFunction(rows)
    bestGain = 0.0
    bestAttribute = None
    bestSets = None
    columnCount = len(rows[0]) - 1  # last column is the result/target column
    recoms = []
    
    for col in range(0, columnCount):
        columnValues = [row[col] for row in rows]

        #unique values
        lsUnique = list(set(columnValues))

        for value in lsUnique:
            (set1, set2) = divideSet(rows, col, value)

            # Gain -- Entropy or Gini
            p = float(len(set1)) / len(rows)
            gain = currentScore - p*evaluationFunction(set1) - (1-p)*evaluationFunction(set2)
            if gain>bestGain and len(set1)>0 and len(set2)>0:
                bestGain = gain
                bestAttribute = (col, value)
                bestSets = (set1, set2)
          
                
    tp, fn = tpfn(rows)
    print(tp, fn)
    dcY = {'TP' : '%d' % tp, 'FN' : '%d' % node_number}
    if bestGain > 0:
        
        nn1 = nodes[node_number][0]
        nn2 = nodes[node_number][1]
        i = max(nn1, nn2)
        nodes[nn1]=[i+1, i+2]
        nodes[nn2] = [i+3, i+4]
        dictionary[nn1]=bestSets[0]
        dictionary[nn2]=bestSets[1]
        
        trueBranch = Fast_Forward(bestSets[0], dictionary, nodes, nn1, evaluationFunction)
        falseBranch = Fast_Forward(bestSets[1], dictionary, nodes, nn2, evaluationFunction)
        return DecisionTree(col=bestAttribute[0], value=bestAttribute[1],  trueBranch=trueBranch,
                            falseBranch=falseBranch, summary=dcY)
    else:
        return DecisionTree(results=uniqueCounts(rows), summary=dcY)
      

  
def click(node_number, parameters, dictionary):
    
    rows = dictionary[node_number]
    #Entropy, Frequency = Show_Recommendations(rows, parameters)
    
    choice = input("Enter the choice")
    
    if choice.upper() == 'PLAY':
        variable, row1, row2 = F_AND_E(Entropy[0], Frequency[0])
        return variable, row1, row2
        
    if choice.upper() == 'FAST FORWARD':
        nodes = {node_number : [node_number+1,node_number+2]}
        tree = Fast_Forward(rows, dictionary, nodes, node_number, evaluationFunction=gini)
        return tree
    
    if choice.upper() == 'SELECT':
        node1, node2 = Entropy[0], Frequency[0]
        matrix[node1], matrix[node2] = row1, row2
        
   
data = pd.read_csv('cart11.csv')
columns = data.columns
matrix = [[int(i) for i in data.iloc[j].tolist()] for j in range(len(data))]
dictionary = {0: matrix}
params = {'columns': data.columns}
decisionTree = click(0, params, dictionary)
 
