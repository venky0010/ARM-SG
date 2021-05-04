import pandas as pd
import numpy as np
data=pd.read_csv('gritd2_d3_rcg_mi_e2k_prc_final_new2.csv',skipinitialspace=True) 
data.head()

"""CREATING FIELDS
"""

#creating columns
import ast
import re
cols=['SOURCE_APPN_IDS_MI','ENTITY_GRIT_INITIAL','COUNTERPART_GRIT_INITIAL','CHPFR_GRIT_INITIAL','CHPIAS_GRIT_INITIAL','CLASS_FR_GRIT_INITIAL','CLASS_IAS_GRIT_INITIAL','PRC_IAS_GRIT_INITIAL','PRC_FR_GRIT_INITIAL','ENTITY_GRIT_E2k','COUNTERPART_GRIT_E2k','CHPFR_GRIT_E2k','CHPIAS_GRIT_E2k','CLASS_FR_GRIT_E2k','CLASS_IAS_GRIT_E2k','PRC_IAS_GRIT_E2k','PRC_FR_GRIT_E2k','ADJUSTMENT_TYPE_GRIT_ADJ','PRC_GRIT_ADJ','CHAPTER_GRIT_ADJ','GAAP_TYPE_GRIT_ADJ','CCY_CD_RCG','FIN_CLASS_RCG','AFFIL_CD_RCG','GLACCT_NBR_RCG','INTERNALPNLFAMILY_E2K','ACCOUNTTYPE_E2K','CHARTOFACCOUNTTYPE_E2K','ACCOUNTINGNORM_E2K','ACCOUNTMONETARYTYPE_E2K','ACCOUNTBALANCE_E2K','INTERNALEXTERNAL_E2K','IASECONOMICPURPOSE_E2K','VALUATIONMETHOD_E2K','TRANSACTIONALINDICATOR_E2K','INTERCOFOLLOWUPTYPE_E2K','BASELPERIMETER_E2K','BASELAMOUNTTYPE_E2K','GLOBALBASELRECONCILIATION_E2K','PRCACCOUNTENGLISHNAME_IAS_PRC','ACCOUNTCLASS_IAS_PRC','ACCOUNTMONETARYTYPE_IAS_PRC','ACCOUNTBALANCE_IAS_PRC','PRCECONOMICPURPOSE_IAS_PRC','INTERCOFOLLOWUPTYPE_IAS_PRC','BASELPERIMETER_IAS_PRC','PRCACCOUNTENGLISHNAME_GAAP_PRC','ACCOUNTCLASS_GAAP_PRC','ACCOUNTMONETARYTYPE_GAAP_PRC','ACCOUNTBALANCE_GAAP_PRC','PRCECONOMICPURPOSE_GAAP_PRC','INTERCOFOLLOWUPTYPE_GAAP_PRC']
data_cols=[]
for i in cols:
    values=data[i].tolist()
    unique_values=list(set(values))
    values_with_suffix = [sub + '_'+str(i) for sub in unique_values]
    data_cols.extend(values_with_suffix)
