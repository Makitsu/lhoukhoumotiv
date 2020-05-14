from geopy import Nominatim
import pandas as pd
from unidecode import unidecode
beers_price_columns = []
for i in range(7):
    beers_price_columns +=( [9+i*4,10+i*4] )


print(beers_price_columns)