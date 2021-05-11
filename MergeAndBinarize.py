#Anagha's code for reading GRIT file and its preprocessing
import pandas as pd
import numpy as np
#Reading INTERCO and RCR
grit_e2k_data = pd.read_csv("GRIT_E2k_PCI_G2279.csv",skipinitialspace=True)
grit_e2k_data.fillna('missing', inplace=True)
grit_e2k_data = grit_e2k_data.add_suffix('_GRIT_E2k')
del_cols=['PUBLISH_DATE_GRIT_E2k','INVENTORY_DATE_GRIT_E2k','PRC_IAS_LIABILITY_GRIT_E2k','PRC_IAS_ASSET_GRIT_E2k',
          'PRC_FR_LIABILITY_GRIT_E2k','PRC_FR_ASSET_GRIT_E2k','E2KPCI_LOCREP_CCY_AMT_GRIT_E2k',
          'E2KPCI_LOCREP_CCY_AMT_CPT_GRIT_E2k','E2KPCI_GRP_AMT_GRIT_E2k']

for i in del_cols:
    del grit_e2k_data[i]

"""GRIT ADJ OPENING"""

grit_adj_data = pd.read_csv("GRIT_PRC_ADJ_2020.csv",skipinitialspace=True)
grit_adj_data.fillna('missing', inplace=True)
grit_adj_data = grit_adj_data.add_suffix('_GRIT_ADJ')
grit_adj_data.head()


grit_e2k_enitiy_list=grit_e2k_data['ENTITY_GRIT_E2k'].tolist()
grit_e2k_counterparty_list=grit_e2k_data['COUNTERPART_GRIT_E2k'].tolist()
grit_e2k_crncy_list=grit_e2k_data['CURRENCY_GRIT_E2k'].tolist()
grit_e2k_prc_ias_list=grit_e2k_data['PRC_IAS_GRIT_E2k'].tolist()
grit_e2k_prc_fr_list=grit_e2k_data['PRC_FR_GRIT_E2k'].tolist()
grit_e2k_chap_fr_list=grit_e2k_data['CHPFR_GRIT_E2k'].tolist()
grit_e2k_chap_ias_list=grit_e2k_data['CHPIAS_GRIT_E2k'].tolist()
grit_adj_entity_list=grit_adj_data['ENTITY_GRIT_ADJ'].tolist()
grit_adj_counterparty_list=grit_adj_data['COUNTERPART_GRIT_ADJ'].tolist()
grit_adj_crncy_list=grit_adj_data['TRAN_CURRENCY_GRIT_ADJ'].tolist()
grit_adj_prc_list=grit_adj_data['PRC_GRIT_ADJ'].tolist() 
grit_adj_chap_list=grit_adj_data['CHAPTER_GRIT_ADJ'].tolist() 

 	 	
for j in range(0,len(grit_e2k_enitiy_list)):
    for i in range(0,len(grit_adj_chap_list)):
        if grit_adj_entity_list[i]==grit_e2k_enitiy_list[j] and grit_adj_counterparty_list[i]==grit_e2k_counterparty_list[j] and grit_adj_crncy_list[i]==grit_e2k_crncy_list[j]:
            q1=grit_adj_prc_list[i]
            q2=grit_e2k_prc_ias_list[j]
            q3=grit_e2k_prc_fr_list[j]
            if str(q1)==str(q2) or str(q1)==str(q3):
                w1=grit_adj_chap_list[i] 
                w2=grit_e2k_chap_fr_list[j]
                w3=grit_e2k_chap_ias_list[j]
                if (w1==w2) or (w1==w3):
                    grit_e2k_data.loc[j,'PRC_GRIT_ADJ']=str(grit_adj_data.loc[i,'PRC_GRIT_ADJ'])
                    grit_e2k_data.loc[j,'CHAPTER_GRIT_ADJ']=str(grit_adj_data.loc[i,'CHAPTER_GRIT_ADJ'])
                    grit_e2k_data.loc[j,'GAAP_TYPE_GRIT_ADJ']=str(grit_adj_data.loc[i,'GAAP_TYPE_GRIT_ADJ'])
                    grit_e2k_data.loc[j,'TRAN_AMOUNT_ADJ_GRIT_ADJ']=str(grit_adj_data.loc[i,'TRAN_AMOUNT_ADJ_GRIT_ADJ'])
                    grit_e2k_data.loc[j,'TOTAL_AFTER_ADJ_GRIT_ADJ']=str(grit_adj_data.loc[i,'TOTAL_AFTER_ADJ_GRIT_ADJ'])
                    grit_e2k_data.loc[j,'ADJUSTMENT_TYPE_GRIT_ADJ']=str(grit_adj_data.loc[i,'ADJUSTMENT_TYPE_GRIT_ADJ'])
grit_e2k_data.head()

