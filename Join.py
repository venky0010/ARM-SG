import pandas as pd 
import numpy as np
rcg_data = pd.read_csv("RCG_G2279_20210121.csv",skipinitialspace=True)

rcg_data.fillna('missing', inplace=True)
del_cols=['CHAR_FIELD1','CHAR_FIELD2','CHAR_FIELD3','CHAR_FIELD4','CHAR_FIELD5','AMOUNT_FIELD1','AMOUNT_FIELD2','AMOUNT_FIELD3','AMOUNT_FIELD4','AMOUNT_FIELD5','DATE_FIELD1','DATE_FIELD2','DATE_FIELD3','E2KACCT_DESC','LCL_CCY_DIFF_AMT']
for i in del_cols:
    del rcg_data[i]
rcg_data = rcg_data.add_suffix('_RCG')
rcg_data.insert(0, 'ID', range(0, 0 + len(rcg_data)))

rcg_cols=list(rcg_data.columns) 
rcg_data.head()

len(rcg_data)

"""READING MI"""

mi_data = pd.read_csv("MI_G2279.csv",skipinitialspace=True)
mi_data.fillna('missing', inplace=True)
del_cols=['DLR_PUBLISH_DATE','TRANSACTION_ID','INVENTORY_DATE','PORTFOLIO_ID','PARTY_ID','PRODUCT_GUID','ADJUSTMENT_DATE','VALUE_DATE','AFF_CODFIL','CONSO1_SUFF','OBJECT','MATURITY_DATE','CLOSING_DATE']
for i in del_cols:
    del mi_data[i]
mi_data = mi_data.add_suffix('_MI')
mi_data.head()

len(mi_data)

"""MERGING MI,RCG"""

rcg_mi_join = pd.merge(rcg_data, mi_data,  how='inner', left_on=['E2KACCT_NBR_RCG','BUS_UNIT_RCG','DEPT_ID_RCG','CCY_CD_RCG','ALTACCT_RCG','AFFIL_CD_RCG','GL_PROD_CD_RCG','OPERATING_UNIT_RCG','E2K_PRODUCT_CD_RCG'], right_on = ['ACCOUNT_MI','BUSINESS_UNIT_MI','DEPTID_MI','CURRENCY_MI','ALTACCT_MI','AFFILIATE_MI','OBJECT_CODE_MI','OPERATING_UNIT_MI','PRODUCT_MI'])
del_cols=['ACCOUNT_MI','BUSINESS_UNIT_MI','DEPTID_MI','CURRENCY_MI','ALTACCT_MI','AFFILIATE_MI','OBJECT_CODE_MI','OPERATING_UNIT_MI','PRODUCT_MI']
for i in del_cols:
    del rcg_mi_join[i]
rcg_mi_join.head()

len(rcg_mi_join)

mi=rcg_mi_join.groupby('ID').agg({'ID': lambda x: x.unique(),'TRANSACTION_TYPE_MI': lambda x: x.unique().tolist(),'TRAN_AMOUNT_MI': lambda x: x.unique().tolist(),'EVENT_NATURE_MI': lambda x: x.unique().tolist(),'ADJUSTMENT_TYPE_MI': lambda x: x.unique().tolist(),'SOURCE_APPLICATION_ID_MI': lambda x: x.unique().tolist(),'INVENTORY_TYPE_MI': lambda x: x.unique().tolist(),'OPERATION_CODE_MI': lambda x: x.unique().tolist(),'OPERATION_DIRECTION_MI': lambda x: x.unique().tolist(),'CONSO1_MI': lambda x: x.unique().tolist(),'PRC_IAS_MI': lambda x: x.unique().tolist(),'ORIGIN_SOURCE_ID_MI': lambda x: x.unique().tolist()})
mi_new=rcg_mi_join.groupby('ID').agg({'TRAN_AMOUNT_MI': lambda x: x.unique().tolist(),'TRANSACTION_TYPE_MI': lambda x: x.unique().tolist(),'EVENT_NATURE_MI': lambda x: x.unique().tolist(),'ADJUSTMENT_TYPE_MI': lambda x: x.unique().tolist(),'SOURCE_APPLICATION_ID_MI': lambda x: x.unique().tolist(),'INVENTORY_TYPE_MI': lambda x: x.unique().tolist(),'OPERATION_CODE_MI': lambda x: x.unique().tolist(),'OPERATION_DIRECTION_MI': lambda x: x.unique().tolist(),'CONSO1_MI': lambda x: x.unique().tolist(),'PRC_IAS_MI': lambda x: x.unique().tolist(),'ORIGIN_SOURCE_ID_MI': lambda x: x.unique().tolist()})
mi.head()

