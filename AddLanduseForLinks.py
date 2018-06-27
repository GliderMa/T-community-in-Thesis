import pandas as pd
df1=pd.read_csv('block_network.csv')
df2=pd.read_csv('block_table.csv')



#add columns for csv
df1['S_TYPE']=None
df1['T_TYPE']=None
df1['Special']=None #to determine which landuse links need further operation

specific_operation={('C','R2'):1,('C','GIC'):1,('GIC','R2'):1,('GIC','GIC'):1,('R2','R2'):1,('R2','GIC'):1}

BlockTable_BLKID_Col=4
BlockTable_L_Col=1

BlockNetwork_BLKID_Col=0
BlockNetwork_BLK_LINK_ID_Col=1

OutputLinkTable='LinkswithLanduse.csv'

def GetDict_Landuse(Block_Table,Con_Table,B_BLK_Col,B_Land_Col,C_BLK_Col):
    tempset = set()
    BLKinC_Table = []

    Landuse_dict = {}
    for i in range(0, len(Con_Table), 1):
        tempset.add(Con_Table.iat[i, C_BLK_Col])
    for item in tempset:
        BLKinC_Table.append(item)
        BLKinC_Table.sort()
    for j in BLKinC_Table:
        for k in range(0, len(Block_Table), 1):
            if j == Block_Table.iat[k, B_BLK_Col]:
                landuse=Block_Table.iat[k, B_Land_Col]
                Landuse_dict[j]=landuse

    return Landuse_dict

LanduseDict=GetDict_Landuse(df2,df1,BlockTable_BLKID_Col,BlockTable_L_Col,BlockNetwork_BLKID_Col)

for i in range(0,len(df1),1):
    S_TYPE=LanduseDict[df1.iat[i,BlockNetwork_BLKID_Col]]
    T_TYPE = LanduseDict[df1.iat[i,BlockNetwork_BLK_LINK_ID_Col]]
    df1.iat[i,df1.columns.get_loc('S_TYPE')]=S_TYPE
    df1.iat[i, df1.columns.get_loc('T_TYPE')]=T_TYPE
    try:
        indicator=specific_operation[S_TYPE,T_TYPE]
    except:
        indicator =0
    df1.iat[i, df1.columns.get_loc('Special')] = indicator


df1.to_csv(OutputLinkTable)

df=pd.read_csv(OutputLinkTable)
df=df[df.Special==1]
df.to_csv('test.csv')

