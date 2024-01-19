import pandas as pd
pd.set_option('display.max_columns', None)
cycle_list = ['2020','2018','2016','2014','2012','2010']
for cycle in cycle_list:
    cycle = int(cycle)
    printFile = 'Data/' + str(cycle) + '/donationData.csv'
    #candComm = 'candComm.csv'
    #indData = ['practice.csv']
    indData = ['Donations/' + str(cycle) + '/practice1.csv']
    candData = 'Donations/' + str(cycle) + '/cn.txt'
    commData = 'Donations/' + str(cycle) + '/cm.txt'
    cols_list = ['committee_id','NAME','contributor_state','contribution_receipt_date','contribution_receipt_amount','MEMO_TEXT','H']
    df = pd.read_csv(indData[0], index_col = 0, dtype = {'TRANSACTION_DT' : str, 'CMTE_ID' : str})
    df.TRANSACTION_AMT = pd.to_numeric(df.TRANSACTION_AMT,errors='coerce')
    df.columns = cols_list
    df = df.astype({'contribution_receipt_date': str})
    print(df)

    #I make contribution number var
    df['cont_num'] = 1
    df['NAME'] = df['NAME'].fillna('n')
    unitimized = df.loc[df['NAME'].str.contains('unitemized',case=False)]
    print(unitimized.index.values.tolist())
    for id in unitimized.index.values.tolist():
        df['cont_num'][id] = int(df['contribution_receipt_amount'][id] / 200) + 1

    df['MEMO_TEXT'] = df['MEMO_TEXT'].fillna('n')
    unitimized = df.loc[df['MEMO_TEXT'].str.contains('unitemized', case=False)]
    print(unitimized.index.values.tolist())
    for id in unitimized.index.values.tolist():
        df['cont_num'][id] = int(df['contribution_receipt_amount'][id] / 200) + 1
    print(df['cont_num'])

    #For combining multiple datasets
    #for i in range(1,len(indData)):
    #    df = df.append(pd.read_csv(indData[i], usecols=cols_list))
    #print(df)

    print(df['contribution_receipt_date'].max())

    #formatting dates manually
    datelist = []
    for d in df['contribution_receipt_date']:
        d = str(d)
        if 'n' in d:
            d = '0000-00-00'
        elif len(d) == 7:
            d = d[3:7]+ '-0' + d[0:1] + '-' + d[1:3]
        elif len(d) == 8:
            d = d[4:8]+ '-' + d[0:2] + '-' + d[2:4]
        elif len(d) == 9:
            d = d[3:7]+ '-0' + d[0:1] + '-' + d[1:3]
        elif len(d) == 10:
            d = d[4:8]+ '-' + d[0:2] + '-' + d[2:4]
        else:
            print(d)
            d = d[4:8] + '-' + d[0:2] + '-' + d[2:4]
        datelist.append(d)
    df['contribution_receipt_date'] = datelist

    df['fYear'] = df['contribution_receipt_date'].str[0:4]
    df['fYear'] = pd.to_numeric(df['fYear'])
    df = df.loc[(df['fYear'] == cycle )| (df['fYear'] == cycle - 1) ]

    print(df)
    print('made it to step 1')

    #####filtering by state######
    stateGroup = df

    #Loading Comm Data
    with open("Donations/cm_header_file.csv") as myfile:
        head = [next(myfile) for x in range(1)]
    head = head[0].split(',')
    df2 = pd.read_csv(commData, sep = '|',header = None, names = head)
    df2 = df2.astype({'CAND_ID' : str, 'CMTE_ID' : str})


    data = [df2['CAND_ID'],df2['CMTE_ID']]
    headers = ["CAND_ID", "CMTE_ID"]
    commCand = pd.concat(data, axis=1, keys=headers)
    stateGroup = pd.merge(stateGroup,commCand,how="left", left_on='committee_id', right_on='CMTE_ID')
    print(commCand)
    print(stateGroup)
    print('made it to step 2')

    #Loading Cand Data
    with open("Donations/cn_header_file.csv") as myfile:
        head1 = [next(myfile) for x in range(1)]
    head1 = head1[0].split(',')
    df3 = pd.read_csv(candData, sep = '|',header = None, names = head1)
    df3 = df3.astype({'CAND_ID' : str})

    print('made it to step 3')

    data = [df3['CAND_ID'],df3['CAND_NAME'],df3['CAND_ST']]
    headers = ["CAND_ID", "CAND_NAME","CAND_ST"]
    commCand = pd.concat(data, axis=1, keys=headers)
    #print(commCand)
    stateGroup = pd.merge(stateGroup,commCand,how="inner", on='CAND_ID')
    inState = stateGroup.loc[(stateGroup['CAND_ST'] == stateGroup['contributor_state'])]
    print(inState)
    inState = inState.groupby(['CAND_NAME','contribution_receipt_date'], as_index = False)[['contribution_receipt_amount','cont_num']].sum()
    data = [inState['CAND_NAME'],inState['contribution_receipt_date'],inState['contribution_receipt_amount'], inState['cont_num']]
    headers = ["CAND_NAME", "contribution_receipt_date","inState_contributionAmount","inState_cont_num"]
    inState = pd.concat(data, axis=1, keys=headers)
    print(inState)

    outState = stateGroup.loc[(stateGroup['CAND_ST'] != stateGroup['contributor_state']) & (stateGroup['contributor_state'] != '')]
    outState = outState.groupby(['CAND_NAME','contribution_receipt_date'], as_index = False)[['contribution_receipt_amount','cont_num']].sum()
    data = [outState['CAND_NAME'],outState['contribution_receipt_date'],outState['contribution_receipt_amount'], outState['cont_num']]
    headers = ["CAND_NAME", "contribution_receipt_date","outState_contributionAmount",'outState_cont_num']
    outState = pd.concat(data, axis=1, keys=headers)
    print(outState)

    df2 = pd.read_csv(commData, sep='|', header=None, names=head)
    df2 = df2.astype({'CAND_ID': str})
    data = [df2['CAND_ID'], df2['CMTE_ID']]
    headers = ["CAND_ID", "CMTE_ID"]
    comm = pd.concat(data, axis=1, keys=headers)
    df3 = pd.read_csv(candData, sep='|', header=None, names=head1)
    df3 = df3.astype({'CAND_ID': str})
    data = [df3['CAND_ID'], df3['CAND_NAME']]
    headers = ["CAND_ID", "CAND_NAME"]
    cand = pd.concat(data, axis=1, keys=headers)
    CommCand = pd.merge(comm, cand, how="inner", on='CAND_ID')
    df = pd.merge(df, CommCand, how="left", left_on='committee_id', right_on='CMTE_ID')
    print(df)
    df = df.dropna(subset = ['CAND_ID'])
    #Getting data grouped by candidate and date

    df = df.groupby(['CAND_NAME','contribution_receipt_date'], as_index = False)[['contribution_receipt_amount','cont_num']].sum()
    #print(df)
    df.to_csv('output1')

    #Making a blank dataframe with every date every cand_id
    cand_names = df['CAND_NAME'].unique()
    dates = df['contribution_receipt_date'].unique()

    comm_str = 'CAND_NAME,contribution_receipt_date,date'
    print(len(cand_names))
    n = -1
    for j in cand_names:
        n += 1
        print(n)
        for d in dates:
            #if d[0:4] == '2018':
                #date = d[0:10]
            #else:
                #date = '2018-' + d[3:5] + '-' + d[0:2]
            comm_str += '\n'+ '"' + j + '"' + ',' + d + ','+d
    from io import StringIO
    comm_DF = pd.read_csv(StringIO(comm_str), dtype= {'contribution_receipt_date' : str})

    df = pd.merge(comm_DF,df,how="left", on=['CAND_NAME','contribution_receipt_date'])
    df = df.sort_values(['CAND_NAME','date'])
    df['contribution_receipt_amount'] = df['contribution_receipt_amount'].fillna(0)
    df['cont_num'] = df['cont_num'].fillna(0)
    df.to_csv('Data/' + str(cycle) + '/t1.csv')

    #This block was moved to the top
    #df2 = pd.read_csv(commData, sep = '|',header = None, names = head)
    #df2 = df2.astype({'CAND_ID' : str})
    #data = [df2['CAND_ID'],df2['CMTE_ID']]
    #headers = ["CAND_ID", "CMTE_ID"]
    #commCand = pd.concat(data, axis=1, keys=headers)
    #df = pd.merge(df,commCand,how="left", on='CAND_ID')
    #df3 = pd.read_csv(candData, sep = '|',header = None, names = head1)
    #df3 = df3.astype({'CAND_ID' : str})
    #data = [df3['CAND_ID'],df3['CAND_NAME']]
    #headers = ["CAND_ID", "CAND_NAME"]
    #commCand = pd.concat(data, axis=1, keys=headers)
    #df = pd.merge(df,commCand,how="inner", on='CAND_ID')
    #print(df)

    df.to_csv('Data/' + str(cycle) + '/donationDataDup.csv')

    #merging in and out-state
    df = pd.merge(df,inState,how="left", on=['CAND_NAME','contribution_receipt_date'])
    df = pd.merge(df,outState,how="left", on=['CAND_NAME','contribution_receipt_date'])
    df['inState_contributionAmount'] = df['inState_contributionAmount'].fillna(0)
    df['outState_contributionAmount'] = df['outState_contributionAmount'].fillna(0)
    df['inState_cont_num'] = df['inState_cont_num'].fillna(0)
    df['outState_cont_num'] = df['outState_cont_num'].fillna(0)

    df = pd.merge(df,df3[['CAND_NAME','CAND_ICI']], on = ['CAND_NAME'])

    print(df)


    df.to_csv(printFile)