print(len(mi))

#TO REMOVE WRONG GLAAM FROM RCG
rows_present_in_rcg_mi=mi['ID'].tolist() #RECORD ID'S OF ROWS WHICH HAVE A MATCH IN MI


inventory_0_rows=[]#RECORDS WITH INVENTORY IS 0
for i in range (0,len(rcg_data)):
    if rcg_data.loc[ i,'ORIG_CCY_MEAS_AMT_RCG']==0  :
        inventory_0_rows.append(rcg_data.loc[ i,'ID'])



rows_not_present_in_rcg_mi=[]#RECORD ID'S OF ROWS WHICH DONT HAVE A MATCH IN MI
for i in range(0,2105):
    if i not in rows_present_in_rcg_mi:
        rows_not_present_in_rcg_mi.append(rcg_data.loc[ i,'ID'])


wrong_glaam=[]#finding wrong glaam records
for i in rows_not_present_in_rcg_mi:
    if i not in inventory_0_rows:
        wrong_glaam.append(i)

for i in wrong_glaam:#deleting records from rcg
    delete_row = rcg_data[rcg_data["ID"]==i].index
    rcg_data = rcg_data.drop(delete_row)
rcg_data = rcg_data.reset_index(drop=True)

print(len(rcg_data))

rcg_mi_merged=pd.merge(rcg_data, mi_new,  how='left', left_on=['ID'], right_on = ['ID'])
rcg_mi_merged.head()

len(rcg_mi_merged)

"""READING E2K
"""

e2k_data = pd.read_csv("E2K_REF.csv",skipinitialspace=True)
e2k_data.fillna('missing', inplace=True)
e2k_data['E2KACCOUNTID'] = e2k_data.E2KACCOUNTID.astype(str)
del_cols=['VERSIONEFFECTIVEDATE','E2KACCOUNTNAME','E2KACCOUNTLABEL','ACCOUNTAGGREGATEID','ACCOUNTAGGREGATEMNEMONIC','AGGREGATEAXISTYPE','REVERSALINDICATOR','FRENCHGAAPECONOMICPURPOSE','ACCOUNTINGFLOWNATURE','MULTIPRODUCTINDICATOR','PCINFOFIINDICATOR','INFOFI60INDICATOR','INTERESTRATENATURE','BASELDEALUPDATEPROCESSSCHEME','ACCOUNTFOLLOWUPMETHOD','MATCHINGINDICATOR','RETENTIONDAYCOUNT','INTACCOUNTAGGREGATEID','INTACCOUNTAGGREGATEMNEMONIC','EXTACCOUNTAGGREGATEID','EXTACCOUNTAGGREGATEMNEMONIC']
for i in del_cols:
    del e2k_data[i]
