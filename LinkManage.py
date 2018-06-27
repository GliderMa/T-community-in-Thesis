import pandas as pd
Theme='CCA'
FolderPath='D:/CUHK Study/s2018/CurrentConnectionAnalysis/'
df1=pd.read_csv(FolderPath+Theme+'500+800.csv')     #after combined 500m+800m connection table
df2=pd.read_csv(FolderPath+'block_table.csv')       #raw block table

df2['IN_C']=None
df2['OU_C']=None
df2['IN-OUT']=None
df2['ALL_IN']=None

BlockTable_BLKID_Col=4
BlockTable_TID_Col=6

BlockNetwork_BLKID_Col=0
BlockNetwork_BLK_LINK_ID_Col=1

OutputFile=FolderPath+Theme+'_Tcommunity.csv'

# find Tcommunity ID for a block
def Get_Tcommunity_ID(BlockID,Block_Table,BLK_Col,TID_Col):
    for i in range(0,len(Block_Table),1):
        if BlockID==Block_Table.iat[i,BLK_Col]:
            TcoomunityID=Block_Table.iat[i,TID_Col]
    return TcoomunityID


#To calculate internal connection and external connection number for each block

def Check_Connection(block_ID,Block_Table,B_BLK_Col,B_TID_Col,Con_Table,C_BLK_Col,C_Link_BLK_Col):
    InCount=0
    OutCount=0
    T1=Get_Tcommunity_ID(block_ID,Block_Table,B_BLK_Col,B_TID_Col)
    for i in range(0,len(Con_Table),1):
        if block_ID==Con_Table.iat[i,C_BLK_Col]:
            T2=Get_Tcommunity_ID(Con_Table.iat[i,C_Link_BLK_Col],Block_Table,B_BLK_Col,B_TID_Col)
            if T1==T2:
                InCount=InCount+1
            else:
                OutCount=OutCount+1
    Indicator=InCount-OutCount
    result=[InCount,OutCount,Indicator]
    return result

#get number of blocks in each community in a dictionary
def get_amount_Tcommunity(Block_Table,TID_Col):
    tempset=set()
    T_IDstore=[]

    outputdict={}
    for i in range(0,len(Block_Table),1):
        tempset.add(Block_Table.iat[i,TID_Col])
    for item in tempset:
        T_IDstore.append(item)
        T_IDstore.sort()
    for j in T_IDstore:
        count=0
        for k in range(0,len(Block_Table),1):
            if j == Block_Table.iat[k,TID_Col]:
                count=count+1
        outputdict[j]=count
    return outputdict



TcommNumber=get_amount_Tcommunity(df2,BlockTable_TID_Col)

#also check internal coverage
for i in range(0,len(df2),1):
    blockID=df2.iat[i,BlockTable_BLKID_Col]
    result=Check_Connection(blockID,df2,BlockTable_BLKID_Col,BlockTable_TID_Col,df1,BlockNetwork_BLKID_Col,BlockNetwork_BLK_LINK_ID_Col)
    inc=result[0]
    outc=result[1]
    calculation=result[2]
    check2=inc/(TcommNumber[df2.iat[i,BlockTable_TID_Col]]-1)


    df2.iat[i, df2.columns.get_loc('IN_C')]=inc
    df2.iat[i, df2.columns.get_loc('OU_C')] = outc
    df2.iat[i, df2.columns.get_loc('IN-OUT')] = calculation
    df2.iat[i, df2.columns.get_loc('ALL_IN')] = check2

            
df2.to_csv(OutputFile)



