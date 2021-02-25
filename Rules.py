#Sensitivity Function

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
  
  
cons = data['SECONDBIT=1_APP_ORGIN_RCG'].tolist() #Consequent (Binarized list of len equal to data len)

columns = []                                      #Will save columns with S>0.8
hs = []                                           #Will be used to create data frame
for i in range(1, len(data.columns)):             #Column 1 is index
        
        col1 = data.columns[i]
        
        if col1 == 'BREAK=0_RCG' or col1 == 'SECONDBIT=1_APP_ORGIN_RCG':
            continue
            
        ante1 = data[col1].tolist()
        else:
            s, tp, fn, fp, tn = sensitivity(ante1, cons) #Cons is Consequent, initialized in early part of the code
            
            if s>0.8 and tp>100:
                columns.append(col1)
                hs.append((col1, s, tp, fn, fp, tn))
                
hs = sorted(hs, reverse=True, key = lambda x: x[2])
df1 = pd.DataFrame(l1, columns = ['Antecedent', 'Sensitivity', 'TP', 'FN', 'FP', 'TN'])



hs2 = []
for ante1 in columns:                                                #Antecedent 1 will be from saved columns from previous rule
    for i in range(1,len(data.columns)):                             #Looping through all data columns
        
        ante2 = data.columns[i]                                      #Columns name of antecedent 2, will skip if present in columns saved
        if ante2 in columns:
            continue
        
        ante1, ante2 = data[ante1].tolist(), data[ante2].tolist()
        ant = [ant1[i]*ant2[i] for i in range(len(ant1))]
        
        s, tp, fn, fp, tn = sensitivity(ant, cons)
        if s>0.75 and tp>100:
    
            hs2.append((col1[i], col1[j], s, tp, fn, fp, tn))

hs2 = sorted(hs2, reverse=True, key = lambda x: x[3])
df2 = pd.DataFrame(hs2, columns=['Antecedent1', 'Antecedent2',  'Sensitivity', 'TP', 'FN', 'FP', 'TN'])


hs3 = []
col3 = []
for column1 in columns:
    for i in range(1, len(data.columns)-1):
        for j in range(i+1, len(data.columns)):
            
            column2, column3 = data.columns[i], data.columns[j]              #Name of antecedent 2 and 3
            ante1, ante2, ante3 = data[column1].tolist(), data[column2].tolist(), data[column3].tolist()    
            ante = [ante1[k]*ante2[i] for k in range(len(ante2))]
            ante = [ante[k]*ante3[k] for k in range(len(ante2))]             #And operation between ante 1,2,3
            
            s, tp, fn, fp, tn = sensitivity(ante, cons)
            if s>0.85 and tp>100:
                hs3.append((column1, column2, column3, s, tp, fn, fp, tn))
hs3 = sorted(hs3, reverse=True, key = lambda x: x[4])
df3 = pd.DataFrame(hs3, columns=['Antecedent1','Antecedent2', 'Antecedent3' ,'Sensitivity', 'TP', 'FN', 'FP', 'TN'])
df3.to_csv('threeAnte.csv')