e2k_data = e2k_data.add_suffix('_E2K')
acnt=e2k_data['E2KACCOUNTID_E2K'].tolist()
acnt=list(map(str, acnt))
for i in range(0,len(e2k_data )):
    if ( e2k_data.loc[ i,'GAAPASSETPRCACCOUNTID_E2K']=='missing' and e2k_data.loc[ i,'GAAPLIABILITYPRCACCOUNTID_E2K']=='missing' and e2k_data.loc[ i,'IASLIABILITYPRCACCOUNTID_E2K']=='missing' and e2k_data.loc[ i,'IASASSETPRCACCOUNTID_E2K']=='missing' and e2k_data.loc[ i,'PARENTE2KACCOUNTID_E2K']!='missing'):
        parent=e2k_data.loc[ i,'PARENTE2KACCOUNTID_E2K']
        if str(parent) in acnt:
            we=e2k_data[e2k_data['E2KACCOUNTID_E2K']==parent].index.values
            new_acnt_indx=we[0]

        if e2k_data.loc[ new_acnt_indx,'GAAPASSETPRCACCOUNTID_E2K']!='missing' and e2k_data.loc[ new_acnt_indx,'GAAPLIABILITYPRCACCOUNTID_E2K']!='missing' and  e2k_data.loc[ new_acnt_indx,'IASLIABILITYPRCACCOUNTID_E2K']!='missing' and e2k_data.loc[ new_acnt_indx,'IASASSETPRCACCOUNTID_E2K']!='missing' :
            e2k_data.loc[ i,'IAS_E2K']='hybrid' 
            e2k_data.loc[ i,'GAAP_E2K']='hybrid'
        else:
            if e2k_data.loc[ new_acnt_indx,'IASASSETPRCACCOUNTID_E2K']!='missing' and e2k_data.loc[ new_acnt_indx,'IASLIABILITYPRCACCOUNTID_E2K']=='missing' :
                e2k_data.loc[ i,'IAS_E2K']=int(e2k_data.loc[ new_acnt_indx,'IASASSETPRCACCOUNTID_E2K'])
            elif e2k_data.loc[ new_acnt_indx,'IASLIABILITYPRCACCOUNTID_E2K']!='missing' and e2k_data.loc[ new_acnt_indx,'IASASSETPRCACCOUNTID_E2K']=='missing':
                e2k_data.loc[ i,'IAS_E2K']=int(e2k_data.loc[ new_acnt_indx,'IASLIABILITYPRCACCOUNTID_E2K'])
            elif e2k_data.loc[ new_acnt_indx,'IASLIABILITYPRCACCOUNTID_E2K']=='missing' and e2k_data.loc[ new_acnt_indx,'IASASSETPRCACCOUNTID_E2K']=='missing':
                e2k_data.loc[ i,'IAS_E2K']='missing'
            else:
                e2k_data.loc[ i,'IAS_E2K']='missing'

          
      
        if e2k_data.loc[ new_acnt_indx,'GAAPLIABILITYPRCACCOUNTID_E2K']!='missing' and e2k_data.loc[ new_acnt_indx,'GAAPASSETPRCACCOUNTID_E2K']=='missing':
            e2k_data.loc[ i,'GAAP_E2K']=int(e2k_data.loc[ new_acnt_indx,'GAAPLIABILITYPRCACCOUNTID_E2K'])
        elif e2k_data.loc[ new_acnt_indx,'GAAPASSETPRCACCOUNTID_E2K']!='missing' and e2k_data.loc[ new_acnt_indx,'GAAPLIABILITYPRCACCOUNTID_E2K']=='missing':
            e2k_data.loc[ i,'GAAP_E2K']=int(e2k_data.loc[ new_acnt_indx,'GAAPASSETPRCACCOUNTID_E2K'])
        elif e2k_data.loc[ new_acnt_indx,'GAAPASSETPRCACCOUNTID_E2K']=='missing' and e2k_data.loc[ new_acnt_indx,'GAAPLIABILITYPRCACCOUNTID_E2K']=='missing' :
            e2k_data.loc[ i,'GAAP_E2K']='missing'
        else:
            e2k_data.loc[ i,'GAAP_E2K']='missing'

    else:
        if e2k_data.loc[ i,'GAAPLIABILITYPRCACCOUNTID_E2K']!='missing' and e2k_data.loc[ i,'GAAPASSETPRCACCOUNTID_E2K']!='missing' and  e2k_data.loc[ i,'IASLIABILITYPRCACCOUNTID_E2K']!='missing' and e2k_data.loc[ i,'IASASSETPRCACCOUNTID_E2K']!='missing':
            e2k_data.loc[ i,'GAAP_E2K']='hybrid'
            e2k_data.loc[ i,'IAS_E2K']='hybrid'
        else:
            if e2k_data.loc[ i,'IASLIABILITYPRCACCOUNTID_E2K']!='missing' and e2k_data.loc[ i,'IASASSETPRCACCOUNTID_E2K']=='missing':
                e2k_data.loc[ i,'IAS_E2K']=int(e2k_data.loc[ i,'IASLIABILITYPRCACCOUNTID_E2K'])
            elif e2k_data.loc[ i,'IASLIABILITYPRCACCOUNTID_E2K']=='missing' and e2k_data.loc[ i,'IASASSETPRCACCOUNTID_E2K']!='missing':
                e2k_data.loc[ i,'IAS_E2K']=int(e2k_data.loc[ i,'IASASSETPRCACCOUNTID_E2K'])
        
            elif e2k_data.loc[ i,'IASLIABILITYPRCACCOUNTID_E2K']=='missing' and e2k_data.loc[ i,'IASASSETPRCACCOUNTID_E2K']=='missing':
                e2k_data.loc[ i,'IAS_E2K']='missing'
            else:
                e2k_data.loc[ i,'IAS_E2K']='missing' 


        if e2k_data.loc[ i,'GAAPLIABILITYPRCACCOUNTID_E2K']!='missing' and  e2k_data.loc[ i,'GAAPASSETPRCACCOUNTID_E2K']=='missing':
            e2k_data.loc[ i,'GAAP_E2K']=int(e2k_data.loc[ i,'GAAPLIABILITYPRCACCOUNTID_E2K'])
        elif e2k_data.loc[ i,'GAAPLIABILITYPRCACCOUNTID_E2K']=='missing' and e2k_data.loc[ i,'GAAPASSETPRCACCOUNTID_E2K']!='missing':
            e2k_data.loc[ i,'GAAP_E2K']=int(e2k_data.loc[ i,'GAAPASSETPRCACCOUNTID_E2K'])
        elif  e2k_data.loc[ i,'GAAPLIABILITYPRCACCOUNTID_E2K']=='missing' and e2k_data.loc[ i,'GAAPASSETPRCACCOUNTID_E2K']=='missing':
            e2k_data.loc[ i,'GAAP_E2K']='missing'
        else:
            e2k_data.loc[ i,'GAAP_E2K']='missing'

