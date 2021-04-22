import csv
from collections import defaultdict
import pydotplus


class DecisionTree:
    """Binary tree implementation with true and false branch. """
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


def variance(rows):
    if len(rows) == 0: return 0
    data = [float(row[len(row) - 1]) for row in rows]
    mean = sum(data) / len(data)

    variance = sum([(d-mean)**2 for d in data]) / len(data)
    return variance

def frequency(rows, cols, columns):
    
    if len(rows) == 0:
        return None
    midbit=[]
    recos = []
    for row in rows:
        midbit.append(row[-1])
    
    for col in range(cols):
        tp=0
        fn=0
        if columns[col] == 'NOT_PEC_AND_QTZ_SOURCE_APPN_IDS_MI':
            continue
        for i in range(len(rows)):
            
            if rows[i][col] == 1 and midbit[i] == 1:
                tp+=1
            elif rows[i][col] == 1 and midbit[i] == 0:
                fn+=1
        recos.append((columns[col], tp, fn))
    
    recos = sorted(recos, reverse = True, key = lambda x : x[1])
    print(recos[:5])
    
    
'''def calculate_values(col, rows):
    
    columnValues = [row[col] for row in rows]
        #unique values
        lsUnique = list(set(columnValues))
        for value in lsUnique:
            (set1, set2) = divideSet(rows, col, value)

            # Gain -- Entropy or Gini
            #p = float(len(set1)) / len(rows)
            #gain = currentScore - p*evaluationFunction(set1) - (1-p)*evaluationFunction(set2)
            #if gain>bestGain and len(set1)>0 and len(set2)>0:
            bestGain = gain
            bestAttribute = (col, value)
            bestSets = (set1, set2)
            bestCol = col
    return bestAttribute, bestSets, bestCol'''
    

def growDecisionTreeFrom(rows, evaluationFunction=entropy):
    """Grows and then returns a binary decision tree.
    evaluationFunction: entropy or gini"""

    if len(rows) == 0: return DecisionTree()
    currentScore = evaluationFunction(rows)
    data = pd.read_csv('cart11.csv')
    cols = data.columns    
    
    freq_list = frequency(rows, len(rows[0])-1, cols)
    print(freq_list)
    show=[]
    recommendColumns = []
    seen = []
    for i in range(5):
        
        bestGain = 0.0
        bestAttribute = None
        bestSets = None
        bestCol = None
        columnCount = len(rows[0]) - 1  # last column is the result/target column
        for col in range(0, columnCount):
            
            if col in seen:
                continue
                
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
                    bestCol = col
        if bestAttribute == None: continue
        seen.append(bestAttribute[0])
        show.append((i, bestCol, cols[bestAttribute[0]]))
        recommendColumns.append((bestAttribute, bestGain, bestSets))
    print(show)
    if len(show) == 0:
        dcY = {'impurity' : '%.3f' % currentScore, 'samples' : '%d' % len(rows)}
        return DecisionTree(results=uniqueCounts(rows), summary=dcY)
    index = int(input("enter index of column selected:"))
    bestAttribute, bestGain, bestSets = recommendColumns[index]
    
    dcY = {'impurity' : '%.3f' % currentScore, 'samples' : '%d' % len(rows)}
    if bestGain > 0 and len(show)>0:
        trueBranch = growDecisionTreeFrom(bestSets[0], evaluationFunction)
        falseBranch = growDecisionTreeFrom(bestSets[1], evaluationFunction)
        return DecisionTree(col=bestAttribute[0], value=bestAttribute[1], trueBranch=trueBranch,
                            falseBranch=falseBranch, summary=dcY)
    else:
        return DecisionTree(results=uniqueCounts(rows), summary=dcY)



def plot(decisionTree):
    """Plots the obtained decision tree. """
    def toString(decisionTree, indent=''):
        
        if decisionTree.results != None:  # leaf node
            lsX = [(x, y) for x, y in decisionTree.results.items()]
            lsX.sort()
            szY = ', '.join(['%s: %s' % (x, y) for x, y in lsX])
            return szY
        
        else:
            szCol = 'Column %s' % decisionTree.col
            if szCol in dcHeadings:
                szCol = dcHeadings[szCol]
            if isinstance(decisionTree.value, int) or isinstance(decisionTree.value, float):
                decision = '%s >= %s?' % (szCol, decisionTree.value)
            else:
                decision = '%s == %s?' % (szCol, decisionTree.value)
            trueBranch = indent + 'yes -> ' + toString(decisionTree.trueBranch, indent + '\t\t')
            falseBranch = indent + 'no  -> ' + toString(decisionTree.falseBranch, indent + '\t\t')
            return (decision + '\n' + trueBranch + '\n' + falseBranch)

    print(toString(decisionTree))