#deleting non mi records
grit_e2k_datas=grit_e2k_data.copy()
for i in range(0,len(grit_e2k_datas)):
    if grit_e2k_data.loc[i,'SOURCE_GRIT_E2k']!='MI':
        grit_e2k_data=grit_e2k_data.drop(i)
grit_e2k_data.fillna('missing', inplace=True)
grit_e2k_data = grit_e2k_data.reset_index(drop=True)



#Venkatesh's Code to left join and binarize the GRIT-RCR files.

import re
rcr = pd.read_csv('GRACE_G2279.csv')
rcr.fillna('missing', inplace=True)
rcr = rcr.add_suffix('_RCR')
grit_e2k_data.insert(0, 'ID', range(0, 0 + len(grit_e2k_data)))

#INTERCO-RCR Join using two keys
interco_rcr = pd.merge(grit_e2k_data, rcr, left_on=['ACCOUNT_GRIT_E2k','DEPTID_GRIT_E2k','AFFILIATE_GRIT_E2k','CURRENCY_GRIT_E2k','BUSINESS_UNIT_GRIT_E2k',], 
                       right_on = ['ACCOUNT_RCR', 'DEPTID_RCR','AFFILIATE_RCR','CURRENCY_RCR','BUSINESS_UNIT_RCR'], how = 'left')

#Merge the aggregated values
interco_rcr.fillna('missing', inplace=True)
int_rcr = interco_rcr.groupby('ID').agg({column: lambda x: x.unique().tolist() for column in rcr.columns})
grit_rcr_data = grit_e2k_data.copy()
for column in int_rcr.columns[1:]:
    grit_rcr_data[column] = int_rcr[column]

#Deleting columns which might increase columns in binary files    
data = grit_rcr_data.copy()
delete_column = ['ID', 'DEAL_ID_RCR', 'TRADE_ID_RCR', 'TRADE_RISK_ID_RCR']
for column in delete_column:
    del data[column]
    
#Change the amount values into categorical ones, > or = or <    
amount_columns = ['E2K_PCI_AGG_AMOUNT_GRIT_E2k', 'RISK_AMOUNT_RCR', 'RISK_ENTRIES_RCR', 'INVENTORY_AMOUNT_RCR', 
                  'TOTAL_INVENTORY_RCR', 'AMOUNT_RCR', 'TOTAL_RISK_BASE_CCY_RCR', 
                  'TOTAL_INVENTORY_BASE_CCY_RCR', 'TOTAL_RISK_RCR','DISCREPANCY_RCR', 'DISCREPANCY_BASE_CCY_RCR']

for column in amount_columns:
    if re.search('RCR', column):
        for i in range(len(data)):
            s = 0
            val = data.loc[i, column]
            if val[0]=='missing':
                data.loc[i, column] = 'missing'
                continue
            s = sum(val)
            if s == 0:
                data.loc[i, column] = 'AMOUNT=0'
            elif s > 0:
                data.loc[i, column] = 'AMOUNT>0'
            elif s < 0:
                data.loc[i, column] = 'AMOUNT<0'
    if re.search('GRIT', column):
        for i in range(len(data)):
            val = data.loc[i, column]
            if val == 'missing':
                continue
            if val == 0:
                data.loc[i, column] = 'AMOUNT=0'
            elif val > 0:
                data.loc[i, column] = 'AMOUNT>0'
            elif val < 0:
                data.loc[i, column] = 'AMOUNT<0'

#Change the list types to str and select 1st element from the aggregated values
for column in data.columns[27:]:
    for i in range(len(data)):
        val = data.loc[i, column]
        if type(val) == list:
            val = val[0]
            
#Binarize the file
import re

def binarize(column, values, data):
    columns_ = []
    
    if re.search('GRIT', column):   
        for val in values:
            val = str(val)+str('_')+str(column)
            columns_.append(val)
            
        dummy = pd.DataFrame(np.zeros((len(data), len(values))), columns=columns_)
        for i in range(len(data)):
            val = data.loc[i, column]
            if val == 'missing':
                continue
            else:
                col = str(val)+str('_')+str(column)
                dummy.loc[i, col] = 1
        return dummy
    
    if re.search('RCR', column):
        
        for val in values:
            if type(val) == list:
                val = val[0]
            val = str(val)+str('_')+str(column)
            columns_.append(val)
            
        dummy = pd.DataFrame(np.zeros((len(data), len(values))), columns=columns_)
        for i in range(len(data)):
            val = data.loc[i, column]
            if val == 'missing':
                continue
            else:
                col = str(val)+str('_')+str(column)
                dummy.loc[i, col] = 1
        return dummy         

bin_data = pd.DataFrame([i for i in range(len(data))], columns=['Index'])
for column in data.columns:
    print(column)
    values = list(set(data[column].tolist()))
    df = binarize(column, values, data)
    type(df)
    bin_data = bin_data.join(df)
        data.loc[i, column] = val