e2k_data.head()

print(len(e2k_data))

"""MERGING E2K,RCG,MI
"""

rcg_mi_merged['E2KACCT_NBR_RCG'] = rcg_mi_merged['E2KACCT_NBR_RCG'].astype(str)
e2k_data['E2KACCOUNTMNEMONIC_E2K'] = e2k_data['E2KACCOUNTMNEMONIC_E2K'].astype(str)
rcg_mi_e2k_merged = pd.merge(  rcg_mi_merged,e2k_data, how='inner', left_on=['E2KACCT_NBR_RCG'], right_on = ['E2KACCOUNTMNEMONIC_E2K'])
del rcg_mi_e2k_merged['E2KACCOUNTMNEMONIC_E2K']

#deleting hybrid accounts
delete_row = rcg_mi_e2k_merged[rcg_mi_e2k_merged["IAS_E2K"]=='hybrid'].index 
rcg_mi_e2k_merged = rcg_mi_e2k_merged.drop(delete_row)

rcg_mi_e2k_merged = rcg_mi_e2k_merged.reset_index(drop=True) 
rcg_mi_e2k_merged.head()

print(len(rcg_mi_e2k_merged))

"""READING PRC
"""

prc_data = pd.read_csv("PRC_REF.csv",skipinitialspace=True)
del_cols=['PRCACCOUNTFRENCHLABEL','PRCACCOUNTENGLISHLABEL','ACCOUNTINGNORM','VALIDITYSTARTDATE','VALIDITYENDDATE','PCINFOFIINDICATOR','INFOFI60INDICATOR','DRACALLOCATION','PRCBRANCHESNUMBER','START_DATE','END_DATE','STATUS']
for i in del_cols:
    del prc_data[i]
