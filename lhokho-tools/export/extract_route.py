import pandas as pd
import numpy as np
import time

start = time.time()

df = pd.read_csv('../../data/temp/train_schedule.csv', sep=';')

stop_df = pd.read_csv('../../data/temp/export_stop.csv', sep=';')

list_station_id = df['stop'].unique().tolist()

extract_df = df.groupby('trip_id')['stop'].apply(list).reset_index()
extract_df_name = df.groupby('trip_id')['stop_by_name'].apply(list).reset_index()

result = pd.merge(extract_df,extract_df_name)


for index, row in result.iterrows():
    row['stop'] = list(dict.fromkeys(row['stop']))
    row['stop_by_name'] = list(dict.fromkeys(row['stop_by_name']))
result = result[~result['stop'].apply(pd.Series).duplicated()]

total_frequency = df.shape[0]

storage = {'stop_uic':[],'stop_name':[],'frequency':[],'connections':[],'connections_name':[]}

print(stop_df['stop_id'])
for station in list_station_id:
    if station in stop_df['stop_id'].tolist():
        print('current',station)
        storage['stop_uic'].append(str(station))
        station_name = df[df['stop'] == station]['stop_by_name'].tolist()[0]
        storage['stop_name'].append(str(station_name))
        frequency_nb = np.sum(df['stop']== station)/total_frequency
        storage['frequency'].append(frequency_nb)
        connections = []
        connections_name = []
        for index,row in result.iterrows():
            list_stop = row['stop']
            #print(list_stop)
            if station in list_stop:
                for other_station in list_stop:
                    if other_station not in connections and other_station != station:
                        if other_station in stop_df['stop_id'].tolist():
                            connections.append(other_station)
                            other_name = df[df['stop'] == other_station]['stop_by_name'].tolist()[0]
                            connections_name.append(other_name)
        storage['connections'].append(connections)
        storage['connections_name'].append(connections_name)
final = pd.DataFrame(storage,columns=['stop_uic','stop_name','frequency','connections','connections_name'])

final.to_csv('../../data/temp/connections.csv',header=True,sep=';',index=False,encoding='utf-8')

print(time.time() - start)