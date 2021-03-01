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

def two_antecedent(column1, column2, cons):
    
    ant1, ant2 = data[column1].tolist(), data[column2].tolist()
    ant1 = [ante1[i]*ante2[i] for i in range(len(ante1))]
    return sensitivity(ant1, cons)

def three_antecedent(column1, column2, column3, cons):
    
    ant1, ant2, ant3 = data[column1].tolist(), data[column2].tolist(), data[column3].tolist()
    ante = [ante1[k]*ante2[k] for k in range(len(ante2))]
    ante = [ante[k]*ante3[k] for k in range(len(ante))]
    return sensitivity(ante, cons)
       
def four_antecedent(column1, column2, column3, column4, cons):
    
    ant1, ant2, ant3, ante4 = data[column1].tolist(), data[column2].tolist(), data[column3].tolist(), data[column4].tolist()
    ante = [ante1[k]*ante2[k] for k in range(len(ante2))]
    ante = [ante[k]*ante3[k] for k in range(len(ante))]
    ante = [ante[k]*ante4[k] for k in range(len(ante))]
    return sensitivity(ante, cons)
    

    
def five_antecedent(ant, cons):
    
    df = []
    
    

def rules(data, columns, rcg_cols, grit_cols):
    
    cons = data['SECONDBIT=1_APP_ORGIN_RCG'].tolist()
    df1 = []
    df2 = []
    df3 = []
    df4 = []
    df5 = []
    for column1 in columns:
        s, tp, fn, fp, tn = sensitivity(data[column1].tolist(), cons)
        if s>0.7 and tp > 30:
            df1.append((column1, s, tp, fn, fp, tn))
        
        for column2 in rcg_cols:
            s, tp, fn, fp, tn = two_antecedent(column1, column2, cons)
            if s>0.75 and tp > 30:
                df2.append((column1, column2, s, tp, fn, fp, tn))
            
            for column3 in grit_cols:
                s, tp, fn, fp, tn = three_antecedent(column1, column2, column3, cons)
                if s>0.8 and tp > 30:
                    df3.append((column1, column2, column3, s, tp, fn, fp, tn))
                
                for column4 in grit_cols:
                    s, tp, fn, fp, tn = four_antecedent(column1, column2, column3, column4, cons)
                    if s>0.8 and tp > 30:
                        df4.append((column1, column2, column3, column4, s, tp, fn, fp, tn))
                        
    return df1, df2, df3, df4


data = pd.read_csv('GRIT26.csv')

columns = ['SOURCE_APPLICATION_ID=QTZ_MI', 'SOURCE_APPLICATION_ID=PEC/QTZ_MI', 'SOURCE_APPLICATION_ID=PEC_MI']   
rcg_cols = []
for i in data.columns:
    if re.search("_RCG$", i):
        rcg_cols.append(i)

grit_cols = []
for i in data.columns:
    if re.search('GRIT_E2k$', i):
        grit_cols.append(i)
        
cons = data['SECONDBIT=1_APP_ORGIN_RCG'].tolist()

df1, df2, df3, df4 = rules(data, columns, rcg_cols, grit_cols)