prc_data.fillna('missing', inplace=True)
ias_prc_data = prc_data.add_suffix('_IAS_PRC')
gaap_prc_data = prc_data.add_suffix('_GAAP_PRC')
gaap_prc_data.head()

print(len(ias_prc_data))
print(len(gaap_prc_data))

"""MERGING RCG,E2K,MI,PRC
"""

rcg_mi_e2k_prcias_merged= pd.merge(rcg_mi_e2k_merged,ias_prc_data,  how='left', left_on=['IAS_E2K'], right_on = ['PRC_ID_IAS_PRC'])
del rcg_mi_e2k_prcias_merged['PRC_ID_IAS_PRC']
rcg_mi_e2k_prc_merged = pd.merge(rcg_mi_e2k_prcias_merged, gaap_prc_data,  how='left', left_on=['GAAP_E2K'], right_on = ['PRC_ID_GAAP_PRC'])
del rcg_mi_e2k_prc_merged ['PRC_ID_GAAP_PRC']
rcg_mi_e2k_prc_merged.fillna('missing', inplace=True)
rcg_mi_e2k_prc_merged.head()

print(len(rcg_mi_e2k_prc_merged))

"""grit opening
"""

grit_e2k_data = pd.read_csv("GRIT_E2k_PCI_G2279.csv",skipinitialspace=True)
grit_e2k_data.fillna('missing', inplace=True)
grit_e2k_data = grit_e2k_data.add_suffix('_GRIT_E2k')
del_cols=['PUBLISH_DATE_GRIT_E2k','INVENTORY_DATE_GRIT_E2k','PRC_IAS_LIABILITY_GRIT_E2k','PRC_IAS_ASSET_GRIT_E2k','PRC_FR_LIABILITY_GRIT_E2k','PRC_FR_ASSET_GRIT_E2k','E2KPCI_LOCREP_CCY_AMT_GRIT_E2k','E2KPCI_LOCREP_CCY_AMT_CPT_GRIT_E2k','E2KPCI_GRP_AMT_GRIT_E2k']
for i in del_cols:
    del grit_e2k_data[i]



grit_e2k_data.head()

print(len(grit_e2k_data))

"""GRIT ADJ OPENING"""

grit_adj_data = pd.read_csv("GRIT_PRC_ADJ_2020.csv",skipinitialspace=True)
grit_adj_data.fillna('missing', inplace=True)
grit_adj_data = grit_adj_data.add_suffix('_GRIT_ADJ')
grit_adj_data.head()

print(len(grit_adj_data))

"""MERGING GRIT_E2K AND GRIT_ADJ"""

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

print(len(grit_e2k_data))

"""RCG,MI,E2K,PRC,GRIT_ADJ,GRIT_E2K JOIN"""

rcg_grit_e2k_join = pd.merge(rcg_mi_e2k_prc_merged, grit_e2k_data,  how='left', left_on=['E2KACCT_NBR_RCG','BUS_UNIT_RCG','DEPT_ID_RCG','CCY_CD_RCG','ALTACCT_RCG'], right_on = ['ACCOUNT_GRIT_E2k','BUSINESS_UNIT_GRIT_E2k','DEPTID_GRIT_E2k','CURRENCY_GRIT_E2k','ALTACCT_GRIT_E2k'])
del_cols=['ACCOUNT_GRIT_E2k','BUSINESS_UNIT_GRIT_E2k','DEPTID_GRIT_E2k','CURRENCY_GRIT_E2k','ALTACCT_GRIT_E2k','AFFILIATE_GRIT_E2k']
for i in del_cols:
    del rcg_grit_e2k_join [i]
