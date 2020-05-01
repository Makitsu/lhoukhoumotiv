import json
import pandas as pd
import numpy
import time
from datetime import date

start = time.time()
print(date.today())
summary = {'departure_code':[],
           'arrival_code':[],
           'price':[],
           'category':[],
           'flexibility':[],
           'departure_date':[],
           'arrival_date':[],
           'type':[],
           'train_number':[]}

with open('data.json', 'r') as outfile:
        data = json.load(outfile)
        for p in data['journeys']:
            try:
                p['unsellableReason']
            except KeyError:
                for t in p['proposals']:
                    summary['departure_code'].append(p['segments'][numpy.argmin(p['segments'])]['departureStation']['info']\
                        ['miInfo']['code'])
                    #Le numpy permet ici de gérer les cas avec correspondance
                    summary['arrival_code'].append(p['segments'][numpy.argmax(p['segments'])]['arrivalStation']['info']\
                        ['miInfo']['code'])
                    summary['price'].append(t['price']['value'])
                    summary['category'].append(t['placements'][0]['travelClass'])
                    summary['flexibility'].append(t['flexibility'])
                    summary['departure_date'].append(p['departureDate'])
                    summary['arrival_date'].append(p['arrivalDate'])
                    # MODIFIER CI-DESSOUS POUR AVOIR TOUS LES MOYENS DE TRANSPORT UTILISES SI CORRESPONDANCES
                    summary['type'].append(p['segments'][0]['transport']['kind'])
                    summary['train_number'].append(p['segments'][0]['transport']['number'])



                #print(summary['departure_code'])
#df_results = pd.DataFrame(columns=['departure_code','arrival_code','price','category','flexibility','departure_date','arrival_date','type','train_number'])

df_results = pd.DataFrame.from_dict(summary)
df_results.to_csv('test.csv',sep=';')

print(df_results)


print(time.time()-start)