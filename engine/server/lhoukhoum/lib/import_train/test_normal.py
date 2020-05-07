import copy
import json
import pandas as pd
import requests
from datetime import datetime as dt
import queue    # For Python 2.x use 'import Queue as queue'
import threading, time, random
from . import Station

passengers = [{'id': '3c29a998-270e-416b-83f0-936b606638da', 'age': 39,
               'cards': [], 'label': '3c29a998-270e-416b-83f0-936b606638da'}]

# Custom function to handle DF
def pandas_explode(df, column_to_explode):
    """
    Similar to Hive's EXPLODE function, take a column with iterable elements, and flatten the iterable to one element
    per observation in the output table

    :param df: A dataframe to explod
    :type df: pandas.DataFrame
    :param column_to_explode:
    :type column_to_explode: str
    :return: An exploded data frame
    :rtype: pandas.DataFrame
    """

    # Create a list of new observations
    new_observations = list()

    # Iterate through existing observations
    for row in df.to_dict(orient='records'):

        # Take out the exploding iterable
        explode_values = row[column_to_explode]
        del row[column_to_explode]

        # Create a new observation for every entry in the exploding iterable & add all of the other columns
        for explode_value in explode_values:

            # Deep copy existing observation
            new_observation = copy.deepcopy(row)

            # Add one (newly flattened) value from exploding iterable
            new_observation[column_to_explode] = explode_value

            # Add to the list of new observations
            new_observations.append(new_observation)

    # Create a DataFrame
    return_df = pd.DataFrame(new_observations)

    # Return
    return return_df

# Fucntion to format the trainline json repsonse
def format_trainline_response(rep_json, segment_details=False, only_sellable=True):
    """
    Format complicated json with information flighing around into a clear dataframe
    """
    #print(rep_json)
    # get folders (aggregated outbound or inbound trip)
    folders = pd.DataFrame.from_dict(rep_json['folders'])
    # print(f'we got {legs.shape[0]} legs')

    folders['nb_segments'] = folders.apply(lambda x: len(x['trip_ids']), axis=1)

    # get places (airport codes)
    stations = pd.DataFrame.from_dict(rep_json['stations'])

    # Filter out legs where there is no itinary associated (so no price)
    if only_sellable:
        folders = folders[folders.is_sellable]

    # We merge to get both the premiere departure airport and the final airport
    folders = folders.merge(stations[['id', 'name', 'country', 'latitude', 'longitude']],
                            left_on='departure_station_id', right_on='id', suffixes=['', '_depart'])
    folders = folders.merge(stations[['id', 'name', 'country', 'latitude', 'longitude']], left_on='arrival_station_id',
                            right_on='id', suffixes=['', '_arrival'])

    # If no details asked we stay at leg granularity
    if not segment_details:
        return folders[
            ['id', 'departure_date', 'arrival_date', 'nb_segments', 'name', 'country', 'latitude', 'longitude',
             'name_arrival', 'country_arrival', 'latitude_arrival', 'longitude_arrival',
             'cents', 'currency', 'comfort', 'flexibility', 'travel_class']].sort_values(by=['departure_date'])
    # else we break it down to each segment
    else:
        # get segments (each unique actual flight)
        trips = pd.DataFrame.from_dict(rep_json['trips'])
        segments = pd.DataFrame.from_dict(rep_json['segments'])
        # Explode the list of segment associated to each leg to have one lie per segment
        folders_rich = pandas_explode(folders, 'trip_ids')
        folders_rich = folders_rich.merge(trips[['id', 'segment_ids']], left_on='trip_ids', right_on='id',
                                          suffixes=['_global', '_trip'])
        folders_rich = pandas_explode(folders_rich, 'segment_ids')
        folders_rich = folders_rich.merge(segments, left_on='segment_ids', right_on='id', suffixes=['', '_seg'])

        # Add relevant segment info to the exploded df (already containing all the leg and itinary infos)
        folders_rich = folders_rich.merge(stations[['id', 'name', 'country', 'latitude', 'longitude']],
                                          left_on='departure_station_id_seg', right_on='id',
                                          suffixes=['', '_depart_seg'])
        folders_rich = folders_rich.merge(stations[['id', 'name', 'country', 'latitude', 'longitude']],
                                          left_on='arrival_station_id_seg', right_on='id',
                                          suffixes=['', '_arrival_seg'])

        # Recreate the order of the segment (not working so far)
        # folders_rich['seg_rank'] = folders_rich.groupby('id')["departure_date_seg"].rank("dense")
        # keep only the relevant information
        return folders_rich[
            ['departure_date', 'arrival_date', 'nb_segments', 'name',
             'name_arrival',
             'cents', 'train_name', 'train_number', 'travel_class_seg']].sort_values(by=['departure_date'])