rcg_grit_e2k_join.fillna('missing', inplace=True)
rcg_grit_e2k_join.head()

print(len(rcg_grit_e2k_join))

"""OPENING D3 DATA"""

grit_initial_data = pd.read_csv("D3.csv",skipinitialspace=True)
grit_initial_data.fillna('missing', inplace=True)
grit_initial_data = grit_initial_data.add_suffix('_GRIT_INITIAL')
del_cols=['PUBLISH_DATE_GRIT_INITIAL','INVENTORY_DATE_GRIT_INITIAL','PRC_IAS_LIABILITY_GRIT_INITIAL','PRC_IAS_ASSET_GRIT_INITIAL','PRC_FR_LIABILITY_GRIT_INITIAL','PRC_FR_ASSET_GRIT_INITIAL','E2KPCI_LOCREP_CCY_AMT_GRIT_INITIAL','E2KPCI_LOCREP_CCY_AMT_CPT_GRIT_INITIAL','E2KPCI_GRP_AMT_GRIT_INITIAL']
for i in del_cols:
    del grit_initial_data[i]


grit_initial_data=grit_initial_data.drop_duplicates()
grit_initial_data.head()

print(len(grit_initial_data))

#deleting non mi records
grit_initial_datas=grit_initial_data.copy()
for i in range(0,len(grit_initial_datas)):
    if grit_initial_data.loc[i,'SOURCE_GRIT_INITIAL']!='MI':
        grit_initial_data=grit_initial_data.drop(i)
grit_initial_data.fillna('missing', inplace=True)
grit_initial_data = grit_initial_data.reset_index(drop=True)

print(len(grit_initial_data))

"""MERGING RCG,MI,GRIT,E2K,PRC"""

rcg_grit_prc_mi_e2k_join = pd.merge(rcg_grit_e2k_join, grit_initial_data,  how='left', left_on=['E2KACCT_NBR_RCG','BUS_UNIT_RCG','DEPT_ID_RCG','CCY_CD_RCG','ALTACCT_RCG'], right_on = ['ACCOUNT_GRIT_INITIAL','BUSINESS_UNIT_GRIT_INITIAL','DEPTID_GRIT_INITIAL','CURRENCY_GRIT_INITIAL','ALTACCT_GRIT_INITIAL'])
del_cols=['ACCOUNT_GRIT_INITIAL','BUSINESS_UNIT_GRIT_INITIAL','DEPTID_GRIT_INITIAL','CURRENCY_GRIT_INITIAL','ALTACCT_GRIT_INITIAL','AFFILIATE_GRIT_INITIAL']
for i in del_cols:
    del rcg_grit_prc_mi_e2k_join[i]
rcg_grit_prc_mi_e2k_join.fillna('missing', inplace=True)
rcg_grit_prc_mi_e2k_join.head()

print(len(rcg_grit_prc_mi_e2k_join))

"""ORGIN_SOURCE_ID AND SOURCE_APPLICATION_ID COMBINATION"""

orgin_source=rcg_grit_prc_mi_e2k_join['ORIGIN_SOURCE_ID_MI'].tolist()
application_source=rcg_grit_prc_mi_e2k_join['SOURCE_APPLICATION_ID_MI'].tolist()
x=[]
for i in range(0,len(application_source)):
    if ['QTZ']==orgin_source[i] and application_source[i]==['QTZ']:
        x.append('QTZ')
    elif orgin_source[i]==['PEC'] and application_source[i]==['PEC']:
        x.append('PEC')
    elif orgin_source[i]==['PEC'] and application_source[i]==['QTZ']:
        x.append('PEC')
    elif orgin_source[i]==['PEC'] and (application_source[i]==['QTZ','PEC'] or application_source[i]==['PEC','QTZ']):
        x.append('PEC_and_QTZ')
    elif orgin_source[i]=='missing' and application_source[i]=='missing':
        x.append('missing')  
    elif orgin_source[i]=='missing' and application_source[i]!='missing':
        x.append(application_source[i])
    elif orgin_source[i]!='missing' and application_source[i]=='missing':
        x.append('missing')    
    else:
        y=orgin_source[i]
        y.extend(application_source[i])
        yy=list(set(y))
        q='_and_'.join(yy)
        x.append(q)
