# -*- coding: UTF-8 -*-

import pandas as pd
import re
from geopy import distance
from itertools import islice
import requests
import datetime
from time import sleep
import json
import simplejson
from geopy import Nominatim
import unicodedata
#from beerStats import Bars
# token_auth = '74c89eca-fa14-47e1-a72f-1c9c062cb1f5'
# gare_depart = 'stop_area:OCE:SA:87391003'
# gare_arrivee = 'stop_area:OCE:SA:87575001'
# paris_lyon = requests.get(
#     ('https://api.sncf.com/v1/coverage/sncf/journeys?'
#      'from={}&to={}&').format(gare_depart, gare_arrivee),
#     auth=(token_auth, '')).json()
#
# print(paris_lyon)

def generate_duration():
    final_results = {'trip_type' : [],
                     'trip_id' : [],
                     'departure_name' : [],
                     'arrival_name' : [],
                     'departure_uic' : [] ,
                     'departure_id' : [],
                     'arrival_uic' : [], 'arrival_id' : [], 'duration' : [],'stops' : []}
    schedule = pd.read_csv('data/train_schedule.csv',sep=';',encoding='utf-8',engine='python')
    link = pd.read_csv('data/uic_id.csv', sep=';', encoding='utf-8', engine='python')
    sort_schedule = schedule.drop_duplicates(subset=['trip_id','stop','time'],ignore_index=True)
    for index, row in sort_schedule.iterrows():
        if row['trip_id'] not in final_results['trip_id']:
            current_trip = row['trip_id']
            trip = sort_schedule[sort_schedule['trip_id'].str.contains(current_trip)]
            len = trip.index.size - 1
            for index, row in islice(trip.iterrows(),0 , len):
                departure_name =  row['stop_by_name']
                departure_uic = row['stop']
                try:
                    departure_id = link.loc[link['uic'] == departure_uic]['id'].iloc[0]
                except:
                    print('En dehors de notre beau pays')
                    continue
                departure_time = str(row['time']).split(':')
                departure_time = int(datetime.timedelta(hours=int(departure_time[0]),minutes=int(departure_time[1]),seconds=int(departure_time[2])).total_seconds())
                stop_list = []
                try:
                    trip = trip.iloc[1:].reset_index(drop=True)
                except:
                    print('on a un pb')
                    pass
                for index, row in trip.iterrows():
                    if row['stop'] != departure_uic:
                        arrival_uic = row['stop']
                        try:
                            arrival_id = link.loc[link['uic'] == arrival_uic]['id'].iloc[0]
                        except:
                            print('En dehors de notre beau pays')
                            continue
                        trip_type = '{}_{}'.format(departure_uic,row['stop'])
                        arrival_name = row['stop_by_name']
                        trip_id = row['trip_id']
                        arrival_time = str(row['time']).split(':')
                        arrival_time = int(datetime.timedelta(hours=int(arrival_time[0]), minutes=int(arrival_time[1]),seconds=int(arrival_time[2])).total_seconds())
                        duration = arrival_time - departure_time
                        print(departure_name, ' - ', arrival_name)
                        final_results['trip_type'].append(trip_type)
                        final_results['trip_id'].append(trip_id)
                        final_results['departure_name'].append(departure_name)
                        final_results['arrival_name'].append(arrival_name)
                        final_results['departure_uic'].append(departure_uic)
                        final_results['departure_id'].append(departure_id)
                        final_results['arrival_uic'].append(arrival_uic)
                        final_results['arrival_id'].append(arrival_id)
                        final_results['duration'].append(duration)
                        final_results['stops'].append(list(stop_list))
                        stop_list.append(arrival_id)
                    else:
                        print('Tu peux pas aller plus loin gadjo')
        else:
            print('Already in!')
    df = pd.DataFrame.from_dict(final_results)
    df.to_csv('data/all_trip_duration.csv', sep=';',encoding='utf-8')

#generate_duration()

