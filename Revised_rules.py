import re
import numpy as np
import pandas as pd

data = pd.read_csv('GRIT26.csv')
old = pd.read_csv('binarized_file.csv')
columns = ['SOURCE_APPLICATION_ID=QTZ_MI', 'SOURCE_APPLICATION_ID=PEC/QTZ_MI', 'SOURCE_APPLICATION_ID=PEC_MI',
          'SOURCE_APPLICATION_ID!=QTZ_MI', 'SOURCE_APPLICATION_ID!=PEC/QTZ_MI', 'SOURCE_APPLICATION_ID!=PEC_MI']

data['SOURCE_APPLICATION_ID!=QTZ_MI'] = [1-i for i in data['SOURCE_APPLICATION_ID=QTZ_MI']]
data['SOURCE_APPLICATION_ID!=PEC/QTZ_MI'] = [1-i for i in data['SOURCE_APPLICATION_ID=PEC/QTZ_MI']]
data['SOURCE_APPLICATION_ID!=PEC_MI'] = [1-i for i in data['SOURCE_APPLICATION_ID=PEC_MI']]

rcg_cols = []

for i in data.columns:
    if re.search("_RCG$", i):
        rcg_cols.append(i)

grit_cols = []

for i in data.columns:
    if re.search('GRIT_E2k$', i):
        grit_cols.append(i)

        
def sensitivity(antecedent, consequent):
    
    tp=0
    fn=0
    fp=0
    tn=0
    
    for i in range(len(antecedent)):
        if   antecedent[i]==1 and consequent[i]==1:         #Ante present, Cons present
            tp+=1
        elif antecedent[i]==1 and consequent[i]==0:         #Ante present, Cons not present
            fn+=1
        elif antecedent[i]==0 and consequent[i]==1:         #Ante not present, cons present
            fp+=1
        else:                                               #Both ante and cons not present
            tn+=1
            
    if tp+fn == 0:                                          #To ignore not defined values
        return 0, 0, 0, 0, 0
    
    s = tp/(tp+fn)
    
    return s, tp, fn, fp, tn


df1 = []
cons = [1-i for i in data['SECONDBIT=1_APP_ORGIN_RCG'].tolist()]
for column1 in columns:
    
    ant1 = data[column1].tolist()
    s, tp, fn, fp, tn = sensitivity(ant1, cons)
    if s>=0:
        
        df1.append((column1, s, tp, fn, fp, tn))
        
        
df2 = []
for column1 in columns:
    for column2 in rcg_cols:
        if column2 == 'SECONDBIT=1_APP_ORGIN_RCG':
            continue
            
        ante1, ante2 = data[column1].tolist(), data[column2].tolist()
        ante = [ante1[i]*ante2[i] for i in range(len(ante1))]
        s, tp, fn, fp, tn = sensitivity(ante, cons)
        if s>0.5 and tp>30:
            df2.append((column1, column2, s, tp, fn, fp, tn))
            cache2.append((column1, column2, ante))
            col2.append(column1)
            col2.append(column2)



df3 = []
col3 = []
cache3 = []

for column1 in columns:
    for column2 in rcg_cols:
        for column3 in grit_cols:
            
            ante1, ante2, ante3 = data[column1].tolist(), data[column2].tolist(), data[column3].tolist()
            ante = [ante1[i]*ante2[i] for i in range(len(ante1))]
            ante = [ante[i]*ante3[i] for i in range(len(ante))]
            
            s, tp, fn, fp, tn = sensitivity(ante, cons)
            
            if s > 0.75 and tp > 30:
                
                df3.append((column1, column2, column3, s, tp, fn, fp, tn))
                col3.append(column3)
                cache3.append((column1, column2, column3, ante))
                
col3 = list(set(col3))
cache4 = []
col4 = []
df4 = []
for val in cache3:
    for column4 in col3:
        cols = [val[0], val[1], val[2]]
        
        if column4 in cols:
            continue
        
        ante3 = data[column4].tolist()
        ante = [val[3][i]*ante3[i] for i in range(len(ante3))]
        s, tp, fn, fp, tn = sensitivity(ante, cons)
        
        if s > 0.75 and tp>30:
            df4.append((val[0], val[1], val[2], column4, s, tp, fn, fp, tn))
            col4.append(column4)
            cache4.append((val[0], val[1], val[2], column4, ante))
            
            
df5 = []
cache5 = []
col4 = list(set(col4))

for val in cache4:
    for col5 in col4:
        
        cols = [val[0], val[1], val[2], val[3]]
        if col5 in cols:
            continue
        
        ante5 = data[col5].tolist()
        ante = [val[4][i]*ante5[i] for i in range(len(ante5))]
        
        s, tp, fn, fp, tn = sensitivity(ante, cons)
        
        if s>0.8 and tp>30:
            df5.append((val[0], val[1], val[2], val[3], col5, s, tp, fn, fp, tn))

            
df2 = sorted(df2, reverse = True, key = lambda x: x[3])            
df3 = sorted(df3, reverse = True, key = lambda x: x[4])
df4 = sorted(df4, reverse = True, key = lambda x: x[5])
df5 = sorted(df5, reverse=True, key = lambda x: x[6])

df1 = pd.DataFrame(df1, columns=['Antecedent1', 'Sensitivity', 'TP', 'FN', 'FP', 'TN'])
df2 = pd.DataFrame(df2, columns=['Antecedent1', 'Antecedent2', 'Sensitivity', 'TP', 'FN', 'FP', 'TN'])
df3 = pd.DataFrame(df3, columns=['Antecedent1', 'Antecedent2', 'Antecedent3', 'Sensitivity', 'TP', 'FN', 'FP', 'TN'])
df4 = pd.DataFrame(df4, columns=['Antecedent1', 'Antecedent2', 'Antecedent3', 'Antecedent4', 'Sensitivity', 'TP', 'FN', 'FP', 'TN'])
df5 = pd.DataFrame(df5, columns=['Antecedent1', 'Antecedent2', 'Antecedent3', 'Antecedent4', 'Antecedent5', 'Sensitivity', 'TP', 'FN', 'FP', 'TN'])


df1.to_csv('ant1.csv')
df2.to_csv('ant2.csv')
df3.to_csv('ant3.csv')
df4.to_csv('ant4.csv')
df5.to_csv('ant5.csv')
