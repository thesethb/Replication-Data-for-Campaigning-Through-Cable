import pandas as pd
import os

cycles = [2020,2018,2016,2014,2012,2010]
for cycle in cycles:
    directory = 'Data/' + str(cycle) + '/trends_files/'
    results = os.listdir(directory)
    result = pd.DataFrame()
    for r in results:
        result = pd.concat([result,pd.read_csv(directory + r)])
    print(result)

    directory = 'Data/' + str(cycle) + '/trends_words/'
    results = os.listdir(directory)
    wordLists = pd.DataFrame()
    for r in results:
        wordLists = pd.concat([wordLists,pd.read_csv(directory + r)])
    print(wordLists)
    #Fixing Formatting
    words = wordLists['names']
    wordNew = []
    for word in words:
        if word[0] == '[':
            word = str(word)[2:len(word)-2]
        wordNew.append(word)
    wordLists['names'] = wordNew
    print(wordLists)

    cols = list(result.columns)

    trendDF = pd.melt(result, id_vars='date', value_vars=cols.remove('date'),
                          var_name='names', value_name='search_results')
    trendDF['search_results'] = trendDF['search_results'].fillna(0)
    trendDF.to_csv('trend1.csv')
    names1 = trendDF['names'].tolist()
    for i in range(len(names1)):
        name = names1[i].split('.')
        names1[i] = name[0]
    trendDF['names'] = names1
    trendDF = trendDF.groupby(['date','names'], as_index=False)['search_results'].sum()
    print('\ntrial1:\n')
    print(trendDF)
    print(wordLists)
    trendDF.to_csv('trends2.csv')
    trendDF = pd.merge(trendDF,wordLists, on='names')
    print(trendDF)
    trendDF.to_csv('trendDF.csv')

    #merging candidate searches into main database
    df = pd.read_csv('Data/' + str(cycle) + '/candidate_donation_appearance.csv')
    print(df)
    df = pd.merge( df,trendDF,how='inner',on = ['name_snyder','date'])
    print(df)

    df.to_csv('Data/' + str(cycle) + '/final_data.csv')
    """
    #The below was originally entered to enable the estimation of candidate averages based on whether they made an appearance.
    
    #getting cand and date averages
    candAvg = df.groupby('name_snyder')[["contribution_receipt_amount",'inState_contributionAmount','outState_contributionAmount']].mean()
    candAvg.columns = ['candAvgAmount','candAvgInState','candAvgOutState']
    print(candAvg)
    dateAvg = df.groupby('date')[["contribution_receipt_amount",'inState_contributionAmount','outState_contributionAmount']].mean()
    print(dateAvg)
    dateAvg.columns = ['dateAvgAmount','dateAvgInState','dateAvgOutState']
    df = pd.merge(df,candAvg,how='left',on = 'name_snyder')
    df = pd.merge(df,dateAvg,how='left',on = 'date')
    print(df)
    
    #getting averages searches for previous five days
    cands = df.drop_duplicates('name_snyder')
    searchLastFive = 0
    for i in cands['name_snyder']:
        working = df.loc[df['name_snyder'] == i]
        working = working.reset_index()
        searchTab = []
        #print(working)
        for s in range(5,len(working)):
            sum = 0
            for i in range(5):
                sum += working['search_results'][s-i]
            searchTab.append(sum/5)
        working = working[5:]
        working['searches_five_day'] = searchTab
        try:
            if searchLastFive == 0:
                searchLastFive = working
            else:
                searchLastFive.append(working)
        except:
            searchLastFive.append(working)
    print(searchLastFive)
    df.to_csv('final_data.csv')
    """
    #df2 = df.groupby(['name_snyder'])[''].mean()
    #df2 = df2.loc[df2['appearance_count'] > 0 , ['count2']] = 1
    #df2 = df2.groupby('count2')['contribution_receipt_amount'].mean()
    #print(df2)