# function to get all trainline fares and trips
def thread_fares(date, origin_id, destination_id, passengers, segment_details,result_queue):
    try:
        print("Thread", date)
        # Define headers (according to github/trainline)

        headers = {
                    'Accept': 'application/json',
                    'User-Agent': 'CaptainTrain/1574360965(web) (Ember 3.5.1)',
                    'Accept-Language': 'fr',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Host': 'www.trainline.eu',
                }

        session = requests.session()
        systems = ['sncf']


        data = {'local_currency': 'EUR'
                , 'search': {'passengers': passengers
                             , 'arrival_station_id': destination_id,
                             'departure_date': date,
                             'departure_station_id': origin_id,
                             'systems': systems
                            }
               }
        post_data = json.dumps(data)

        tmp = dt.now()
        ret = session.post(url= "https://www.trainline.eu/api/v5_1/search",
                                            headers=headers,
                                            data=post_data)



        print(f'API call duration {dt.now() - tmp}')

        result_df = format_trainline_response(ret.json(), segment_details=segment_details)
        #print(ret.json())
        result_queue.put(result_df)


    except KeyError:
        print('no result')
        pass
    except ValueError:
        print('no result')
        pass

# function to get all trainline fares and trips
def search_fares(date, origin_id, destination_id, passengers, segment_details):
    try:
        print("Search ", date)
        # Define headers (according to github/trainline)

        headers = {
                    'Accept': 'application/json',
                    'User-Agent': 'CaptainTrain/1574360965(web) (Ember 3.5.1)',
                    'Accept-Language': 'fr',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Host': 'www.trainline.eu',
                }

        session = requests.session()
        systems = ['sncf']


        data = {'local_currency': 'EUR'
                , 'search': {'passengers': passengers
                             , 'arrival_station_id': destination_id,
                             'departure_date': date,
                             'departure_station_id': origin_id,
                             'systems': systems
                            }
               }
        post_data = json.dumps(data)

        tmp = dt.now()
        ret = session.post(url= "https://www.trainline.eu/api/v5_1/search",
                                            headers=headers,
                                            data=post_data)



        print(f'API call duration {dt.now() - tmp}')

        result_df = format_trainline_response(ret.json(), segment_details=segment_details)
        #print(ret.json())
        return result_df
    except KeyError:
        print('no result')
        return pd.DataFrame.empty
    except ValueError:
        print('no result')
        return pd.DataFrame.empty


#short_response = search_for_all_fares('2020-05-15T09:00:00+0200', 4920, 828, passengers)
#detail_response = search_for_all_fares('2020-05-15T09:00:00+0200', 4920, 828, passengers,True)

def main():
    #test connections
    date = '2020-05-15T09:00:00+0200'
    departure_station = Station().from_tl(153)
    departure_connections = [4919,91]
    segment_details = True
    start = dt.now()
    q = queue.Queue()
    threads = [ threading.Thread(target=thread_fares, args=(date,departure_station.code_tl,connection,passengers,segment_details,q)) for connection in departure_connections ]
    for th in threads:
        th.start()
        time.sleep(3)

    while q.qsize() < len(departure_connections):
        print('wait')
        time.sleep(5)

    for i in range(q.qsize()):

        result_df = q.get()
        if i == 0:
            result_df.to_csv('test_connection.csv',sep=';',index=False)
        else:
            result_df.to_csv('test_connection.csv', sep=';', index=False, mode='a',header=False)

    print(f'Total duration {dt.now() - start}')
if __name__=='__main__':
    main()

#
# folders =  pd.DataFrame.from_dict(tmp['folders'])
# print(folders.shape)
# folders.sample(10)
#
# trips =  pd.DataFrame.from_dict(tmp['trips'])
# print(trips.shape)
# trips.head()
#
# stations =  pd.DataFrame.from_dict(tmp['stations'])
# print(stations.shape)
# stations.head()