rcg_grit_prc_mi_e2k_join['SOURCE_APPN_IDS_MI']=x
rcg_grit_prc_mi_e2k_join.head()

print(len(rcg_grit_prc_mi_e2k_join['SOURCE_APPLICATION_ID_MI'].tolist()))

"""ADDING DIFFERENCE AMOUNT COLUMN"""

e2k_amount_list=rcg_grit_prc_mi_e2k_join['E2K_PCI_AGG_AMOUNT_GRIT_E2k'].tolist()
initial_amount_list=rcg_grit_prc_mi_e2k_join['E2K_PCI_AGG_AMOUNT_GRIT_INITIAL'].tolist()
diff=[]

for i in range(0,len(e2k_amount_list)):
    if e2k_amount_list[i]=='missing' or initial_amount_list[i]=='missing':
        diff.append('missing')
    else:
        diff_amount=float(e2k_amount_list[i])-float(initial_amount_list[i])
        diff.append(diff_amount)
rcg_grit_prc_mi_e2k_join['E2K_PCI_AGG_AMOUNT_DIFF_GRIT']=diff
rcg_grit_prc_mi_e2k_join.head()

"""ADDING PERCENTAGE COLUMN"""

diff_amount_list=rcg_grit_prc_mi_e2k_join['E2K_PCI_AGG_AMOUNT_DIFF_GRIT'].tolist()
initial_amount_list=rcg_grit_prc_mi_e2k_join['E2K_PCI_AGG_AMOUNT_GRIT_INITIAL'].tolist()
diff=[]

for i in range(0,len(diff_amount_list)):
    if initial_amount_list[i]=='missing':
        diff.append('missing')
    else:
        if float(diff_amount_list[i])==0:
            diff.append(0)
        else:
            diff_amount=float(diff_amount_list[i])/float(initial_amount_list[i])
            diff.append(diff_amount)
rcg_grit_prc_mi_e2k_join['E2K_PCI_AGG_AMOUNT_DIFF_PERCENTAGE_GRIT']=diff
rcg_grit_prc_mi_e2k_join.head()

"""DELETE COLUMN WITH SOURCE_APPN_IDS=[PEC,QTZ,TOP] and [PEC,QTZ,MPA]"""

delete_row1 = rcg_grit_prc_mi_e2k_join[rcg_grit_prc_mi_e2k_join['SOURCE_APPN_IDS_MI']=='QTZ_and_TOP_and_PEC'].index 
rcg_grit_prc_mi_e2k_join = rcg_grit_prc_mi_e2k_join.drop(delete_row1)
delete_row2 = rcg_grit_prc_mi_e2k_join[rcg_grit_prc_mi_e2k_join['SOURCE_APPN_IDS_MI']=='MPA_and_QTZ_and_PEC'].index 
rcg_grit_prc_mi_e2k_join = rcg_grit_prc_mi_e2k_join.drop(delete_row2)
rcg_grit_prc_mi_e2k_join = rcg_grit_prc_mi_e2k_join.reset_index(drop=True) 
rcg_grit_prc_mi_e2k_join.head()

print(len(rcg_grit_prc_mi_e2k_join))

print(list(rcg_grit_prc_mi_e2k_join.columns))

rcg_grit_prc_mi_e2k_join.to_csv('gritd2_d3_rcg_mi_e2k_prc_final_new2.csv')
