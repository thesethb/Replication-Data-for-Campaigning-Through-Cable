import pandas as pd
cycle_list = ['2020','2018','2016','2014','2012','2010']
for cycle in cycle_list:
    cycle = int(cycle)
    txt = open('candidates_2006-2020.tab', 'r')
    candidateDF = pd.read_csv(txt, sep='	', dtype = {'year' : int})
    print(candidateDF)
    print(candidateDF.keys())
    candidateDF = candidateDF.loc[(candidateDF['year'] == cycle) & (candidateDF['office'] == 'H') &
                                  ((candidateDF['party'] == 'D') | (candidateDF['party'] == 'R'))]
    print(candidateDF)
    #candidateDF.to_csv('candidateData.csv')

    try:
        candidateDF = pd.read_csv('Data/' + str(cycle) + '/nameCheck.csv')
    except:
        pass
    candidateDF = candidateDF.loc[(candidateDF['type'] == 'G')]

    df = pd.read_csv('Data/' + str(cycle)+ '/donationData.csv', dtype = {'contribution_receipt_date' : str})
    names = df['CAND_NAME'].unique()
    try:
        nameDF = pd.read_csv('Data/' + str(cycle) + '/nameCheck1.csv')
        names = nameDF[0]
    except:
        pass
    print(names)
    names = pd.Series(names)
    names.to_csv('Data/' + str(cycle)+ '/nameCheck1.csv')
    names = names.to_list()
    names1 = candidateDF['name_snyder'].to_list()
    names_new = []
    for name in names1:
        indx = names1.index(name)
        n = str(name)
        n = n.replace('(','')
        n = n.replace(')','')
        n = n.replace(',','')
        n = n.split(' ')
        #print(name)
        indicator = 0
        for i in range(len(names)):
            namie = str(names[i]).replace(',','')
            namie = namie.split(' ')
            last = namie[0]
            #print(namie)
            if last == n[0]:
                #first = namie[1].replace(' ','')
                #print(names[i])
                for j in range(1,len(n)):
                    for k in range(1,len(namie)):
                        first = namie[k].replace(' ','')
                        if n[j].replace(' ','') == first:
                            print(names[i])
                            #names_i = names[i].replace('-','') Before I run search history again, remove dashes from names
                            #names_new.append(names_i)
                            #n = str(name).replace('-','')
                            #names1['indx'] = n

                            names_new.append(names[i])
                            names.remove(names[i])
                            indicator = 1
                            break
                    if indicator == 1:
                        break
            if indicator == 1:
                break
        if indicator == 0:
            names_new.append('INCORRECT')




    #candidateDF['CAND_NAME'] = names_new
    #df = pd.merge(df,candidateDF,how="left", on='CAND_NAME')

    #print(df)
    #df.to_csv('candidate_donation.csv')

    candidateDF['CAND_NAME'] = names_new
    candidateDF1 = candidateDF.loc[candidateDF['year'] == cycle]
    candidateDF1.to_csv('Data/' + str(cycle) + '/nameCheck.csv')
    df = pd.merge(df,candidateDF,how="inner", on='CAND_NAME')
    #df = df.drop_duplicates(['CAND_NAME'])

    """
    #formatting dates manually, moved to previous file
    datelist = []
    for d in df['date']:
        d = str(d)
        if len(d) == 9:
            d = d[3:7] + '-' + d[1:3] + '-0' + d[0:1]
        elif len(d) == 10:
            d = d[4:8] + '-' + d[2:4] + '-' + d[0:2]
        else:
            print(d)
            d = d[4:8] + '-' + d[2:4] + '-' + d[0:2]
        datelist.append(d)
    df['contribution_receipt_date'] = datelist
    
    df['fYear'] = df['contribution_receipt_date'].str[0:4]
    df['fYear'] = pd.to_numeric(df['fYear'])
    df = df.loc[(df['fYear'] == cycle )| (df['fYear'] == cycle - 1) ]
    df = df.sort_values(['committee_id','contribution_receipt_date'])
    """

    print(df)
    df.to_csv('Data/' + str(cycle) + '/candidate_donation.csv')

