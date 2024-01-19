#with open("./Transcripts/1/_Wall Street Journal__ Trump Lawyers Hope to Decide By May 17 for Trump's Possible Sit-Down with Rob", 'r') as file:
 #   text = file.read()
#print(text)

import os


import PyPDF2

guestList = open('guestList.csv','w')
folderList = ['2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009']
guestList.write('Date,Guest,Primetime,Start_Hour,Program\n')
for f in folderList:
    fileList = []
    directory = r'./CNN/' + f
    for filename in os.listdir(directory):
        fileList.append(filename)
    print(fileList)
    # line = ".\Transcripts\1" +
    for d in range(len(fileList)):
        try:
            # creating a pdf file object
            pdfFileObj = open('./CNN/' + f + '/' + fileList[d], 'rb')


            # Creating a pdf reader object
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            # Getting number of pages in pdf file
            pages = pdfReader.numPages
            # Loop for reading all the Pages
            for i in range(pages):
                    # Creating a page object
                    pageObj = pdfReader.getPage(i)
                    # Printing Page Number
                    #print("Page No: ",i)
                    # Extracting text from page
                    # And splitting it into chunks of lines
                    text = pageObj.extractText().split("\n")

                    if i == 0:
                        #Retrieve Date:
                        date = ''
                        dateLine = 0
                        for line in text:
                            #if len(line) >= 9 and line[0-9] == "Copyright":
                            if "Copyright" in line:
                                #print('HELLO THERE')
                                dateLine = text.index(line) - 1
                                date = text[dateLine]


                        # Check for primetime and tucker:
                        primetime = 0
                        tucker = 0
                        for line in text:
                            if "EST" in line and ("PM" in line or "AM" in line):
                                print(line)

                                if 'TUCKER CARLSON' in line:
                                    tucker = 1

                                line = line.split()
                                time1 = 0
                                if 'PM' in line:
                                    ix = line.index('PM')
                                    time1 += 12
                                else:
                                    ix = line.index('AM')
                                show = ' '.join(line[0:ix-1])
                                time = line[ix - 1].split(':')
                                if int(time[0]) != 12:
                                    time1 += int(time[0])
                                if int(time[0]) > 7:
                                    primetime = 1
                                    print("PRIMETIME\n\n\n")
                                break

                        #Retrieve Guest List:
                        guests = ''
                        guestLine = 0
                        for line in text:
                            if "Guests:" in line:
                                #print("hi!!!!")
                            #if len(line) >= 7 and line[0 - 7] == "Guests:":
                                guestLine = text.index(line) + 1
                                guests = text[guestLine]
                        date = date.replace(',','')
                        guests = guests.replace(', ',';')
                        guests = guests.replace(',','')
                        guestList.write(date + ',' + guests[1:len(guests)] + ',' + str(primetime) + ',' +
                                        str(time1)  + ',' + str(show) + '\n')
                        break

                    """
                    # Finally the lines are stored into list
                    # For iterating over list a loop is used
                    for i in range(len(text)):
                            # Printing the line
                            # Lines are seprated using "\n"
                            print(text[i],end="END\n")
                    # For Seprating the Pages
                    print()
                    """
        except Exception as e:
            print(e)
            print(fileList[d])
            print('\n')
# closing the pdf file object
pdfFileObj.close()