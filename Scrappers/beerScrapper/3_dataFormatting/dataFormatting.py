"""
    - Takes data scrapped on MisterGoodBeer and GPS coordinates from Nomatim
    - Output beer-only data in the wanted format in "out.csv"
    - Output data in a csv easy-to-handle format called "result.csv" which columns are the following:
    [barName, barAddress, latitude, longitude, HHstart, HHend, confidenceIndex, beer1, nHHprice1, HHprice1, beer2, nHHprice2, HHprice2, beer3, ...]

"""
import pandas as pd
from geopy import Nominatim


dataProc = False #True if need to extract and reaarang beer data (is is saved at the end)
dataFormating = False
normaliseAddress = False
no_TDB_price = True

if dataProc is True:
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
if dataFormating is True:
    df4= pd.read_csv("../1_mainScrapper/data.csv", delimiter =";", index_col=False)    #Loading original data
    df4 = df4.drop(["beers"],axis=1)    #Getting rid of last 'beers' column
    df5 = pd.read_csv("out.csv")    #Load new beer dataframe
    df6 = pd.read_csv("../2_GPS/SAVE(old)/latitude_data.csv", names=['latitude'])  #Load latitude data
    df6 = df6.drop(df6.index[0]).reset_index()  #Drop first line irrelevant data
    df7 = pd.read_csv("../2_GPS/SAVE(old)/longitude_data.csv", names=['longitude'])     #Load longitude data
    df7 = df7.drop(df7.index[0]).reset_index()  #Drop irrelevant first line irrelevant data
    result = pd.concat([df4, df5, df6, df7], axis=1, sort=False)  #Build new data with wanted dataframe
    column_names = list(result.columns)

    #Rearranging dataframe
    final_order = column_names[:2] + [column_names[-3], column_names[-1]] + column_names[2:-4]
    result=result[final_order]

    #Take out TBD data
    result_no_TBD = result[result['latitude'] != 'TBD']

if normaliseAddress is True:
    result_no_TBD = pd.read_csv("SAVE (old)/result_no_TBD.csv", delimiter=",")
    #Normalise address data with Geopy
    Initialisation = True
    counter = 0

    if Initialisation is False:
        with open('progress', mode='rb') as file:
            progress = int(file.read())
    else:
        progress = 0

    while progress > counter:
            counter +=1

    for index, row in result_no_TBD.iterrows():
        try:
            if counter%100 == 0: # print progress every 200 adresses processed
                print(counter, 'adresses ont été traitées')

            #call of Nomatim to generates normalised address from GPS coordinates
            GPS = (row['latitude'], row['longitude'])
            geolocator = Nominatim(user_agent="my-application", timeout=10)
            location = geolocator.reverse(GPS)
            location_keys = location.raw['address'].keys()
            result_no_TBD.loc[index, 'display_name'] = location.raw['display_name']
            for key in location_keys:
                result_no_TBD.loc[index, key] = location.raw['address'][key]

            # Save counter to be able to re-run the code where it has stopped
            counter += 1
            with open('progress', mode='w') as file:
                    file.write(str(counter))
            print(counter)

        except StopIteration:
            print('Itération interrompue.', counter, ' lignes ont été traitées')
            break

    print(counter)
#Saving
#result.to_csv('result.csv')
#result.to_excel('result.xlsx')
#result_no_TBD.to_csv('result_no_TBD.csv')

if no_TDB_price is True:
    result_no_TBD = pd.read_csv("SAVE (old)/result_no_TBD.csv", delimiter=",")
    result_no_TBD.loc[:,['HHprice_8','nHHprice_8']] = result_no_TBD.loc[:,['HHprice_8','nHHprice_8']].replace("TBD","")


#data = pd.read_csv("SAVE (old)/result_no_TBD.csv", index_col = 0)
#result_no_TBD = result_no_TBD.drop(["Unnamed: 0.1"], axis = 1)
result_no_TBD.to_csv('result_no_TBD.csv')


# Datatype forcing for smooth analysis
all_bars = pd.read_csv('result_no_TBD.csv', delimiter=',', index_col=0)
beers_price_columns = []
beers_volume_columns = []
for i in range(7):
    beers_price_columns += [9+i*4,10+i*4]
    beers_volume_columns += [11+i*4]
for i in beers_price_columns:
    all_bars.iloc[:, i] = pd.to_numeric(all_bars.iloc[:, i], errors='coerce')

all_bars = all_bars.drop(["Unnamed: 0.1"], axis = 1)
all_bars.to_csv('result_no_TBD.csv')