extra_cols=['NOT_PEC_AND_QTZ_SOURCE_APPN_IDS_MI','missing_SOURCE_APPLICATION_ID_MI','DIFF=missing_E2K_PCI_AGG_AMOUNT_DIFF_PERCENTAGE_GRIT','0<DIFF_PERCENTAGE<=25_E2K_PCI_AGG_AMOUNT_DIFF_PERCENTAGE_GRIT','25<DIFF_PERCENTAGE<=50_E2K_PCI_AGG_AMOUNT_DIFF_PERCENTAGE_GRIT','50<DIFF_PERCENTAGE<=75_E2K_PCI_AGG_AMOUNT_DIFF_PERCENTAGE_GRIT','75<DIFF_PERCENTAGE<=100_E2K_PCI_AGG_AMOUNT_DIFF_PERCENTAGE_GRIT','DIFF!=0_E2K_PCI_AGG_AMOUNT_DIFF_GRIT','DIFF=missing_E2K_PCI_AGG_AMOUNT_DIFF_GRIT','WITHIN_ENTITY_INTERCO_TYPE_GRIT_E2k','SAME_REGION_INTERCO_TYPE_GRIT_E2k','INTRA_REGION_INTERCO_TYPE_GRIT_E2k','NON_SGCIB_ENTITY_INTERCO_TYPE_GRIT_E2k','QTZ_SOURCE_APPLICATION_ID_MI','NOT_PEC&QTZ_SOURCE_APPLICATION_ID_MI','BOTH_PEC&QTZ_SOURCE_APPLICATION_ID_MI','PEC_SOURCE_APPLICATION_ID_MI','INVENTORYIS-_ORIG_CCY_MEAS_AMT_RCG','INVENTORY=0_ORIG_CCY_MEAS_AMT_RCG','INVENTORYIS+_ORIG_CCY_MEAS_AMT_RCG','GLIS-_GLACCT_BAL_AMT_RCG','GL=0_GLACCT_BAL_AMT_RCG','GLIS+_GLACCT_BAL_AMT_RCG','BREAKIS-_ORIG_CCY_DIFF_AMT_RCG','BREAK=0_ORIG_CCY_DIFF_AMT_RCG','BREAKIS+_ORIG_CCY_DIFF_AMT_RCG','FIRSTBIT=1_APP_ORGIN_RCG','SECONDBIT=0_APP_ORGIN_RCG','THIRDBIT=1_APP_ORGIN_RCG']
data_cols.extend(extra_cols)
mi_cols=['ADJUSTMENT_TYPE_MI','PRC_IAS_MI','CONSO1_MI','EVENT_NATURE_MI','OPERATION_CODE_MI','OPERATION_DIRECTION_MI','TRANSACTION_TYPE_MI']
mi_vals=[]
for i in mi_cols:
    values=[]
    x=data[i].tolist()
    for j in x:
        if j=='missing' or j=="['missing']":
            continue
        else:
            m = ast.literal_eval(j)
            values.extend(m)
  
    values_with_suffix = [sub + '_'+str(i) for sub in values]
    unique_values=list(set(values_with_suffix))
    mi_vals.extend(unique_values)
data_cols.extend(mi_vals)
data_cols =[x for x in data_cols if not x.startswith('missing')]
bin_data = pd.DataFrame(0, index=np.arange(len(data)), columns=data_cols) 

#entering values


for j in cols:
    for i in range(0,len(data)):
        item=data.loc[ i,j]
        if item.startswith('missing'):
            continue
        else:
            item=data.loc[ i,j]+'_'+str(j)
            bin_data.loc[ i,item]=1
w='_SOURCE_APPN_IDS_MI'+'$'
o=[]
k=list(bin_data.columns)
for i in k:
    if re.search(w, i):
        o.append(i)
o.remove('NOT_PEC_AND_QTZ_SOURCE_APPN_IDS_MI')
for i in o:
    if i!='PEC_and_QTZ_SOURCE_APPN_IDS_MI':
   
        val=bin_data[i].tolist()
        for j in range(0,len(val)):
            if val[j]==1:
                bin_data.loc[ j,'NOT_PEC_AND_QTZ_SOURCE_APPN_IDS_MI']=1
diff_amount=data['E2K_PCI_AGG_AMOUNT_DIFF_GRIT'].tolist()
for i in range(0,len(diff_amount)):
    if diff_amount[i]=='missing':
        bin_data.loc[ i,'DIFF=missing_E2K_PCI_AGG_AMOUNT_DIFF_GRIT']=1   
    else:  
        bin_data.loc[ i,'DIFF=missing_E2K_PCI_AGG_AMOUNT_DIFF_GRIT']=0 
        num=float(diff_amount[i])
        if num==0:
            bin_data.loc[ i,'DIFF!=0_E2K_PCI_AGG_AMOUNT_DIFF_GRIT']=0
        else:
            bin_data.loc[ i,'DIFF!=0_E2K_PCI_AGG_AMOUNT_DIFF_GRIT']=1    

