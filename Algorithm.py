import re
import csv
import numpy as np
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

def steps(rows, step, evaluationFunction=entropy):
    
    if len(rows) == 0: return 0
    currentScore = evaluationFunction(rows)
    bestGain = 0.0
    bestAttribute = None
    bestSets = None
    columnCount = len(rows[0]) - 1  # last column is the result/target column
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

    return bestGain

#Fast Forward Starts here
def Fast_Forward(node_number, parameters, dictionary, evaluationFunction=entropy):
    rows = dictionary[node_number]
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
    dcY = {'TP' : '%d' % tp, 'FN' : '%d' % fn}
    if bestGain > 0:

        nn1 = 2*node_number
        nn2 = 2*node_number+1
        dictionary[nn1]=bestSets[0]
        dictionary[nn2]=bestSets[1]
        
        trueBranch = Fast_Forward(nn1, parameters, dictionary, evaluationFunction)
        falseBranch = Fast_Forward(nn2, parameters, dictionary, evaluationFunction)
        return DecisionTree(col=bestAttribute[0], value=bestAttribute[1],  trueBranch=trueBranch,
                            falseBranch=falseBranch, summary=dcY)
    else:
        return DecisionTree(results=uniqueCounts(rows), summary=dcY)
      

#Frequency, Entropy, Diversity Starts here
def diversity(recommendation, column_thresh, table_thresh):
    
    if (table_thresh == 0 or table_thresh >5) and (column_thresh == 0 or column_thresh >= 5):
        return recommendation[:5]
    column = pd.read_csv('0204Raw.csv').columns[1:]
    column_seen = {i: 0 for i in column}
    table = ['OPER', 'RCG', 'GRIT', 'RCR']
    table_seen = {i: 0 for i in table}
    
    recos = []
    for index in recommendation:
        variable = index[0]
        for t in table:
            if re.search(t, variable):
                if table_seen[t] > table_thresh:
                    break
                table_seen[t]+=1
                for c in column:
                    if re.search(c, variable):
                        if column_seen[c]>column_thresh:
                            break
                        column_seen[c]+=1
                        recos.append(index)
                        if len(recos)==5:
                            return recos
                                                
def Entropy_(rows, dictionary, columns, parameters, evaluationFunction=entropy):
    
    column_diversity, table_diversity, step = parameters
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
            if gain > bestGain and len(set1)>0 and len(set2)>0:
                recoms.append((columns[col], col, gain, value, set1, set2))
    if len(recoms) == 0:
        return []
    recoms = sorted(recoms, reverse=True, key = lambda x: x[2])
    recoms = diversity(recoms, column_diversity, table_diversity)
    
    recom_changed=[]
    if step == 2:
        for i in recoms:
            column, col, gain, value, set1, set2 = i
            s1 = steps(set1, step-1, evaluationFunction)
            s2 = steps(set2, step-1, evaluationFunction)
            recom_changed.append((gain+s1+s2, column, col, value, set1, set2))
        recom_changed = sorted(recom_changed, reverse=True, key = lambda x: x[0])
        recom_changed = [columns[i[1]] for i in recoms[:5]]
        return recom_changed
    
    recoms = [columns[i[1]] for i in recoms[:5]]
    return recoms
    
def Frequency(rows, columns, parameters, dictionary):
    
    column_diversity, table_diversity, step = parameters
    cols = len(rows[0])-1
    cons = [row[-1] for row in rows]
    recoms = []
    for col in range(cols):
        #if columns[col] == 'NOT_PEC_AND_QTZ_SOURCE_APPN_IDS_MI':
            #continue
        tp, fn = 0, 0
        row = [row[col] for row in rows]
        for i in range(len(cons)):
            if row[i] == 1 and cons[i] == 1:
                tp+=1
            elif row[i] == 1 and cons[i] == 0:
                fn+=1
        recoms.append((columns[col], col, tp, fn))
    
    recoms = sorted(recoms, reverse=True, key = lambda x : x[2]+x[3])
    recoms = diversity(recoms, column_diversity, table_diversity)
    recoms = [i[0] for i in recoms]
    return recoms

  
#SPLIT starts here
def SPLIT(node_number, variables, columns, dictionary, evaluationFunction=entropy):
    
    rows = dictionary[node_number]
    currentScore = evaluationFunction(rows)
    tp, fn = tpfn(rows)
    
    #When PLAY is pressed
    var = None
    if len(variables) == 2:
        if fn/(tp+fn)>0.8:
            index = columns.tolist().index(variables[1])
            (set1, set2) = divideSet(rows, index, value=1)
            var = variables[1]
        else:
            index = columns.tolist().index(variables[0])
            (set1, set2) = divideSet(rows, index, value=1)
            var = variables[0]
        nn1 , nn2 = 2*node_number, 2*node_number + 1
        dictionary[nn1], dictionary[nn2] = set1, set2 
        tp1, fn1 = tpfn(set1)
        tp2, fn2 = tpfn(set2)
        return var, currentScore, nn1, tp1, fn1, nn2, tp2, fn2
    
    #When a variable from the recommendation or searchable list is selected
    index = columns.tolist().index(variables[0])
    (set1, set2) = divideSet(rows, index, value=1)
    nn1 , nn2 = 2*node_number, 2*node_number + 1
    dictionary[nn1], dictionary[nn2] = set1, set2
    tp1, fn1 = tpfn(set1)
    tp2, fn2 = tpfn(set2)
    return variables[0], currentScore, nn1, tp1, fn1, nn2, tp2, fn2
  

#CLICK starts here
def CLICK(node_number, nodes, columns, parameters, dictionary):
    
    rows = dictionary[node_number]
    if len(nodes) != 0:
        for node in nodes:
            dictionary.pop(node)
    reco1 = Entropy_(rows, dictionary, columns, parameters, evaluationFunction=gini)
    reco2 = Frequency(rows, columns, parameters, dictionary)
    return reco1, reco2
  
#PROCESS Starts here
def PROCESS(antecedents, consequent, params, ref):
    
    rcgdata = 0
    gritdata = pd.read_csv('0204Bin.csv')
    rcrdata = pd.read_csv('binary.csv')
    operdata = 0
    
    #Defining Global Variables
    global dictionary
    global columns
    global parameters
    dictionary = {}
    
    data = {'OPER': operdata, 'RCG': rcgdata, 'GRIT': gritdata, 'RCR': rcrdata}
    bindata = data[ref]
    parameters = params
    columns = bindata.columns
    #AND operation on antecedents
    for i in antecedents: 
        bindata = bindata[bindata[i] == 1]
    
    #Setting consequent as the last column
    cons = bindata[consequent[0]].tolist()
    del bindata[consequent[0]]
    bindata[consequent[0]] = cons
    
    bindata = [[int(i) for i in bindata.iloc[j].tolist()] for j in range(len(bindata))]
    dictionary[1] = bindata
    return 1
