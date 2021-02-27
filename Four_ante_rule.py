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
                                      #Will save columns with S>0.8


rcg_cols = []

for i in data.columns:
    if re.search("_RCG$", i):
        rcg_cols.append(i)

grit_cols = []

for i in data.columns:
    if re.search('GRIT_E2k$', i):
        grit_cols.append(i)

'''Copy here'''

hs4 = []
col4 = []
for column1 in columns:
    for column2 in rcg_cols:
        for i in range(len(grit_cols)-1):
            for j in range(i+1, len(grit_cols)):
            
            
                column3, column4 = grit_cols[i], grit_cols[j]
           
                #Name of antecedent 2 and 3
                ante1, ante2, ante3, ante4 = data[column1].tolist(), data[column2].tolist(), data[column3].tolist(), data[column4].tolist()   
                ante = [ante1[k]*ante2[k] for k in range(len(ante2))]
                ante = [ante[k]*ante3[k] for k in range(len(ante2))]             #And operation between ante 1,2,3,4
                ante = [ante[k]*ante4[k] for k in range(len(ante2))]             
            
                s, tp, fn, fp, tn = sensitivity(ante, cons)
            
                if s>0.8 and tp > 30:
                    hs4.append((column1, column2, column3, column4, s, tp, fn, fp, tn))
hs4 = sorted(hs4, reverse=True, key = lambda x: x[4])
df4 = pd.DataFrame(hs4, columns=['Antecedent1','Antecedent2', 'Antecedent3', 'Antecedent4' ,'Sensitivity', 'TP', 'FN', 'FP', 'TN'])