diff_amount=data['E2K_PCI_AGG_AMOUNT_DIFF_PERCENTAGE_GRIT'].tolist()
for i in range(0,len(diff_amount)):
    if diff_amount[i]=='missing':
        bin_data.loc[ i,'DIFF=missing_E2K_PCI_AGG_AMOUNT_DIFF_PERCENTAGE_GRIT']=1   
    else:  
        bin_data.loc[ i,'DIFF=missing_E2K_PCI_AGG_AMOUNT_DIFF_PERCENTAGE_GRIT']=0 
        num=float(diff_amount[i])
        if num<=.25:
            bin_data.loc[ i,'0<DIFF_PERCENTAGE<=25_E2K_PCI_AGG_AMOUNT_DIFF_PERCENTAGE_GRIT']=1
        elif num<=0.5:
            bin_data.loc[ i,'25<DIFF_PERCENTAGE<=50_E2K_PCI_AGG_AMOUNT_DIFF_PERCENTAGE_GRIT']=1 
        elif num<=.75:
            bin_data.loc[ i,'50<DIFF_PERCENTAGE<=75_E2K_PCI_AGG_AMOUNT_DIFF_PERCENTAGE_GRIT']=1
        elif num<=1:
            bin_data.loc[ i,'75<DIFF_PERCENTAGE<=100_E2K_PCI_AGG_AMOUNT_DIFF_PERCENTAGE_GRIT']=1 
rcg_col=['ORIG_CCY_MEAS_AMT_RCG','GLACCT_BAL_AMT_RCG','ORIG_CCY_DIFF_AMT_RCG']
for ii in range(0,len(rcg_col)):
    col=data[rcg_col[ii]].tolist()
    for i in range(0,len(col)):         
        if col[i]=='missing':
            continue
        else:
            if ii==0:
                if float(col[i])<0:
                    bin_data.loc[ i,'INVENTORYIS-_ORIG_CCY_MEAS_AMT_RCG']=1    
                                     
                elif float(col[i])==0:
                    bin_data.loc[ i,'INVENTORY=0_ORIG_CCY_MEAS_AMT_RCG']=1
                else:                       
                    bin_data.loc[ i,'INVENTORYIS+_ORIG_CCY_MEAS_AMT_RCG']=1
                      
            elif ii==2:
                if float(col[i])<0:
                    bin_data.loc[ i,'BREAKIS-_ORIG_CCY_DIFF_AMT_RCG']=1
                    
                elif float(col[i])==0:
                    bin_data.loc[ i,'BREAK=0_ORIG_CCY_DIFF_AMT_RCG']=1
                else:
                        
                    bin_data.loc[ i,'BREAKIS+_ORIG_CCY_DIFF_AMT_RCG']=1
            elif ii==1:
                if float(col[i])<0:
                    bin_data.loc[ i,'GLIS-_GLACCT_BAL_AMT_RCG']=1
                       
                    
                elif float(col[i])==0:
                    bin_data.loc[ i,'GL=0_GLACCT_BAL_AMT_RCG']=1
                else:                        
                    bin_data.loc[ i,'GLIS+_GLACCT_BAL_AMT_RCG']=1
app_orgin_list=data['APP_ORIGIN_RCG'].tolist()
for i in range(0,len(app_orgin_list)):
    if app_orgin_list[i]=='missing':
        continue
    else:   
        num=str(app_orgin_list[i]).zfill(3)
        if num[0]=="1":
            bin_data.loc[ i,'FIRSTBIT=1_APP_ORGIN_RCG']=1
        if num[1]=="0":
            bin_data.loc[ i,'SECONDBIT=0_APP_ORGIN_RCG']=1       
        if num[2]=="1":
            bin_data.loc[ i,'THIRDBIT=1_APP_ORGIN_RCG']=1

interco=data['INTERCO_TYPE_GRIT_E2k'].tolist()
for i in range(0,len(interco)):
    if interco[i]=='missing':
        continue
    else:   
        num=str(interco[i])
        if num=="0.0":
            bin_data.loc[ i,'WITHIN_ENTITY_INTERCO_TYPE_GRIT_E2k']=1
        elif num=="1.0":
            bin_data.loc[ i,'SAME_REGION_INTERCO_TYPE_GRIT_E2k']=1       
        elif num=="2.0":
            bin_data.loc[ i,'INTRA_REGION_INTERCO_TYPE_GRIT_E2k']=1
        elif num=="3.0":
            bin_data.loc[ i,'NON_SGCIB_ENTITY_INTERCO_TYPE_GRIT_E2k']=1
adjustment_list=data['ADJUSTMENT_TYPE_MI'].tolist()
for i in range(0,len(adjustment_list)):
    if adjustment_list[i]=='missing' or adjustment_list[i]=="['missing']":
        continue
    else:   
        org_list= ast.literal_eval(adjustment_list[i])
        for j in org_list:
            if str(j)=='missing':
                continue
            else:
                item_s=str(j)+'_'+'ADJUSTMENT_TYPE_MI'
                bin_data.loc[i,item_s]=1