def generate_beer_list():
    df = pd.read_csv('city_info.csv',sep=';',encoding='utf-8',engine='python')
    beer_index = {}
    for index, row in df.iterrows():
        city_id = index
        ville = str(row['ville'])
        print(ville)
        output = Bars.from_location_name(ville)
        found_count = output.data.name.count()
        if found_count > 0:
            cheap = output._get_cheapest_bars(partial_match=True)
            df = pd.DataFrame(output.data)
            min_price_HH = cheap[0][1]
            min_price_nHH = cheap[1][1]
            df2 = df.filter(like='HHprice_')
            average_price_HH = round(df2.mean(axis=1).mean(axis=0), 1)
            df2 = df.filter(like='nHHprice')
            average_price_nHH = round(df2.mean(axis=1).mean(axis=0), 1)
            df2 = df.filter(like='beer_')
            try:
                ranking = df2.apply(pd.Series.value_counts).sum(axis=1).round().sort_values(ascending=False,kind='mergesort').drop(
                    index=['Cheapest beer', 'TBD'])
                for k in ranking.keys():
                    k = str(k).replace('.','_')
                    print(k)
            except KeyError:
                ranking = 'None'
            city_beer = {'city' : ville,
                        'price_min_nHH' : min_price_nHH,
                         'price_min_HH' : min_price_HH,
                         'average_price_HH' :  average_price_HH,
                         'average_price nHH' : average_price_nHH,
                         'ranking' : ranking}
        else:
            city_beer = 0
        beer_index.update({city_id : city_beer})
        #print(beer_index)
        with open('beer_list.json', 'w',encoding='utf-8') as output:
            inside = simplejson.dumps(beer_index, ignore_nan=True, ensure_ascii=False)
            output.write(inside)

#generate_beer_list()

def reframe_wiki():
    df = pd.read_csv('results_wikiscrapping.csv', sep=';', encoding='utf-8', engine='python')
    df = df.drop_duplicates(subset=['ville'],ignore_index=True).drop(labels=['Unnamed: 0'],axis=1)
    df.to_json('city_info.json',orient='index')
    df.to_csv('city_info.csv',sep=';')

#reframe_wiki()

def bar_list():
    df = pd.read_csv('city_info.csv', sep=';', encoding='utf-8', engine='python')
    dict = {}
    for index, row in df.iterrows():
        print(index)
        city_id = index
        print(row['ville'])
        output = Bars.from_location_name(str(row['ville']))
        if output.data.empty == True:
            print('à sec')
            json = 0
        else:
            print('à boire')
            output = pd.DataFrame(output.data).reset_index().iloc[:, 1:41]
            json = output.to_dict(orient='index')
        dict.update({city_id : json})
        print('prout')
    with open('bar_list.json', 'w', encoding='utf-8') as output:
        json = simplejson.dumps(dict, ignore_nan=True, ensure_ascii=False)
        output.write(json)

#bar_list()

def connection_list():
    df = pd.read_csv('data/all_trip_duration.csv',sep=';',encoding='utf-8',engine='python')
    with open('station.json', 'r', encoding='utf-8') as j:
        json = simplejson.loads(j.read(),encoding='utf-8')
        lenght = len(json)-1
        main_dict = {}
        for key in range(0 , lenght):
            #récupération ID départ
            city_id = key
            for key in json[key]:
                #Isole les destinations
                departure_name = key['name']
                departure_uic = key['uic']
                all_trip = df[df.departure_uic == key['uic']]
                all_trip = all_trip.filter(items=['arrival_uic','duration','stops'])
                trip_list = all_trip.drop_duplicates(subset='arrival_uic')
                arrival_dict = {}
                for index, row in trip_list.iterrows():
                    #Loop à travers les destinations
                    arrival_uic = row['arrival_uic']
                    find = False
                    for k in range(0 , lenght):
                        if find == False:
                            for elem in json[k]:
                                if arrival_uic == elem['uic']:
                                    arrival_id = k
                                    print(elem['name'])
                                    temp_df = all_trip[all_trip.arrival_uic == arrival_uic]
                                    temp_df = temp_df.filter(items=['duration', 'stops']).drop_duplicates(
                                                subset=['duration', 'stops']).reset_index(drop=True)
                                    temp_df = temp_df.to_dict('index')
                                    arrival_dict.update({k : temp_df})
                                    find = True
                                    break
                                else:
                                    continue
                                break
                        else:
                            break
            main_dict.update({city_id : arrival_dict})
        with open('data/duration.json', 'w', encoding='utf-8') as output:
            json = simplejson.dumps(main_dict, ignore_nan=True, ensure_ascii=False)
            output.write(json)

#connection_list()