def dotgraph(decisionTree):
    
    global dcHeadings
    dcNodes = defaultdict(list)
    """Plots the obtained decision tree. """
    
    def toString(iSplit, decisionTree, bBranch, szParent = "null", indent=''):
        if decisionTree.results != None:  # leaf node
            lsX = [(x, y) for x, y in decisionTree.results.items()]
            lsX.sort()
            lsX = ['FN: %s' % (y) if x == 0 else 'TP: %s' %(y) for x, y in lsX]
            szY = ', '.join(['%s' % (x) for x in lsX])
            dcY = {"name": szY, "parent" : szParent}
            dcSummary = decisionTree.summary
            dcNodes[iSplit].append(['leaf', dcY['name'], szParent, bBranch, dcSummary['impurity'],
                                    dcSummary['samples']])
            return dcY
        else:
            szCol = 'Column %s' % decisionTree.col
            if szCol in dcHeadings:
                    szCol = dcHeadings[szCol]
            if isinstance(decisionTree.value, int) or isinstance(decisionTree.value, float):
                    decision = '%s >= %s' % (szCol, decisionTree.value)
            else:
                    decision = '%s == %s' % (szCol, decisionTree.value)
            trueBranch = toString(iSplit+1, decisionTree.trueBranch, True, decision, indent + '\t\t')
            falseBranch = toString(iSplit+1, decisionTree.falseBranch, False, decision, indent + '\t\t')
            dcSummary = decisionTree.summary
            dcNodes[iSplit].append([iSplit+1, decision, szParent, bBranch, dcSummary['impurity'],
                                    dcSummary['samples']])
            return

    toString(0, decisionTree, None)
    lsDot = ['digraph Tree {',
                'node [shape=box, style="filled, rounded", color="black", fontname=helvetica] ;',
                'edge [fontname=helvetica] ;'
    ]
    i_node = 0
    dcParent = {}
    for nSplit in range(len(dcNodes)):
        lsY = dcNodes[nSplit]
        for lsX in lsY:
            iSplit, decision, szParent, bBranch, szImpurity, szSamples =lsX
            if type(iSplit) == int:
                szSplit = '%d-%s' % (iSplit, decision)
                dcParent[szSplit] = i_node
                lsDot.append('%d [label=<%s<br/>impurity %s<br/>samples %s>, fillcolor="#e5813900"] ;' % (i_node,
                                        decision.replace('>=', '&ge;').replace('?', ''),
                                        szImpurity,
                                        szSamples))
            else:
                lsDot.append('%d [label=<impurity %s<br/>samples %s<br/>class %s>, fillcolor="#e5813900"] ;' % (i_node,
                                        szImpurity,
                                        szSamples,
                                        decision))
                
            if szParent != 'null':
                if bBranch:
                    szAngle = '45'
                    szHeadLabel = 'True'
                else:
                    szAngle = '-45'
                    szHeadLabel = 'False'
                szSplit = '%d-%s' % (nSplit, szParent)
                p_node = dcParent[szSplit]
                if nSplit == 1:
                    lsDot.append('%d -> %d [labeldistance=2.5, labelangle=%s, headlabel="%s"] ;' % (p_node,
                                                        i_node, szAngle, szHeadLabel))
                else:
                    lsDot.append('%d -> %d ;' % (p_node, i_node))
            i_node += 1
    #lsDot.append('}')
    #dot_data = '\n'.join(lsDot)
    #return dot_data
    return lsDot


def loadCSV(file):
    """Loads a CSV file and converts all floats and ints into basic datatypes."""
    def convertTypes(s):
        s = s.strip()
        try:
            return float(s) if '.' in s else int(s)
        except ValueError:
            return s

    reader = csv.reader(open(file, 'rt'))
    dcHeader = {}
    if bHeader:
        lsHeader = next(reader)
        for i, szY in enumerate(lsHeader):
                szCol = 'Column %d' % i
                dcHeader[szCol] = str(szY)
    return dcHeader, [[convertTypes(item) for item in row] for row in reader]

import pandas as pd

if __name__ == '__main__':


    bHeader = True
    dcHeadings, trainingData = loadCSV('cart11.csv') # demo data from matlab

    print(len(trainingData))
    decisionTree = growDecisionTreeFrom(trainingData, evaluationFunction=gini)
    #prune(decisionTree, 0.8, notify=True) # notify, when a branch is pruned (one time in this example)
    result = plot(decisionTree)
    #print(result)
    lsDot = dotgraph(decisionTree)
    initial_lsDots=lsDot
    print(initial_lsDots)
    lsDot.append('}')
    dot_data = '\n'.join(lsDot)
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_pdf("iris0.pdf")
    graph.write_png("iris0.png")
