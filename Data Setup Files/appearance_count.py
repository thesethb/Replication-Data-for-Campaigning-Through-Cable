import pandas as pd
cycle_list = ['2020','2018','2016','2014','2012','2010']
for cycle in cycle_list:
    cycle = int(cycle)
    #Setting up skeleton lists
    candidateDF = pd.read_csv('Data/' + str(cycle) + '/nameCheck.csv')
    df = pd.read_csv('Data/' + str(cycle) + '/candidate_donation.csv')
    dates1 = df['date']
    dates = []
    num = []
    j = ''
    n = 0
    while j != dates1[0]:
        num.append(0)
        dates.append(dates1[n])
        n += 1
        j = dates1[n]
    print(dates)
    names1 = candidateDF['name_snyder']
    names_new = []
    bigList = []
    nameList = []
    for name in names1:
        n = str(name).lower()
        n = n.replace('(','')
        n = n.replace(')','')
        n = n.replace(',','')
        n = n.split(' ')
        nameList.append(n)
    print(nameList)
    print(bigList)

    #pulling info from guestList
    fileList = ['guestList','foxGuestList','msnbcGuestList']
    stationList = ['cnn','fox','msnbc']
    for s in range(3):
        guestList = pd.read_csv(fileList[s] + '.csv')
        dateList = guestList['Date']
        print(len(dates))
        guests = guestList['Guest']
        print(len(guests))

        datesNameList = [[],[],[],[],[]]
        dateRef = {"January":"01",'February':'02','March':'03','April':'04','May':'05','June':'06'
                   ,'July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}

        for index,group in guests.iteritems():
            group = str(group).lower()
            group = group.split(';')
            for name in group:
                #name = name.lower()
                name1 = name.split(' ')
                last = name1[len(name1)-1]
                for nIndex in range(len(nameList)):
                    #print(n[0] + ',' + last)
                    n = nameList[nIndex]
                    if n[0] == last:
                        for i in range(1,len(n)):
                            for j in range(len(name1)-1):
                                if n[i] == name1[j]:
                                    #print(names1[nIndex] + "," + str(n) +","+ dateList[index] )
                                    d = dateList[index].split()
                                    if len(d[1]) == 1:
                                        d[1] = '0' + d[1]
                                    d = d[2] + '-' + dateRef[d[0]] + '-' + d[1]

                                    datesNameList[0].append(names1[nIndex])
                                    datesNameList[1].append(d)
                                    datesNameList[2].append(1)
                                    datesNameList[3].append(guestList['Primetime'][index])
                                    if stationList[s] == 'fox':
                                        datesNameList[4].append(guestList['Tucker'][index])
                                        #if guestList['Tucker'][index] == 1:
                                            #print(guestList['Primetime'][index])
                                            #print(index)
                                            #print(names1[nIndex])
                                    else:
                                        datesNameList[4].append(0)

        print(sum(datesNameList[3]))
        appearancesDF = pd.DataFrame(list(zip(datesNameList[0], datesNameList[1],datesNameList[2],
                                              datesNameList[3],datesNameList[4])),
                       columns =['name_snyder','date',stationList[s],stationList[s] + '_' + 'primetime','tucker' + str(s)])
        appearancesDF = appearancesDF.groupby(['date','name_snyder'])[stationList[s],stationList[s] + '_' + 'primetime','tucker' + str(s)].sum()
        #print(appearancesDF)

        print(appearancesDF)
        appearancesDF.to_csv('Data/' + str(cycle) + '/' + stationList[s] + 'appearances.csv')


        df = pd.merge(df,appearancesDF,how="left", on=['name_snyder','date'])
        print(df)
        print(f"The sum of primetime is {df[stationList[s] + '_' + 'primetime'].sum()}")
        df[stationList[s]] = df[stationList[s]].fillna(0)
        df[stationList[s] + '_' + 'primetime'] = df[stationList[s] + '_' + 'primetime'].fillna(0)
        df['tucker' + str(s)] = df['tucker' + str(s)].fillna(0)
        print(df)
        #df.to_csv('Data/' + str(cycle) + '/candidate_donation_appearance.csv')
    df.loc[df['cnn'] >= 1, 'cnn'] = 1
    df.loc[df['fox'] >= 1, 'fox'] = 1
    df.loc[df['msnbc'] >= 1, 'msnbc'] = 1
    df['appearance_count1'] = df['fox'] + df['cnn'] + df['msnbc']
    df.loc[df['appearance_count1'] >= 1, 'appearance_count'] = 1
    df['appearance_count'] = df['appearance_count'].fillna(0)

    df.loc[df['cnn_primetime'] >= 1, 'cnn_primetime'] = 1
    df.loc[df['fox_primetime'] >= 1, 'fox_primetime'] = 1
    df.loc[df['msnbc_primetime'] >= 1, 'msnbc_primetime'] = 1
    df['primetime1'] = df['fox_primetime'] + df['cnn_primetime'] + df['msnbc_primetime']
    df.loc[df['primetime1'] >= 1, 'primetime'] = 1
    df['primetime'] = df['primetime'].fillna(0)
    print(f"The sum of primetime is {df['primetime'].sum()}")

    df['tucker'] = df['tucker1']
    df.loc[df['tucker'] >= 1, 'tucker'] = 1
    print(f"The sum of tucker is {df['tucker'].sum()} or {df['tucker1'].sum()}")
    df = df.drop(['tucker0','tucker1','tucker2'], axis=1)


    df.to_csv('Data/' + str(cycle) + '/candidate_donation_appearance.csv')

    df2 = df.groupby(['name_snyder'])[['appearance_count1','primetime1','tucker','cnn','fox','msnbc',
        'cnn_primetime','fox_primetime','msnbc_primetime']].sum()
    df2.to_csv('Data/' + str(cycle) + '/candidateAppearanceCounts.csv')
