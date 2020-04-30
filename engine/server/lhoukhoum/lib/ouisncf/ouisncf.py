import requests
import json
import pandas as pd
import time

start = time.time()
df = pd.read_csv('stations_mini5.csv',sep=";")

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
               'Cookie': 'VMO_city=LIL_PRD1; datadome=K35nsDRpsTgotfwzRtTconzcvLUMRdxNd97BFwgj-5PYg~1ynmCWkIqGcFaGLEtJ~ZwopBANWRdKJ4gtf4AhLElu~-8tR1T9nNOwMwTEvD; vmosas=0'}
    r = requests.post('https://wshoraires.oui.sncf/m730/vmd/maq/v3/proposals/train', data=json.dumps(payload),
                     headers=headers)
    print(row[1])
    print(r.content)
    j = json.loads(r.text)
    print(j['journeys'][1]["price"]["value"])
    with open('data.json', 'w') as outfile:
        json.dump(j, outfile)
    time.sleep(5)

print('time :', time.time() - start)
#print(r.headers['allow'])

