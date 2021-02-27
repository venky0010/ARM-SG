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
'''Copy here'''

hs3 = []
col3 = []
for column1 in columns:
    for column2 in rcg_cols:
        for column3 in grit_cols:
            
                         #Name of antecedent 2 and 3
            ante1, ante2, ante3 = data[column1].tolist(), data[column2].tolist(), data[column3].tolist()    
            ante = [ante1[k]*ante2[k] for k in range(len(ante2))]
            ante = [ante[k]*ante3[k] for k in range(len(ante2))]             #And operation between ante 1,2,3
            
            s, tp, fn, fp, tn = sensitivity(ante, cons)
            
            if s>0.8 and tp > 30:
                hs3.append((column1, column2, column3, s, tp, fn, fp, tn))
hs3 = sorted(hs3, reverse=True, key = lambda x: x[4])
df3 = pd.DataFrame(hs3, columns=['Antecedent1','Antecedent2', 'Antecedent3' ,'Sensitivity', 'TP', 'FN', 'FP', 'TN'])
