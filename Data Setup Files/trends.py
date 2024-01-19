from pytrends.request import TrendReq
from pytrends import dailydata
import pytrends
import pandas as pd
import time
import os
import random

cycle = 2010

def turn_back_date(date, days):

     year = int(date[0:4])
     month = int(date[5:7])
     day = int(date[8:10])
     if year % 4 == 0:
          days_per = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
     else:
          days_per = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
     if day > days:
          day = day - days
     elif month >= 2:
          month = month - 1
          day = days_per[month] - days + day
     else:
          year = year-1
          month = 12
          day = days_per[month] - days + day - 1
     if month < 10:
          month = '0' + str(month)
     if day < 10:
          day = '0' + str(day)
     return str(year) + '-' + str(month) + '-' + str(day)
#print(turn_back_date('2018-05-02',3))

df = pd.read_csv('Data/' + str(cycle) + '/candidate_donation_appearance.csv')
cands = df['name_snyder'].drop_duplicates()
#print(cands)
cands = cands.to_list()
#print(cands)

startTime = time.time()
pytrend = TrendReq(hl='en-UZ', tz=360)#, timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=2, backoff_factor=0.1, requests_args={'verify':False})

try:
     #Finds all the names that havent already been analyzed to make new list
     directory = 'Data/' + str(cycle) + '/trends_words/'
     results = os.listdir(directory)
     wordLists = pd.DataFrame()
     for r in results:
         wordLists = pd.concat([wordLists,pd.read_csv(directory + r)])
     print(wordLists)
     #Fixing Formatting
     finishedCandidates = wordLists['name_snyder'].to_list()
     print(len(finishedCandidates))
     cands2 = cands.copy()
     for name in cands2:
          print(name)
          if name in finishedCandidates:
               print('hahaha')
               cands.remove(name)
               print(len(cands))
     print(len(cands))
except:
     pass


wordList = [[],[]]

dataset = []
i = 0
print(len(cands))
random.shuffle(cands)
#startnum = 561 #Used to resume if run is interrupted by google (ex: if you make it through 15 cands set to "15")
for j in range(len(cands)):
     x = cands[j]
     attempt_count = 0
     if i >= 0:
          words = x.split()
          word = ''
          if ',' in words[1]:
               words[0] += ' ' + words[1].replace(',','')
               words.remove(words[1])
          else:
               for j in range(len(words)-1,0,-1):
                    if ')' in words[j]:
                         w = words[j].replace('(','')
                         w = w.replace(')','')
                         w = w.replace(',','')
                         word += w + ' '
                         break
                    elif j ==1:
                         if '.' not in words[1]:
                              word += words[1].replace(',','') + ' '
                         else:
                              word += words[2].replace(',','') + ' '
          words[0] = words[0].replace(',','')
          word += words[0]
          word = [word]
          print(word)
          #date = turn_back_date(df['date'][x], 10) + ' ' + turn_back_date(df['date'][x], 1)
          #print(date)
          z = 0
          n = 1
          while z == 0:

               try:

                    ind = 0
                    while ind == 0:
                         print(word)

                         pytrend.build_payload(
                              kw_list=word,
                              cat=0,
                              timeframe= str(cycle) + '-01-01 ' + str(cycle) +  '-12-31',
                              geo='US')
                         data = pytrend.interest_over_time()
                         #data = pytrend.get_historical_interest(word, year_start=cycle-1, month_start=1, day_start=1,
                                                                 #hour_start=0, year_end=cycle, month_end=12, day_end=31, hour_end=23, cat=0, geo='', gprop='')
                         print(data)
                         time.sleep(1)
                         if not data.empty:
                              data1 = []
                              for chunk in [str(cycle-1) + '-01-01 ' + str(cycle-1) +  '-06-30', str(cycle-1) + '-07-01 ' + str(cycle-1) +  '-12-31',
                                            str(cycle) + '-01-01 ' + str(cycle) +  '-06-30',str(cycle) + '-07-01 ' + str(cycle) +  '-12-31']:
                                   pytrend.build_payload(
                                        kw_list=word,
                                        cat=0,
                                        timeframe= chunk,
                                        geo='US')
                                   data = pytrend.interest_over_time()
                                   try:
                                        data = data.drop(labels=['isPartial'], axis='columns')
                                   except:
                                        pass

                                   dataset.append(data)
                                   print(data)
                                   time.sleep(2)
                              #data.to_csv('trendstrial1')
                              #data1.to_csv('trendstrial2')
                              #dataset[word[0]] = data1
                              print(dataset)
                              ind = 1
                              z = 1
                              wordList[0].append(word[0])
                              wordList[1].append(x)
                              time.sleep(4)


                         word = [words[n].replace(',','') + ' ' + words[0].replace(',','')]
                         n += 1
               except Exception as inst:
                    print(type(inst))
                    print(inst.args)
                    print(inst)
                    #n += 1
                    #word = words[n] + ' ' + words[0]
                    time.sleep(5)
                    if type(inst) == IndexError:
                         z = 1
                         print("\n\n\n\n\n\n\n\nTHIS\nIS\nTHE\nONE\nTHAT\nIS\nBROKEN\n\nSO FIX IT\n\n\n\n\n\n\n\n")
                    attempt_count += 1
                    if attempt_count > 5:
                         z = 1

     i += 1
     print(i)
     print(j)
     if attempt_count > 5:
          break
#keywords = [df['Cand_Name'][x]]
#print(keywords)
#date = turn_back_date(df['date'][x],1) + ' ' + turn_back_date(df['date'][x],4)
#print(date)
#pytrend.build_payload(
#kw_list=keywords,

result = pd.concat(dataset, axis=1)
result.to_csv('Data/' + str(cycle) + '/trends_files/search_trends_total' + str(cands[int(len(cands) / 2)]) + '.csv')

wordLists = pd.DataFrame(list(zip(wordList[0], wordList[1])), columns=['names','name_snyder'])
wordLists.to_csv('Data/' + str(cycle) + '/trends_words/word_list' + str(cands[int(len(cands) / 2)]) + '.csv')

executionTime = (time.time() - startTime)
print('Execution time in sec.: ' + str(executionTime))