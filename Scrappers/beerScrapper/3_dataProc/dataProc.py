"""
    - Takes data scrapped on MisterGoodBeer and GPS coordinates from Nomatim
    - Output beer-only data in the wanted format in "out.csv"
    - Output data in a csv easy-to-handle format called "result.csv" which columns are the following:
    [barName, barAddress, latitude, longitude, HHstart, HHend, confidenceIndex, beer1, nHHprice1, HHprice1, beer2, nHHprice2, HHprice2, beer3, ...]

"""
import pandas as pd

dataProc = True #True if need to extract and reaarang beer data (is is saved at the end)

if dataProc is False:

    #Initiate new data structure
    i = 0
    beer_list = []
    while i < 8: #Create list of columns label
        i += 1
        temp = ["beer_"+str(i), "nHHprice_"+str(i),"HHprice_"+str(i),"volume_"+str(i)]
        beer_list = beer_list + temp
    df2 = pd.DataFrame([],columns=beer_list) #Create the dataframe

    #Loading scrapping data and converting beers data back into dict type
    df1= pd.read_csv("../1_mainScrapper/data.csv", delimiter =";")
    beers = df1["beers"].apply(lambda x : dict(eval(x)))

    #Loop on dict data to rearrange into df1 data with wanted structure
    i=0
    while i < len(df1.index):   #loop on rows/bars

        # list of beers, formating [(beer_name1, {HHprice, nHHprice, volume}), (beer_name2, {...}), ...]
        row = list(beers.iloc[i].items())
        temp=[]     # contains the line with the wanted format
        j=0

        while j < len(row):     #loop on each beer of the bar
            if row[j][0] == 'others':   #if more than 8 beers (not captured by the scrapper)
                temp += ["TBD","TBD","TBD","TBD"]
            else:
                keys = list(row[j][1].keys())
                temp.append(row[j][0])
                if 'nHHprice' in keys:
                    temp.append( str(row[j][1]['nHHprice'].replace('€', '')) )
                else:
                    temp.append('NaN')
                if 'HHprice' in keys:
                    temp.append( str(row[j][1]['HHprice'].replace('€', '')) )
                else:
                    temp.append( 'NaN' )
                if 'volume' in keys:
                    temp.append( str(row[j][1]['volume']) )
                else:
                    temp.append( 'NaN' )
            j +=1

        while j < 8:    #no data for these columns
            temp += ['NaN', 'NaN', 'NaN', 'NaN']
            j +=1

        df3 = pd.Series(temp, index=beer_list)
        df2 = df2.append(df3,ignore_index=True)
        i += 1
    df2.to_csv('out.csv',index=False)

#Global datadrame reformatting
df4= pd.read_csv("../1_mainScrapper/data.csv", delimiter =";", index_col=False)    #Loading original data
df4 = df4.drop(["beers"],axis=1)    #Getting rid of last 'beers' column
df5 = pd.read_csv("out.csv")    #Load new beer dataframe
df6 = pd.read_csv("../2_GPS/latitude_data.csv", names=['latitude'])  #Load latitude data
df6 = df6.drop(df6.index[0]).reset_index()  #Drop first line irrelevant data
df7 = pd.read_csv("../2_GPS/longitude_data.csv", names=['longitude'])     #Load longitude data
df7 = df7.drop(df7.index[0]).reset_index()  #Drop irrelevant first line irrelevant data
result = pd.concat([df4, df5, df6, df7], axis=1, sort=False)  #Build new data with wanted dataframe
column_names = list(result.columns)


#Rearranging dataframe and save
final_order = column_names[:2] + [column_names[-3], column_names[-1]] + column_names[2:-4]
result=result[final_order]
result.to_csv('result.csv')
result.to_excel('result.xlsx')





