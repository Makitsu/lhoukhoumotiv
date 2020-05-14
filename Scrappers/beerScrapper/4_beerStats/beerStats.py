"""
    Defines a class containing beer data with corresponding methods for easy read-out
        - bar_cheapest_beer (bar_name)
            OUTPUT : 'beer_name'
        - bar_list_beers (bar_name)
            OUTPUT : [list of beers]
        - beer_prices (bar_name,beer_name)
            OUTPUT : {HH_price: xx, nHH_price: xx}
        - city_cheapest_beer (city_name,  opt: beer_name(s))
            OUTPUT : {beer_name:xx, HH_price: xx, nHH_price: xx}
"""

import pandas as pd
from math import *
from time import time
import numpy as np
import re

# data import and dataype forcing for smooth analysis
all_bars = pd.read_csv('result_no_TBD.csv', delimiter=',', index_col=0)
beers_price_columns = []
beers_volume_columns = []
for i in range(7):
    beers_price_columns += [9+i*4,10+i*4]
    beers_volume_columns += [11+i*4]
for i in beers_price_columns:
    all_bars.iloc[:, i] = pd.to_numeric(all_bars.iloc[:, i], errors='coerce')

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
    """
        simple formula to compute distances between 2 GPS coordinates taking into account earth oblateness (0.05% of approximation)
    """
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
        contains dataframe of bars with the data and the filters used to generate it
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
    def from_coord(cls, coordinates, radius=1000):
        """
        finds all bars within a radius (1000m per default) from the coordinages (longitude, latitude)
        Output : Bars dataframe with filtered bars data (within the radiys), type set as "from_coord", location set as "gps coordinates", and radius set with the specified
        radius
        """
        df = Bars()
        df.data = all_bars
        df.data['distance'] = haversine(coordinates[1], coordinates[0], all_bars['latitude'].values, all_bars['longitude'].values)
        radius = radius * 1.005 #Harvesine approximation
        df.data = df.data[df.data['distance']<=radius]
        return cls(df.data, "from_coord", coordinates, radius)

    @classmethod
    def from_postcode(cls,postcode):
        """
        finds all bars filtered via postcode from the specified postcode
        :param postcode (int)
        :return: Bars class object with data of the bars in the specified postcode
        """
        df = Bars()
        df.data = all_bars
        df.data = df.data[df.data['postcode'] == str(postcode)]
        return cls(df.data, "from_postcode", postcode)

    @classmethod
    def from_location_name(cls, name):
        """
        finds all bar filtered via location name from the specified name (case insensitive)
        :param name (str) city_district, city, municipality, suburb, town, village
        :return: Bars class object with data of the bars in the specified location name
        """
        df = Bars()
        df.data = all_bars
        name = name.lower()
        df.data = df.data[(df.data["city_district"].str.lower() == name) | (df.data["city"].str.lower() == name) | (df.data["municipality"].str.lower() == name) | (df.data["suburb"].str.lower() == name) | (df.data["town"].str.lower() == name) | (df.data["village"].str.lower() == name)]
        return cls(df.data, "from_location_name", name)

    def _get_cheapest_bar(self):
        """
        Finds the bar with the cheapest
        :return:
        """
        HH_prices  = self.data.loc[:, self.data.columns.map(lambda x: x.startswith(('HHprice_')))].values
        min_HH_prices = np.nanmin(HH_prices,axis=1)
        cheapest_index = np.where(min_HH_prices == np.nanmin(min_HH_prices))
        cheapest_HH = self.data.iloc[cheapest_index]

        nHH_prices  = self.data.loc[:, self.data.columns.map(lambda x: x.startswith(('nHHprice_')))].values
        min_nHH_prices = np.nanmin(nHH_prices,axis=1)
        cheapest_index = np.where(min_nHH_prices == np.nanmin(min_nHH_prices))
        cheapest_nHH = self.data.iloc[cheapest_index]

        return cheapest_HH, cheapest_nHH

    def _get_cheapest_beer(self):
        cheapest_HH, cheapest_nHH = self._get_cheapest_bar()
        cheapest_HH_infos = cheapest_HH.loc[:, cheapest_HH.columns.map(lambda x: x.startswith(('name','beer', 'HHprice')))].min()
        return cheapest_HH_infos

    #def _how_many(self):


tic = time()
test = Bars.from_location_name("paris")
output = test._get_cheapest_bar()
toc = time()
toc = time()
print('number of bars listed : ', len(test.data.index))
print(output)
print('temps nécessaire', toc-tic)