def get_all_station():
    new_ref = pd.read_csv('data/trainline_data_filtered.csv',sep=';',encoding='utf-8')
    with open('data/uic_list.json','r', encoding='utf-8') as j:
        json = simplejson.loads(j.read(), encoding='utf-8')
        lenght = len(json) - 1
        new_lenght = len(json) - 1
        dict = {'id': [],
                'city' : [],
                'name': [],
                'uic': [],
                'iata_code': [],
                'lat': [],
                'lon': []}
        for index, row in new_ref.iterrows():
            city_found = 0
            current_uic = row['code_uic']
            iata_code = row['code_iata']
            try:
                for key in range(0, lenght):
                    id = key
                    for key in json[key]:
                        city_name = key['city']
                        if key['uic'] == current_uic:
                            raise KeyError
            except KeyError:
                city_found = 1
                dict['id'].append(id)
                dict['city'].append(city_name)
                dict['name'].append(row['name'])
                dict['uic'].append(current_uic)
                dict['iata_code'].append(iata_code)
                dict['lat'].append(str(row['lat']).replace(',','.'))
                dict['lon'].append(str(row['lon']).replace(',','.'))
                print('Station found')
                continue
            if city_found == 0:
                print(row['name'])
                test_point = [{'lat' : str(row['lat']).replace(',','.'), 'lng': str(row['lon']).replace(',','.')}]
                try:
                    for key in range(0, lenght):
                        id = key
                        for key in json[key]:
                            city_name = key['city']
                            center_point = [{'lat': str(key['coords'][1]).replace(',','.'), 'lng' : str(key['coords'][0]).replace(',','.')}]
                            radius = 5
                            center_point_tuple = tuple(center_point[0].values())
                            test_point_tuple = tuple(test_point[0].values())
                            dis = distance.distance(center_point_tuple, test_point_tuple).km
                            if dis <= radius:
                                dict['id'].append(id)
                                city_found = 1
                                raise KeyError
                except KeyError:
                    dict['city'].append(city_name)
                    dict['name'].append(row['name'])
                    dict['uic'].append(current_uic)
                    dict['iata_code'].append(iata_code)
                    dict['lat'].append(str(row['lat']).replace(',','.'))
                    dict['lon'].append(str(row['lon']).replace(',','.'))
                if city_found == 0:
                    pos = str(row['lat']).replace(',','.') + ", " + str(row['lon']).replace(',','.')
                    geolocator = Nominatim(user_agent="my-application", timeout=10)
                    location = geolocator.reverse(pos)
                    location_keys = location.raw['address'].keys()
                    if 'city' in location_keys:
                        dict['city'].append(location.raw['address']['city'])
                    elif 'town' in location_keys:
                        dict['city'].append(location.raw['address']['town'])
                    elif 'village' in location_keys:
                        dict['city'].append(location.raw['address']['village'])
                    elif 'municipality' in location_keys:
                        dict['city'].append(location.raw['address']['municipality'])
                    new_lenght += 1
                    print(new_lenght)
                    dict['id'].append(new_lenght)
                    dict['name'].append(row['name'])
                    dict['uic'].append(current_uic)
                    dict['iata_code'].append(iata_code)
                    dict['lat'].append(str(row['lat']).replace(',','.'))
                    dict['lon'].append(str(row['lon']).replace(',','.'))
    df = pd.DataFrame.from_dict(dict)
    d = (df.groupby(['id'], as_index=False).apply(lambda x: x[['name','city','uic','iata_code','lat','lon']].to_dict('r')).to_json(orient='records'))
    with open('station.json', 'w', encoding='utf-8') as output:
        json = simplejson.dumps(simplejson.loads(d), indent=2, sort_keys=True, ignore_nan=True, ensure_ascii=False)
        output.write(json)
    print('prout')

#get_all_station()

def get_csv_uic_id():
    with open('station.json', 'r', encoding='utf-8') as j:
        json = simplejson.loads(j.read(), encoding='utf-8')
        lenght = len(json) - 1
        new_lenght = len(json) - 1
        main_dict = {'id': [], 'city': [], 'uic': [], 'station' : []}
        for key in range(0, lenght):
            city_id = key
            for key in json[key]:
                main_dict['id'].append(city_id)
                main_dict['city'].append(key['city'])
                main_dict['uic'].append(key['uic'])
                main_dict['station'].append(key['name'])
        df = pd.DataFrame.from_dict(main_dict)
        df.to_csv('data/uic_id.csv', sep=';')
        print('prout')

#get_csv_uic_id()

