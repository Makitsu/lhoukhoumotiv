"""
    Defines a class containing beer data with corresponding methods for easy read-out
        - bars_near (bar_name, distance [m])
            OUTPUT : [list of bars]
        - bar_city(bar_name)
            OUTPUT : 'city_name'
        - bar_cheapest_beer (bar_name)
            OUTPUT : 'beer_name'
        - bar_list_beers (bar_name)
            OUTPUT : [list of beers]
        - beer_prices (bar_name,beer_name)
            OUTPUT : {HH_price: xx, nHH_price: xx}
        - city_cheapest_beer (city_name, opt: beer_name(s))
            OUTPUT : {beer_name:xx, HH_price: xx, nHH_price: xx}
"""

import pandas as pd
from geopy import distance
from math import *
from time import time
import numpy as np
all_bars = pd.read_csv('result_no_TBD.csv', delimiter=',')
earth_circum = 40075e3  # earth circumference at equator (meters)
circularity_error = 1.01  # earth is not circular but here calculation suppose so -> 0.5% error


def is_in_square(coords1, coords2, radius):
    delta_lat = radians(abs(coords1[0] - coords2[0]))
    delta_long = radians(abs(coords1[1] - coords2[1]))
    max_delta_lat = abs((radius * 2 * pi) / earth_circum * circularity_error)
    max_delta_long = abs((radius * 2 * pi) / (cos(radians(coords1[0])) * earth_circum) * circularity_error)
    if delta_lat < max_delta_lat and delta_long < max_delta_long:
        return True
    else:
        return False


def haversine(lat1, lon1, lat2, lon2):
    metres = 6371392.896
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    total_metres = metres * c
    return total_metres



class Bars():
    """
        contains dataframe of bars with generating parameters,
    """

    def __init__(self, data=None, type=None, location=None, radius=None):
        if data is None:
            self.data = pd.DataFrame(columns=list(all_bars.columns))
        if data is not None:
            self.data = data
        if type is not None:
            self.type = type
        if location is not None:
            self.location = location
        if radius is not None:
            self.radius = radius

    @classmethod
    def from_coord(cls, coordinates, radius=300):
        """
            finds all bars within a radius (3000m per default) from the coordinages (longitude, latitude)
                Output : Bars dataframe
        """
        df = Bars()
        df.data = all_bars
        df.data['distance'] = haversine(coordinates[1], coordinates[0], all_bars['latitude'].values, all_bars['longitude'].values)
        radius = radius * 1.005 #Harvesine approximation
        df.data = df.data[df.data['distance']<=radius]
        return cls(df.data, "from_coord", coordinates, radius)

tic = time()
test = Bars.from_coord((2.35915061, 48.87656977), radius=200)
toc = time()
print(test.data.head(20))
print('number of bars listed : ', len(test.data.index))
print(toc - tic)