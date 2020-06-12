# -*- coding: UTF-8 -*-

import pandas as pd
from itertools import islice
import requests
import datetime
from time import sleep
import json
import simplejson
import unicodedata
from beerStats import Bars
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
                     'departure_uic' : [] ,'arrival_uic' : [],'duration' : [],'stops' : []}
    schedule = pd.read_csv('train_schedule.csv',sep=';',encoding='utf-8',engine='python')
    sort_schedule = schedule.drop_duplicates(subset=['trip_id','stop','time'],ignore_index=True)
    for index, row in sort_schedule.iterrows():
        if row['trip_id'] not in final_results['trip_id']:
            current_trip = row['trip_id']
            trip = sort_schedule[sort_schedule['trip_id'].str.contains(current_trip)]
            len = trip.index.size - 1
            for index, row in islice(trip.iterrows(),0 , len):
                departure_name =  row['stop_by_name']
                departure_uic = row['stop']
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
                        trip_type = '{}_{}'.format(departure_uic,row['stop'])
                        arrival_name = row['stop_by_name']
                        arrival_uic = row['stop']
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
                        final_results['arrival_uic'].append(arrival_uic)
                        final_results['duration'].append(duration)
                        final_results['stops'].append(list(stop_list))
                        stop_list.append(row['stop_by_name'])
                    else:
                        print('Tu peux pas aller plus loin gadjo')
        else:
            print('Already in!')
    df = pd.DataFrame.from_dict(final_results)
    df.to_csv('trip_duration_3.csv', sep=';')

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
    df = pd.read_csv('trip_duration_3.csv',sep=';',encoding='utf-8',engine='python')
    with open('uic_list.json', 'r') as j:
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
        with open('trip_duration.json', 'w', encoding='utf-8') as output:
            json = simplejson.dumps(main_dict, ignore_nan=True, ensure_ascii=False)
            output.write(json)
connection_list()