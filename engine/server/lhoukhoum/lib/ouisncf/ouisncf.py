import requests
import json
import pandas as pd
import time
from datetime import date
import numpy
import __init__

cookie1 = "datadome=KJQOZLvAP-6j7U9YsM6zhxLvzg4CcJKYLle2E2~ycZCnS-vZFIqP5eDJO9eZ4ed52oY3KyMw.mX4mT1WA8f97msgpJGN9DnXJllsHaqV2F"
cookie2 = "datadome=1guhvzE6Bez4nFLZdb6YT6UIY3lbPVsjaSfq841C0HDOs~gu9gDGHZ6KVp.Zjm4q9hPvPjTsLDv5o7xQzN2UEzTi1n.zDt2xcdIFa85BBm; VMO_city=LIL_PRD1"
cookie3 = "VMO_city=LIL_PRD1; datadome=BE5NXk4Sar2MxhjNw9-vDzO5PXmGlW~.w.Gym07lQ98I1xqhPVhPdkNxJji7iIEIwhsPaOmlbTgRBzE-ydE.KxVQkZLJwMthrm4WVsZ5_B; vmosas=0"

time_sleep = 6
global_time = time.time()

summary = {'departure_code':[],
           'arrival_code':[],
           'price':[],
           'category':[],
           'flexibility':[],
           'travel_time':[],
           'departure_date':[],
           'arrival_date':[],
           'type':[],
           'train_number':[]}

debug = {'error_code':[],'departure_code':[],'destination_code':[]}


departures = __init__._STOP_CODE
for departure in departures:
    try:
        destinations = __init__.Station().from_code(departure)._get_connection_code()
        for destination in destinations:
            request_time = time.time()
            payload = {"fceCode": "",
                       "departureTown": {"codes": {"resarail": "{}".format(departure)}},
                       "destinationTown": {"codes": {"resarail": "{}".format(destination)}},
                       "features": ["DIRECT_TRAVEL"],
                       "outwardDate": "2020-05-06T06:00:00.000+02:00",
                       "passengers": [
                           {"age": 33, "ageRank": "ADULT", "commercialCard": {"type": "NO_CARD"}, "type": "HUMAN"}],
                       "travelClass": "SECOND"}
            headers = {'X-Device-Type': 'ANDROID',
                       'X-Device-Os-Version': '24',
                       'x-vsc-locale': 'fr_FR',
                       'Accept': 'application/json',
                       'Content-Type': 'application/json; charset=UTF-8',
                       'Host': 'wshoraires.oui.sncf',
                       'Connection': 'Keep-Alive',
                       'Accept-Encoding': 'gzip',
                       'Cookie' : "{}".format(cookie1)}
            r = requests.post('https://wshoraires.oui.sncf/m730/vmd/maq/v3/proposals/train', data=json.dumps(payload),
                              headers=headers, timeout=20)
            print("Temps requête : ", request_time - time.time())
            print(r, " : ", r.content)
            data = json.loads(r.text)
            print(data['journeys'][0]['arrivalStation'])
            for p in data['journeys']:
                try:
                    p['unsellableReason']
                except KeyError:
                    try:
                        p['segments'][1]
                    except IndexError:
                        if p['segments'][0]['transport']['kind'] == "TER":
                            print("TER")
                        else:
                            for t in p['proposals']:
                                summary['departure_code'].append(
                                    p['segments'][numpy.argmin(p['segments'])]['departureStation']['info']['miInfo'][
                                        'code'])
                                # Le numpy permet ici de gérer les cas avec correspondance
                                summary['arrival_code'].append(
                                    p['segments'][numpy.argmax(p['segments'])]['arrivalStation']['info']['miInfo'][
                                        'code'])
                                summary['price'].append(t['price']['value'])
                                summary['category'].append(t['placements'][0]['travelClass'])
                                summary['flexibility'].append(t['flexibility'])
                                summary['travel_time'].append(p['durationInMillis'])
                                summary['departure_date'].append(p['departureDate'])
                                summary['arrival_date'].append(p['arrivalDate'])
                                # MODIFIER CI-DESSOUS POUR AVOIR TOUS LES MOYENS DE TRANSPORT UTILISES SI CORRESPONDANCES
                                summary['type'].append(p['segments'][0]['transport']['kind'])
                                summary['train_number'].append(p['segments'][0]['transport']['number'])
            print('End request computing : ',time.time()-request_time)
            time.sleep(time_sleep)

    except requests.Timeout as error:
        print("Timeout - {} => {}".format(departure, destination))
        debug['error_code'].append("Timeout")
        debug['departure_code'].append(departure)
        debug['destination_code'].append(destination)
        time.sleep(time_sleep)
        continue

    except (KeyboardInterrupt, SystemExit):
        print('KeyboardInterrupt')
        with open('temp/debug.json', 'w') as outfile:
            json.dump(data, outfile)
        df_results = pd.DataFrame.from_dict(summary)
        df_debug = pd.DataFrame.from_dict(debug)
        df_results.to_csv('temp/oui_export_{}.csv'.format(date.today()), sep=';', index=False)
        df_debug.to_csv('temp/debug_{}.csv'.format(date.today()), sep=';', index=False)
        print('Debug - Time :', time.time() - global_time)
        exit()
    except KeyError:
        print("KeyError - {} => {}".format(departure,destination))
        debug['error_code'].append(r.status_code)
        debug['departure_code'].append(departure)
        debug['destination_code'].append(destination)
        time.sleep(time_sleep)
        continue
    except:
        with open('temp/debug.json', 'w') as outfile:
            json.dump(data, outfile)
        df_results = pd.DataFrame.from_dict(summary)
        df_debug = pd.DataFrame.from_dict(debug)
        df_results.to_csv('temp/oui_export_{}.csv'.format(date.today()), sep=';', index=False)
        df_debug.to_csv('temp/debug_{}.csv'.format(date.today()), sep=';', index=False)
        print('Debug - Time :', time.time() - global_time)
        exit()

df_results = pd.DataFrame.from_dict(summary)
df_debug = pd.DataFrame.from_dict(debug)
df_results.to_csv('temp/oui_export_{}.csv'.format(date.today()), sep=';', index=False)
df_debug.to_csv('temp/debug_{}.csv'.format(date.today()), sep=';', index=False)
print('Final - Time :', time.time() - global_time)

# except:
#     with open('temp/debug.json', 'w') as outfile:
#         json.dump(data, outfile)
#     df_results = pd.DataFrame.from_dict(summary)
#     df_results.to_csv('temp/oui_export_{}.csv'.format(date.today()),sep=';')
#     print('Debug - Time :', time.time() - start)
#     exit()





# except:
#     df_results = pd.DataFrame.from_dict(summary)
#     df_results.to_csv('temp/oui_export_bug_{}.csv'.format(date.today()), sep=';')
#     with open('temp/debug.json', 'w') as outfile:
#         json.dump(data, outfile)
#     print("Error Cap", "Time : ", time.time() - start)


