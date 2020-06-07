import requests
import simplejson

api_key = '5e0c07d2d939d7a1cbaadf4d6d0ee1bf'
lat = 43.3
lon = 5.4
lang = 'fr'

#r = requests.get('http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&lang={}&appid={}&units=metric'.format(lat,lon,lang,api_key))
# with open('test_weather.json', 'w', encoding='utf-8') as output:
#     json = simplejson.dumps(r.json(), ignore_nan=True, ensure_ascii=False)
#     output.write(json)
r = r.json()
print()
