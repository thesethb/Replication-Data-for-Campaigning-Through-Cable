import pandas as pd
import time
import codecs

cycle_list = ['2020','2018','2016','2014','2012','2010']
for cycle in cycle_list:
    #with open('Donations/' + cycle + '/ccl.txt', 'r', encoding="ascii", errors="surrogateescape") as datafile:
        #datafile = str(datafile)
        #datafile = datafile.decode('unicode_escape').encode('utf-8')
    ccl = pd.read_csv('Donations/' + cycle + '/ccl.txt', sep = '|',header = None, names = ['CAND_ID','CAND_ELECTION_YR','FEC_ELECTION_YR','CMTE_ID','CMTE_TP','CMTE_DSGN','LINKAGE_ID'], usecols = ['CAND_ID', 'CMTE_ID'])


    ccl['CAND_ID'] = ccl['CAND_ID'].str[0]
    print(ccl)
    with open("Donations/indiv_header_file.csv") as myfile:
        head = [next(myfile) for x in range(1)]
    head = head[0].split(',')
    print(head)
    local_time = time.time()
    cols_list = ['CMTE_ID','TRANSACTION_DT','TRANSACTION_AMT','STATE','NAME','MEMO_TEXT']
    df = pd.read_csv('Donations/' + cycle + '/itcont.txt', sep = '|',header = None, names = head, usecols = cols_list)
    print(df.head())
    print((time.time() - local_time) / 60)
    df = pd.merge(df, ccl, how="left", on= 'CMTE_ID')
    df = df.loc[df['CAND_ID'] == 'H']
    df.to_csv('Donations/' + cycle + '/practice1.csv')
    print((time.time() - local_time) / 60)

#indData = ['Donations/2020/indiv_2020.csv']
#df = pd.read_csv(indData[0], index_col = 0)
#df = df.loc[0:100000,:]
#df.to_csv('practice.csv')