adjustment_list=data['SOURCE_APPLICATION_ID_MI'].tolist()
for i in range(0,len(adjustment_list)):
    if adjustment_list[i]=='missing' or adjustment_list[i]=="['missing']":
        bin_data.loc[i,'missing_SOURCE_APPLICATION_ID_MI']=1
    else:   
        org_list= ast.literal_eval(adjustment_list[i])
        if ('QTZ' in org_list )and ('PEC' in org_list):
            bin_data.loc[i,'BOTH_PEC&QTZ_SOURCE_APPLICATION_ID_MI']=1
            bin_data.loc[i,'missing_SOURCE_APPLICATION_ID_MI']=0
        elif 'QTZ' in org_list:
            bin_data.loc[i,'QTZ_SOURCE_APPLICATION_ID_MI']=1
            bin_data.loc[i,'NOT_PEC&QTZ_SOURCE_APPLICATION_ID_MI']=1
            bin_data.loc[i,'missing_SOURCE_APPLICATION_ID_MI']=0
        elif 'PEC' in org_list:
            bin_data.loc[i,'PEC_SOURCE_APPLICATION_ID_MI']=1
            bin_data.loc[i,'NOT_PEC&QTZ_SOURCE_APPLICATION_ID_MI']=1
            bin_data.loc[i,'missing_SOURCE_APPLICATION_ID_MI']=0



adjustment_list=data['PRC_IAS_MI'].tolist()
for i in range(0,len(adjustment_list)):
    if adjustment_list[i]=='missing' or adjustment_list[i]=="['missing']":
        continue
    else:   
        org_list= ast.literal_eval(adjustment_list[i])
        item_sets=str(org_list[0])+'_'+'PRC_IAS_MI'
        bin_data.loc[i,item_sets]=1

adjustment_list=data['CONSO1_MI'].tolist()
for i in range(0,len(adjustment_list)):
    if adjustment_list[i]=='missing' or adjustment_list[i]=="['missing']":
        continue
    else:   
        org_list= ast.literal_eval(adjustment_list[i])
        for j in org_list:
            if str(j)=='missing':
                continue
            else:
                item_s=str(j)+'_'+'CONSO1_MI'
                bin_data.loc[i,item_s]=1
adjustment_list=data['EVENT_NATURE_MI'].tolist()
for i in range(0,len(adjustment_list)):
    if adjustment_list[i]=='missing' or adjustment_list[i]=="['missing']":
        continue
    else:   
        org_list= ast.literal_eval(adjustment_list[i])
        for j in org_list:
            if str(j)=='missing':
                continue
            else:
                item_s=str(j)+'_'+'EVENT_NATURE_MI'
                bin_data.loc[i,item_s]=1
adjustment_list=data['OPERATION_CODE_MI'].tolist()

for i in range(0,len(adjustment_list)):
    if adjustment_list[i]=='missing' or adjustment_list[i]=="['missing']":
        continue
    else:   
        org_list= ast.literal_eval(adjustment_list[i])
        for j in org_list:
            if str(j)=='missing':
                continue
            else:
                item_s=str(j)+'_'+'OPERATION_CODE_MI'
                bin_data.loc[i,item_s]=1
adjustment_list=data['TRANSACTION_TYPE_MI'].tolist()
for i in range(0,len(adjustment_list)):
    if adjustment_list[i]=='missing' or adjustment_list[i]=="['missing']":
        continue
    else: 
        org_list= ast.literal_eval(adjustment_list[i])
        for j in org_list:
            if str(j)=='missing':
                continue
            else:
                item_s=str(j)+'_'+'TRANSACTION_TYPE_MI'
                bin_data.loc[i,item_s]=1  


adjustment_list=data['OPERATION_DIRECTION_MI'].tolist()
for i in range(0,len(adjustment_list)):
    if adjustment_list[i]=='missing' or adjustment_list[i]=="['missing']":
        continue
    else:   
        org_list= ast.literal_eval(adjustment_list[i])
        for j in org_list:
            if str(j)=='missing':
                continue
        else:
            item_s=str(j)+'_'+'OPERATION_DIRECTION_MI'
            bin_data.loc[i,item_s]=1

bin_data.head()

bin_data.to_csv('binarized_g2279_final4.csv')
