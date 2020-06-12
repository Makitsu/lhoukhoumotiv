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
import matplotlib.pyplot as plt
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
        df = all_bars = data_import()
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

    def _get_bars_serving(self, beer_name, partial_match = True):
        """
        intermediate method to extract all bars serving the specified beer and the beer associated infos
        :param beer_name: name of the searched beer
        :param partial_match: optional for partial or strict match with specified name, default as True
        :return:beer_nHH_price_list, all prices of the searched beer (nHH).
                beer_HH_price_list, all prices of the searched beer (HH).
                bars_indices
        """
        bars_list = self.data
        # finds indices of all bars having the searched beer with the corresponding beer column (case insensitive)
        bars_list.reset_index(inplace=True)
        beer_name = beer_name.capitalize()
        beers_list = bars_list.filter(regex="^beer_").astype(str).values.tolist()
        beers_list = np.char.capitalize(beers_list)
        if partial_match is False:
            bars_indices = np.where(beers_list == beer_name)
        else:
            bars_indices = np.where(np.char.find(beers_list, beer_name) != -1)
        # translates list indices into dataframe indices
        beer_nHHprice_index = bars_indices[1] * 4 + 9
        beer_HHprice_index = bars_indices[1] * 4 + 10
        # loop to extract all prices of the searched beer
        beer_nHHprice_list = []
        beer_HHprice_list = []
        i = 0
        while i < len(bars_indices[0]):
            beer_nHHprice_list.append(float(self.data.iloc[bars_indices[0][i], beer_nHHprice_index[i]]))
            beer_HHprice_list.append(float(self.data.iloc[bars_indices[0][i], beer_HHprice_index[i]]))
            i += 1

        bars_indices = bars_indices[0]

        return beer_nHHprice_list, beer_nHHprice_index, beer_HHprice_list, beer_HHprice_index, bars_indices

    def _get_cheapest_bars(self, beer_name = None, partial_match = True):
        """
        Finds the cheapest bars within the list of bars
        :param beer_name (opt): name of the beer you are particularly interested in, if not specified all beers will be taken into account
               partial_match (opt) : optional for partial or strict match with specified name, default as True
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
            (beer_nHHprice_list, beer_nHHprice_index, beer_HHprice_list, beer_HHprice_index, bars_indices) = \
                self._get_bars_serving(beer_name, partial_match)
            # find the cheapest price and the list indices of all the bars having this cheapest price (one or several)
            min_nHH_price = np.nanmin(beer_nHHprice_list)
            min_HH_price  = np.nanmin(beer_HHprice_list)
            cheapest_nHH_list_indices = [i for i, x in enumerate(beer_nHHprice_list) if x == min_nHH_price]
            cheapest_HH_list_indices = [i for i, x in enumerate(beer_HHprice_list) if x == min_HH_price]
            # translates list indices into list of dataframe indices
            cheapest_nHH_df_indices = [bars_indices[i] for i in cheapest_nHH_list_indices]
            cheapest_HH_df_indices = [bars_indices[i] for i in cheapest_HH_list_indices]
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

    def _filter(self, max_price = None, min_price = None, include_HH = True, beer_name = None, partial_match = True, HH_from = None, HH_to = None):
        """
        General filtering beer data method allowing to filter according to specified parameters. All the parameters are optional.
        The returned bars dataframe is the cumulation of all the filters specified
        :param max_price (float): keeps bars having at least one beer below the specified price
        if max_price = "cheapest" the _get_cheapest_bars method is called and returned, there are four returning values
        :param min_price (float): keeps bars having at least one beer above the specified price
        :param include_HH (boolean): takes into account or not happy hour prices when price filtering
        :param beer_name (str): keeps bars having the specified beer
        :param partial_match (boolean): takes into account or not beers only containing specified (no exact match) beer name when name filtering
        :param HH_from (list[HH:mm]): keeps bars having happy hour beginning before or at the specified time
        :param HH_to (list[HH:mm]): keeps bars having happy hour ending after or at the specified time
        :return: filtered bars dataframe (exception when max_price = "cheapest")
        """
        ###################   CHEAPEST FILTER  ###################
        if max_price == "cheapest":
            (cheapest_HH, min_HH_price), (cheapest_nHH, min_nHH_price) = self._get_cheapest_bars(beer_name, partial_match)
            return (cheapest_HH, min_HH_price), (cheapest_nHH, min_nHH_price)

        ###################   BEER NAME FILTER   ###################
        if beer_name is not None:
            (beer_nHHprice_list, beer_nHHprice_index, beer_HHprice_list, beer_HHprice_index, bars_indices) = \
                self._get_bars_serving(beer_name, partial_match)
            self.data = self.data.iloc[bars_indices]

        ###################   HAPPY HOUR FILTER   ###################
        #Isolate time data and convert time into handable algebric unit --> minutes from the beginning of the day
        if HH_from is not None:
            #read HH string data and convert it into two integer columns
            HH_start = self._HH_conversion("HH_start")
            HH_from = HH_from[0] * 60 + HH_from[1]
            #Filtering bars
            HH_start_in_range = [HH_from >= time if time is not None else None for time in HH_start]
        if HH_to is not None:
            #read HH string data and convert it into two integer columns
            HH_end = self._HH_conversion("HH_end")
            HH_to = HH_to[0] * 60 + HH_to[1]
            #Filtering bars
            HH_end_in_range = [HH_to <= time if time is not None else None for time in HH_end]

        #Filtering bars data
        if HH_from is not None and HH_to is not None:
            HH_in_range = [ a and b if (a and b) is not None else(False if (a and b) is None else a or b)
                           for a,b in zip(HH_start_in_range,HH_end_in_range) ]
        elif HH_from is not None and HH_to is None:
            HH_in_range = [x if x is not None else False for x in HH_start_in_range]
        elif HH_from is None and HH_to is not None:
            HH_in_range = HH_end_in_range.replace(None,False)

        self.data = self.data[HH_in_range]

        ###################   PRICE RANGE FILTER   ###################
        if max_price is not None or min_price is not None:
            if include_HH is True:
                price_columns = "HHprice_"
            else:
                price_columns = "nHHprice_"
            prices = self.data.filter(regex=price_columns).values
            if max_price is not None and min_price is not None:
                prices_in_max =  [x <= max_price for x in np.nanmin(prices,axis=1) ]
                prices_in_min = [x >= min_price for x in np.nanmax(prices, axis=1)]
                prices_in_range = [a and b for a,b in zip(prices_in_min, prices_in_max)]
            elif max_price is not None and min_price is None:
                prices_in_range =  [x <= max_price for x in np.nanmin(prices,axis=1)]
            elif max_price is None and min_price is not None:
                prices_in_range = [x >= min_price for x in np.nanmax(prices, axis=1)]
            self.data = self.data[prices_in_range]

        return self.data

        ###################   CLOSEST BAR    ###################
    def _closest(self, lat, long):
        """
        Compute from the list of bars the closest one from the specified coordinates
        :param lat (float): latitude of your location
        :param long (float): longitude of your location
        :return closest_bar, closest_dist: dataframe row of the closest bar and distance of the closest bar
        """
        bars_list = self.data #load bars data

        bars_lat = bars_list["latitude"].values
        bars_long = bars_list["longitude"].values
        distance = [haversine(lat,long,a,b) for a,b in zip(bars_lat,bars_long)]
        closest_index = np.argmin(distance)
        closest_bar = bars_list.iloc[closest_index]
        closest_dist = np.min(distance)

        return closest_bar, closest_dist

    def _HH_conversion(self, column_name):
        """
        Converts time from [HH,MM] format into minutes passed from the beginning of the day (example : 4pm will return 16*60 = 960)
        :param column_name (str): name of the dataframe column containing time data in [HH,MM] format
        :return: corresponding list of times in minutes from the beginning of the day (example : 4pm = 16*60)
        """

        #read HH string data and convert it into two integer columns
        HH_time = self.data.filter(regex=column_name).values
        HH = [str(time[0]).replace("\'", "").replace("[", "").replace("]", "") if len(str(time)) !=5 else "" for time in HH_time]
        HH_hours = [int(str(time).split(",")[0]) if len(time) != 0 else None for time in HH]
        HH_mins = [int(str(time).split(",")[1]) if len(time) != 0 else None for time in HH]
        #convert hours into minutes from the beginning of the day (example : 4pm = 16*60)
        HH_hours = [hour * 60 if hour is not None else None for hour in HH_hours]
        HH_algebric = [a + b if a is not None else None for a,b in zip(HH_hours,HH_mins)]
        return HH_algebric

    def _stats_prices(self, include_HH = False, only_HH = False):
        if only_HH is True:
            prices = self.data.filter(regex="^HHprice_").values
        elif include_HH is True:
            prices = self.data.filter(regex="HHprice_").values
        else:
            prices = self.data.filter(regex="nHHprice_").values
        mean_prices = np.nanmean(prices)
        max_prices = np.nanmax(prices)
        min_prices = np.nanmin(prices)

        return mean_prices, max_prices, min_prices

    def _advanced_stats_prices(self, include_HH = False, only_HH = False):
        if only_HH is True:
            prices = self.data.filter(regex="^HHprice_").values
        elif include_HH is True:
            prices = self.data.filter(regex="HHprice_").values
        else:
            prices = self.data.filter(regex="nHHprice_").values
        bars_mean = np.nanmean(prices, axis=1)
        bars_mean = [floor(x) for x in bars_mean]
        mean_floor_values = []
        mean_values_counts = []
        for i in range (np.min(bars_mean), np.max(bars_mean)+1):
            mean_floor_values.append(i)
            mean_values_counts.append(bars_mean.count(i))
        mean_values_range = [str(i)+'-'+str(i+1) for i in mean_floor_values]
        # graphics
        plt.bar(mean_values_range, mean_values_counts)
        plt.title('Bars mean price distribution')
        plt.xlabel('Price range')
        plt.ylabel('number of bars')
        plt.xticks(mean_values_range)
        plt.show()
        return bars_mean

tic = time()
# test = Bars.from_location_name("lyon")
# print(test.data.columns)
# sample_df = test.data[['name','latitude','longitude']]
# sample_df['position'] = sample_df.apply(lambda row: [row['latitude'],row['longitude']], axis=1)
# print(sample_df)
# sample_df.to_csv('sample_test.csv',sep=';',index=False)
# output = test._HH_infos()
#test = Bars.from_location_name("paris")
#output = test._advanced_stats_prices(include_HH= True)
toc = time()
#print(output)
print('temps nécessaire', toc-tic)