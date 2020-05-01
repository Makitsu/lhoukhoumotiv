import requests
import json
import pandas as pd
import time
from datetime import date
import numpy

start = time.time()
df = pd.read_csv('stations_mini5.csv',sep=";")

summary = {'departure_code':[],
           'arrival_code':[],
           'price':[],
           'category':[],
           'flexibility':[],
           'departure_date':[],
           'arrival_date':[],
           'type':[],
           'train_number':[]}
try:
    for index,row in df.iterrows():
        payload = {"fceCode": "",
                   "departureTown": {"codes": {"resarail": "FRPAR"}},
                   "destinationTown": {"codes": {"resarail": "{}".format(row[2])}}, "features": ["DIRECT_TRAVEL"],
                   "outwardDate": "2020-05-21T06:00:00.000+02:00",
                   "passengers": [{"age": 33, "ageRank": "ADULT", "commercialCard": {"type": "NO_CARD"}, "type": "HUMAN"}],
                   "travelClass": "SECOND"}

        headers = {'X-Device-Type': 'ANDROID',
                   'X-Device-Os-Version': '24',
                   'x-vsc-locale': 'fr_FR',
                   'Accept': 'application/json',
                   'Content-Type': 'application/json; charset=UTF-8',
                   'Host': 'wshoraires.oui.sncf',
                   'Connection': 'Keep-Alive',
                   'Accept-Encoding': 'gzip',
                   'Cookie': 'VMO_city=LIL_PRD1; datadome=K488XQsEatVagBURAHrgkMXqX1EVx.25_-zPs3~eBh9TifG9iJ-v.KUwdZIqZmC0Liy8ielAZYgrttcX1HnEfOOx1Iy.uRwU-V6uTSUZz~'}
        r = requests.post('https://wshoraires.oui.sncf/m730/vmd/maq/v3/proposals/train', data=json.dumps(payload),
                         headers=headers)
        print(row[1])
        print(r.content)
        data = json.loads(r.text)
        print(data['journeys'][0]['arrivalStation'])
        #data = json.load(data)
        for p in data['journeys']:
            try:
                p['unsellableReason']
            except KeyError:
                for t in p['proposals']:
                    summary['departure_code'].append(p['segments'][0]['departureStation']['info']['miInfo']['code'])
                    # Le numpy permet ici de gérer les cas avec correspondance
                    summary['arrival_code'].append(p['segments'][1]['arrivalStation']['info']['miInfo']['code'])
                    summary['price'].append(t['price']['value'])
                    summary['category'].append(t['placements'][0]['travelClass'])
                    summary['flexibility'].append(t['flexibility'])
                    summary['departure_date'].append(p['departureDate'])
                    summary['arrival_date'].append(p['arrivalDate'])
                    # MODIFIER CI-DESSOUS POUR AVOIR TOUS LES MOYENS DE TRANSPORT UTILISES SI CORRESPONDANCES
                    summary['type'].append(p['segments'][0]['transport']['kind'])
                    summary['train_number'].append(p['segments'][0]['transport']['number'])
        time.sleep(10)
except:
    print(summary)
    with open('temp/debug.json', 'w') as outfile:
        json.dump(data, outfile)
    df_results = pd.DataFrame.from_dict(summary)
    df_results.to_csv('temp/oui_export_{}.csv'.format(date.today()),sep=';')
    print('time :', time.time() - start)
# except:
#     df_results = pd.DataFrame.from_dict(summary)
#     df_results.to_csv('temp/oui_export_bug_{}.csv'.format(date.today()), sep=';')
#     with open('temp/debug.json', 'w') as outfile:
#         json.dump(data, outfile)
#     print("Error Cap", "Time : ", time.time() - start)