def get_ter_station():
    df_stop = pd.read_csv('data/TER_station.csv',sep=';',encoding='utf-8')


    dict = {'name':[],
            'uic':[],
            'lat':[],
            'lon':[]}
    for index, row in df_stop.iterrows():
        name = row['stop_name']
        uic = re.findall('\d+', row['stop_id'])[0]
        lat = str(row['stop_lat']).replace(',','.')
        lon = str(row['stop_lon']).replace(',','.')
        dict['name'].append(name)
        dict['uic'].append(uic)
        dict['lat'].append(lat)
        dict['lon'].append(lon)
    df_stop = pd.DataFrame.from_dict(dict)
    df_stop = df_stop.drop_duplicates(subset=['uic'])
    df_stop.to_csv('data/TER_stops.csv',sep=';',encoding='utf-8')
    print('prout')
#get_ter_station()

def get_ter_connection():
    df_stop = pd.read_csv('data/TER_stops.csv', sep=';', encoding='utf-8')
    df_connection = pd.read_csv('data/TER_schedule.csv',sep=';', encoding='utf-8')
    with open('station.json', 'r', encoding='utf-8') as j:
        json = simplejson.loads(j.read(),encoding='utf-8')
        lenght = len(json)-1
        main_dict = {}
        for key in range(0 , lenght):
            #récupération ID départ
            city_id = key
            station_index = 0
            mid_dict = {}
            for key in json[key]:
                try:
                    #Isole les destinations
                    departure_name = key['name']
                    print(departure_name)
                    departure_uic = key['uic']
                    all_trip = df_connection[df_connection['stop_id'].str.contains(str(departure_uic))]
                    all_trip = all_trip[all_trip['stop_sequence'] == 0]
                    all_trip = all_trip.drop_duplicates(subset=['trip_id'],ignore_index=True)
                    arrival_df = pd.DataFrame(columns=['name','uic','lat','lon','duration'])
                    #Take the departure coord and define the radius to take only the nearest stations
                    center_point = [
                        {'lat': str(key['lat']), 'lng': str(key['lon'])}]
                    radius = 200
                    center_point_tuple = tuple(center_point[0].values())
                    for index, row in all_trip.iterrows():
                        current_trip = row['trip_id']
                        trip_list = df_connection[df_connection.trip_id == current_trip]
                        departure_hour = str(trip_list[trip_list.stop_sequence == 0]['departure_time'].iloc[0]).split(':')
                        departure_hour = int(datetime.timedelta(hours=int(departure_hour[0]), minutes=int(departure_hour[1]),
                                                              seconds=int(departure_hour[2])).total_seconds())
                        trip_list = trip_list[trip_list.stop_sequence != 0]
                        for index, row in trip_list.iterrows():
                            destination_uic = int(re.findall('\d+', row['stop_id'])[0])
                            temp_df = df_stop[df_stop['uic'] == destination_uic].reset_index(drop=True).drop(columns=['Unnamed: 0'])
                            arrival_hour = str(row['departure_time']).split(':')
                            arrival_hour = int(datetime.timedelta(hours=int(arrival_hour[0]), minutes=int(arrival_hour[1]),
                                                              seconds=int(arrival_hour[2])).total_seconds())
                            duration = {'duration' : [arrival_hour - departure_hour]}
                            duration = pd.DataFrame(duration, columns=['duration'])
                            temp_df = pd.concat([temp_df, duration],axis=1)
                            # Check if the TER station is not to far
                            test_point = [{'lat' : str(temp_df['lat'].iloc[0]), 'lng': str(temp_df['lon'].iloc[0])}]
                            test_point_tuple = tuple(test_point[0].values())
                            dis = distance.distance(center_point_tuple, test_point_tuple).km
                            if dis <= radius:
                                arrival_df = arrival_df.append(temp_df[['name','uic','lat','lon','duration']])
                    arrival_df = arrival_df.sort_values(by=['duration'])
                    arrival_df = arrival_df.drop_duplicates(subset=['uic'],ignore_index=True)
                    arrival_df = arrival_df.to_dict(orient='index')
                    mid_dict.update({station_index : arrival_df})
                    station_index += 1
                except:
                    continue
            main_dict.update({city_id : mid_dict})
        with open('data/TER_station.json', 'w', encoding='utf-8') as output:
            json = simplejson.dumps(main_dict, ignore_nan=True, ensure_ascii=False)
            output.write(json)

get_ter_connection()