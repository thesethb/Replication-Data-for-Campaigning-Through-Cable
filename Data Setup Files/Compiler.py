import pandas as pd
import os

cycles = [2020,2018,2016,2014,2012,2010]
df = pd.DataFrame()

for cycle in cycles:
    data = pd.read_csv('Data/' + str(cycle) + '/final_data.csv')
    df = df.append(data)
    print(f"The sum of primetime is {df['primetime'].sum()}")
print(df)
print(df.columns)
df = df[['date','contribution_receipt_amount','cont_num','CAND_NAME',
       'inState_contributionAmount', 'inState_cont_num','outState_contributionAmount','outState_cont_num','year', 'state', 'office',
       'dist', 'type', 'nextup', 'party', 'party_formal', 'name_snyder', 'inc',
       'candidatevotes', 'totalvotes', 'won', 'cnn', 'fox', 'msnbc','cnn_primetime','fox_primetime','msnbc_primetime',
       'appearance_count1', 'appearance_count','primetime1','primetime','tucker','search_results']]
df=df.fillna({'appearance_count1':0,'primetime1':0,'primetime':0,'search_results':0,'tucker':0,'cnn_primetime':0,
              'fox_primetime':0,'msnbc_primetime':0})
print(df['primetime'])
presidencies = {'Donald Trump' : 'R', 'Barack Obama' : 'D', 'George W. Bush' : 'R'}


#Adding approval rating
xl_file = pd.ExcelFile('American Presidency Project - Approval Ratings for POTUS.xlsx')
sheet_names = xl_file.sheet_names
print(sheet_names)

#Cleaning and Storing data for each sheet
bigDF = pd.DataFrame()
for x in sheet_names:
    if x in presidencies.keys():
        temp_df = pd.read_excel(xl_file,sheet_name=x)
        temp_df['president'] = x
        temp_df['party'] = presidencies[x]
        bigDF = bigDF.append(temp_df)
print(bigDF)
bigDF = bigDF.reset_index()
startDates = bigDF['Start Date'].to_list()
endDates = bigDF['End Date'].to_list()
dates = df['date'].unique()
print(dates)
approval_rateDF = pd.DataFrame()
for date in dates:
    for i in range(1,len(startDates)):
        if date >= str(endDates[i])[0:10] and date <= str(endDates[i - 1])[0:10]:
            print(bigDF.loc[i,['Approving', 'Disapproving','president','party']])
            approval_rateDF = approval_rateDF.append(bigDF.loc[i,['Approving', 'Disapproving','president','party']])
            print(date)
            print(str(startDates[i])[0:10])
            print(str(endDates[i])[0:10])
            break
print(approval_rateDF)
approval_rateDF['date'] = dates
print(approval_rateDF)
print(len(df))
df = pd.merge(df, approval_rateDF, on = 'date')
print(len(df))
print(df)
df.to_csv('house_appearances_fundraising.csv')