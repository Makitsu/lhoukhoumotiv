import pandas as pd
import time

start = time.time()

df = pd.read_csv('../../data/temp/train_schedule.csv', sep=';')

list_station_id = df['stop'].unique().tolist()

extract_df = df.groupby('trip_id')['stop'].apply(list).reset_index()
extract_df_name = df.groupby('trip_id')['stop_by_name'].apply(list).reset_index()

result = pd.merge(extract_df,extract_df_name)


for index, row in result.iterrows():
    row['stop'] = list(dict.fromkeys(row['stop']))
    row['stop_by_name'] = list(dict.fromkeys(row['stop_by_name']))
result = result[~result['stop'].apply(pd.Series).duplicated()]

#result.to_csv('../../data/temp/connections2.csv',header=True,sep=';',index=False,encoding='utf-8')

foreign_uic = {80110684,80143099,80142281,80140087,80143198,80143313,80143503,80290346,80291039,
                80021402,80203471,80253914,80196980,80142778,80253914,80196980,#deutchland
                82001000,#Luxembourg
                87756403,#Monaco
                88140010,#Belgique
                83002022,83016451,83002485,83002048,83002220,83002451#Italie
               }

storage = {'stop_uic':[],'stop_name':[],'connections':[],'connections_name':[]}

for station in list_station_id:
    if station not in foreign_uic:
        print('current',station)
        storage['stop_uic'].append(str(station))
        station_name = df[df['stop'] == station]['stop_by_name'].tolist()[0]
        storage['stop_name'].append(str(station_name))
        connections = []
        connections_name = []
        for index,row in result.iterrows():
            list_stop = row['stop']
            #print(list_stop)
            if station in list_stop:
                for other_station in list_stop:
                    if other_station not in connections and other_station != station:
                        if other_station not in foreign_uic:
                            connections.append(other_station)
                            other_name = df[df['stop'] == other_station]['stop_by_name'].tolist()[0]
                            connections_name.append(other_name)
        storage['connections'].append(connections)
        storage['connections_name'].append(connections_name)
final = pd.DataFrame(storage,columns=['stop_uic','stop_name','connections','connections_name'])

final.to_csv('../../data/temp/connections.csv',header=True,sep=';',index=False,encoding='utf-8')

print(time.time() - start)