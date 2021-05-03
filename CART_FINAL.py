import csv
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

def diversity(recoms, raw, thresh):

    if thresh > 4:
        return recoms[:5]
  
    r = []
    for i in recoms:
        col = i[1]
        for column in raw:
            if re.search(column, col):
                
                if raw[column] > thresh:
                    break
                elif raw[column] <= thresh:
                    r.append(i)
                    raw[column]+=1
                    break
                    
        if len(r) == 5:
            break
    return r

def frequency(rows, columns, raw, thresh):
    
    cols = len(rows[0])-1
    cons = [row[-1] for row in rows]
    recoms = []
    for col in range(cols):
        if columns[col] == 'NOT_PEC_AND_QTZ_SOURCE_APPN_IDS_MI':
            continue
        tp, fn = 0, 0
        row = [row[col] for row in rows]
        for i in range(len(cons)):
            if row[i] == 1 and cons[i] == 1:
                tp+=1
            elif row[i] == 1 and cons[i] == 0:
                fn+=1
        recoms.append((col, columns[col], tp, fn))
    
    recoms = sorted(recoms, reverse=True, key = lambda x : x[2])
    recoms = diversity(recoms, raw, thresh)
    return recoms

def searchable_list(rows, columns):
    
    l = []
    for i in row[0][:-1]:
        l.append((i, columns[i]))
    print(l)
    index = input("Enter index of the variable:")
    return index
  
def steps(rows, step, evaluationFunction=entropy):
    
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
    
    if step == 0:
        return bestGain
    
    if bestGain > 0:

        trueBranch = steps(bestSets[0], step-1, evaluationFunction)
        falseBranch = steps(bestSets[1], step-1, evaluationFunction)
        return trueBranch + falseBranch
    else:
        return 0 
      

def Entropy_R(rows, step, thresh, columns, raw, evaluationFunction=entropy):
    
    recoms1 = []
    
    #Varibles used in calculating IG
    currentScore = evaluationFunction(rows)
    bestGain = 0.0
    bestAttribute = None
    bestSets = None
    bestCol = None
    columnCount = len(rows[0]) - 1
    
    for col in range(columnCount):
        
        columnValues = [row[col] for row in rows]
        #unique values
        lsUnique = list(set(columnValues))
        for value in lsUnique:
            (set1, set2) = divideSet(rows, col, value)
            #Gain -- Entropy or Gini
            p = float(len(set1)) / len(rows)
            gain = currentScore - p*evaluationFunction(set1) - (1-p)*evaluationFunction(set2)
            if len(set1)>0 and len(set2)>0:
                
                recoms1.append((col, columns[col], gain, value, set1, set2))
            
    recoms1 = sorted(recoms1, reverse=True, key = lambda x: x[2])
    recoms1 = diversity(recoms1, raw, thresh)
    recoms = []
    if step == 2:
        
        for i in recoms1[:5]:
            gain, col, column, value, set1, set2 = i
            s1 = steps(set1, step-1, evaluationFunction)
            s2 = steps(set2, step-1, evaluationFunction)

            recoms.append((gain+s1+s2, column, col, value, set1, set2))
        recoms = sorted(recoms, reverse=True, key = lambda x: x[0])
        return recoms

    return recoms1[:5]
  
  
  
