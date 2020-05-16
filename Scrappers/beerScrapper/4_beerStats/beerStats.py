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

earth_circum = 40075e3  # earth circumference at equator (meters)
circularity_error = 1.01  # earth is not circular but here calculation suppose so -> 0.5% error

def data_import():
    # data import and datatype forcing for smooth analysis
    all_bars = pd.read_csv('result_no_TBD.csv', delimiter=',', index_col=0)

    HH_columns = (5,6)
    beers_price_columns = []
    beers_volume_columns = []
    for i in range(7):
        beers_price_columns += [9+i*4,10+i*4]
        beers_volume_columns += [11+i*4]
    for i in beers_price_columns:
        all_bars.iloc[:, i] = pd.to_numeric(all_bars.iloc[:, i], errors='coerce')

    return all_bars


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
            all_bars = data_import()
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
        df.data = data_import()
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
        df.data = data_import()
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
        df.data = data_import()
        name = name.lower()
        df.data = df.data[(df.data["city_district"].str.lower() == name) | (df.data["city"].str.lower() == name) | (df.data["municipality"].str.lower() == name) | (df.data["suburb"].str.lower() == name) | (df.data["town"].str.lower() == name) | (df.data["village"].str.lower() == name)]
        return cls(df.data, "from_location_name", name)

    def _get_cheapest_bars(self, beer_name = None):
        """
        Finds the cheapest bars within the list of bars
        :param beer_name (opt): name of the beer you are particularly interested in, if not specified all beers will be taken into account
        :return: 2 dataframes: the first one contains bars with the cheapest Happy Hour price, the second the cheapset non Happy Hour bars
        """

        bars_list = self.data
        if beer_name == None:
            HH_prices = bars_list.filter(regex="^HHprice_").values
            min_HH_prices = np.nanmin(HH_prices, axis=1)
            min_HH_price = np.nanmin(min_HH_prices)
            cheapest_index = np.where(min_HH_prices == min_HH_price)
            cheapest_HH = bars_list.iloc[cheapest_index]

            nHH_prices = bars_list.filter(regex="^nHHprice_").values
            min_nHH_prices = np.nanmin(nHH_prices, axis=1)
            min_nHH_price = np.nanmin(min_nHH_prices)
            cheapest_index = np.where(min_nHH_prices == min_nHH_price)
            cheapest_nHH = bars_list.iloc[cheapest_index]

        else: #specific beer has been specified
            # finds indices of all bars having the searched beer with the corresponding beer column (case insensitive)
            bars_list.reset_index(inplace = True)
            beer_name = beer_name.capitalize()
            beers_list = bars_list.filter(regex="^beer_").astype(str).values.tolist()
            beers_list = np.char.capitalize(beers_list)
            bars_indices = np.where(np.char.capitalize(beers_list) == beer_name)
            # translates list indices into dataframe indices
            beer_nHHprice_index = bars_indices[1] * 4 + 9
            beer_HHprice_index = bars_indices[1] * 4 + 10
            # loop to extract all prices of the searched beer
            beer_nHHprice_list = []
            beer_HHprice_list = []
            i=0
            while i < len(bars_indices[0]):
                beer_nHHprice_list.append( self.data.iloc[bars_indices[0][i], beer_nHHprice_index[i]] )
                beer_HHprice_list.append(self.data.iloc[bars_indices[0][i], beer_HHprice_index[i]])
                i += 1
            # find the cheapest price and the list indices of all the bars having this cheapest price (one or several)
            min_nHH_price = min(beer_nHHprice_list)
            min_HH_price  = min(beer_HHprice_list)
            cheapest_nHH_list_indices = [i for i, x in enumerate(beer_nHHprice_list) if x == min_nHH_price]
            cheapest_HH_list_indices = [i for i, x in enumerate(beer_HHprice_list) if x == min_HH_price]
            # translates list indices into list of dataframe indices
            cheapest_nHH_df_indices = [bars_indices[0][i] for i in cheapest_nHH_list_indices]
            cheapest_HH_df_indices = [bars_indices[0][i] for i in cheapest_HH_list_indices]
            # results 
            cheapest_HH = bars_list.iloc[cheapest_HH_df_indices]
            cheapest_nHH = bars_list.iloc[cheapest_nHH_df_indices]

        return (cheapest_HH, min_HH_price), (cheapest_nHH, min_nHH_price)


    def _how_many(self):
        """
        count the number of bars in the dataframe
        :return: number of bars
        """
        return len(self.data.index)

    def _HH_infos(self):
        HH_hours = self.data["HH_start"].values

        return  HH_hours

tic = time()
test = Bars.from_location_name("lyon")
print(test.data.columns)
sample_df = test.data[['name','latitude','longitude']]
sample_df['position'] = sample_df.apply(lambda row: [row['latitude'],row['longitude']], axis=1)
print(sample_df)
sample_df.to_csv('sample_test.csv',sep=';',index=False)
output = test._HH_infos()
toc = time()
print(output)
print('temps nécessaire', toc-tic)
