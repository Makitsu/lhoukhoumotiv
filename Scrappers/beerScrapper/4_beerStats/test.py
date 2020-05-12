from geopy import Nominatim
import pandas as pd
from unidecode import unidecode

#all_bars = pd.read_csv('result_no_TBD.csv', delimiter=',')

#for index, row in all_bars.iterrows():
#    print(row['address'].split(',')[-2])

address = (48.5826016,7.755537)

geolocator = Nominatim(user_agent="my-application", timeout=10)
location = geolocator.reverse(address)

print(location.raw)