def evaluate(rows, params, raw, evaluationFunction=entropy):
    
    if len(rows) == 0: return DecisionTree()
    thresh, steps, cd, td = params
    data = pd.read_csv('cart11.csv')
    columns = data.columns
    
    if input("Fast Forward: Yes/No").upper() == 'YES':   
        return fastforward(rows, params, raw, columns, evaluationFunction)

    cols = len(rows[0])-1
    recomsF = frequency(rows, columns, raw, thresh)
    recomsE = Entropy_R(rows, steps, thresh, columns, raw, evaluationFunction)
    recomsED = []
    for i in recomsE:
        recomsED.append((i[1], i[2]))
    #recomsS = searchable_list(rows, columns)
    print(recomsF, '\n', recomsED)
    index = int(input('1. Frequency \n 2. Entropy \n 3. Search \n'))
    if index == 1:
        tp, fn = tpfn(rows)
        dcY = {'TP' : '%d' % tp, 'FN' : '%d' % fn}
        col, column, tp, fn = recomsF[0]

        set1, set2 = divideSet(rows, cols, 1)
        print(column, len(set1), len(set2))
        trueBranch = evaluate(set1, params, raw, evaluationFunction)
        falseBranch = evaluate(set2, params, raw, evaluationFunction)
        if len(set1)>0 and len(set2)>0:
            return DecisionTree(col=col, value=1, trueBranch=trueBranch,
                            falseBranch=falseBranch, summary=dcY)
        else:
            return DecisionTree(results=uniqueCounts(rows), summary=dcY)
    if index == 2:
        tp, fn = tpfn(rows)
        dcY = {'TP' : '%d' % tp, 'FN' : '%d' % fn}
        if len(recomsE) == 0:
            return DecisionTree(results=uniqueCounts(rows), summary=dcY)
        gain, col, column, value, set1, set2 = recomsE[0]
        
        if gain > 0:
            trueBranch = evaluate(set1, params, raw, evaluationFunction)
            falseBranch = evaluate(set2, params, raw, evaluationFunction)
            return DecisionTree(col=col, value=value, trueBranch=trueBranch,
                            falseBranch=falseBranch, summary=dcY)
        else:
            return DecisionTree(results=uniqueCounts(rows), summary=dcY)
          
          
          
def fastforward(rows, params, raw, columns, evaluationFunction=entropy):
    
    if len(rows) == 0: return DecisionTree()
    
    thresh, step, cd, td = params
    #data = pd.read_csv('cart11.csv')
    #columns = data.columns
    cols = len(rows[0])-1
    recomsE = Entropy_R(rows, step, thresh, columns, raw, evaluationFunction)
    
    tp, fn = tpfn(rows)
    dcY = {'TP' : '%d' % tp, 'FN' : '%d' % fn}
        
    if len(recomsE) == 0:
        return DecisionTree(results=uniqueCounts(rows), summary=dcY)
    gainE, colE, columnE, valueE, set1E, set2E = recomsE[0]
    #print(gainE)
    if gainE > 0 and len(set1E)>0 and len(set2E)>0:
        trueBranch = fastforward(set1E, params, raw, columns, evaluationFunction)
        falseBranch = fastforward(set2E, params, raw, columns, evaluationFunction)
        return DecisionTree(col=colE, value=valueE, trueBranch=trueBranch,
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
            print(lsX)
            lsX = ['FN: %s' % (y) if x == 0 else 'TP: %s' %(y) for x, y in lsX]
            szY = ', '.join(['%s' % (x) for x in lsX])
            print(szY)
            dcY = {"name": szY, "parent" : szParent}
            dcSummary = decisionTree.summary
            dcNodes[iSplit].append(['leaf', dcY['name'], szParent, bBranch, dcSummary['TP'],
                                    dcSummary['FN']])
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
            dcNodes[iSplit].append([iSplit+1, decision, szParent, bBranch, dcSummary['TP'],
                                    dcSummary['FN']])
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
                lsDot.append('%d [label=<%s<br/>TP %s<br/>FN %s>, fillcolor="#e5813900"] ;' % (i_node,
                                        decision.replace('>=', '&ge;').replace('?', ''),
                                        szImpurity,
                                        szSamples))
            else:
                lsDot.append('%d [label=<Impurity %s<br/>Samples %s<br/>%s>, fillcolor="#e5813900"] ;' % (i_node,
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

  import pandas as pd

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

if __name__ == '__main__':

    bHeader = True
    dcHeadings, trainingData = loadCSV('cart11.csv') # demo data from matlab
    d = pd.read_csv('0204Raw.csv')
    r = d.columns
    raw = {}
    for i in r[1:]:
        raw[i]=0
    data = pd.read_csv('cart11.csv')
    columns = data.columns
    print(len(trainingData))
    params = [int(i) for i in input('Thresh, steps, column diversity, table diversity:').split()]
    decisionTree = evaluate(trainingData, params, raw, evaluationFunction=gini)
    #prune(decisionTree, 0.8, notify=True) #notify, when a branch is pruned (one time in this example)
    result = plot(decisionTree)
    lsDot = dotgraph(decisionTree)
    initial_lsDots=lsDot
    print(initial_lsDots)
    lsDot.append('}')
    dot_data = '\n'.join(lsDot)
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_pdf("iris8.pdf")
    graph.write_png("iris8.png")
