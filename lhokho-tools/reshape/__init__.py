import time

import geocoder
import folium
import pandas
import requests
from shapely import geometry

from ..trainline import *
from ..ouisncf import *

import datetime

data_to_store_df = pandas.DataFrame(
        columns=["destination", "departure_date", "arrival_date", "duration", "number_of_segments", "price", "currency",
                 "transportation_mean"])


def _string_from_datetime(date_datetime):
    date = date_datetime
    string = str(date.day)+"/"+str(date.month)+"/"+str(date.year)+" "+str(date.hour)+":"+str(date.minute)
    # DD/MM/YYYY HH:mm
    return string

def import_trip(*args):
    print('Start batch to import trip prices...')
    start = time.time()
    if len(args) == 0:
        print('No args found. Exit')
        raise ValueError
    #get date from arguments
    if isinstance(args[0], datetime.datetime):
        date = args[0]
    else:
        raise ValueError

    if len(args) > 1:
        #case 1: treat one uic
        if isinstance(args[1], int):
            departure_id = args[1]
            print('Import price for station n°',args[1],'...')
            connections = Station.from_uic(departure_id)._get_connections()
            data_to_store_df.append(get_trip_information(departure_id,connections,date))
            print(time.time() - start)

        #case 2: treat a list of uic
        elif isinstance(args[1], list):
            departure_id = args[1]
            print('Import price for stations', args[1], '...')
            for station in args[1]:
                connections = Station.from_uic(departure_id)._get_connections()
                data_to_store_df.append(get_trip_information(station, connections,date))
                print(time.time() - start)
        #case 3: treat all station
        else:
            print('Import price for all stations...')
            for station in Station()._get_connections():
                connections = Station.from_uic(station)._get_connection_code()
                data_to_store_df.append(get_trip_information(station, connections, date))
                print(time.time() - start)
    else:
        print('Import price for all stations...')
        for station in Station()._get_connections():
            connections = Station._get_connections()
            data_to_store_df.append(get_trip_information(station, connections, date))
            print(time.time()-start)
    print(time.time() - start)
    data_to_store_df.to_csv('../temp/tl_export_{}.csv'.format(datetime),header=True,index=False,sep=';')

def get_trip_information(departure_uic_int,connections_uic_list_int,from_date,*args):
    #dataframe to retrieve results from api request
    query_df = pandas.DataFrame(
        columns=["destination", "departure_date", "arrival_date", "duration", "number_of_segments", "price", "currency",
                 "transportation_mean"])

    for connection_stop in connections_uic_list_int:
        looptime = time.time()
        try:
            from_date_str = _string_from_datetime(from_date.replace(month=5,day=1,hour=00,minute=00))
            #determine time range
            if len(args) == 0:
                to_date_str = _string_from_datetime(from_date.replace(month=5,day=1,hour=23,minute=59))
            else:
                to_date_str = _string_from_datetime(args[0])
            print("look for results from",from_date_str," to ",to_date_str)
            #search
            resultats = search(
                departure_station=str(departure_uic_int),
                arrival_station=str(connection_stop),
                from_date=from_date_str,
                to_date=to_date_str)
            #retrieve result
            query_df = resultats.df()
            query_df = query_df.fillna(connection_stop)
            print("trip [",str(departure_uic_int),"->",str(connection_stop), "] terminé")
            action_time = time.time() - looptime
            print("Temps total requête : ", action_time)
        except requests.ConnectionError:
            print(str(connection_stop), " : aucun voyage possible")
            action_time = time.time() - looptime
            print("Temps total requête (Error - connection) : ", action_time)
            pass

        except TimeoutError:
            action_time = time.time() - looptime
            print("Temps total requête (error - TimeOut) : ", action_time)
            pass

    return query_df


def connections(station_uic):
    df_connection = pd.DataFrame(columns=["origin","stop_id","frequency"])
    document_path = os.getcwd() + '\\lhoukhoum\\static\\connections.csv'
    df = pd.read_csv(document_path,sep=";")
    #df['stop_id'] = df['stop_uic']
    station_uic = [int(i) for i in station_uic]
    for index,row in df.iterrows():
        if row['stop_uic'] in station_uic:
            connections = row['connections'].replace('[','').\
                            replace(']','').split(', ')
            a = int(row["stop_uic"])

            for connection in connections:
                df_temp = pd.DataFrame(columns=["origin","stop_id"])
                df_temp['origin'] = [a]
                df_temp["stop_id"] = [connection]
                df_freq = df[df['stop_uic'].isin(df_temp['stop_id'])]
                df_freq = df_freq['frequency'].astype(float)
                df_temp['frequency'] = float(df_freq)
                #df_temp = pd.merge(df_temp,df[['stop_id','frequency']],on='stop_id')
                df_connection = df_connection.append(df_temp)

    return df_connection

def get_map_html(departure_station):
    document_path = os.getcwd() + '\\lhoukhoum\\static\\export_stop.pkl'
    stop_df = pd.read_pickle(document_path)
    departure_station = str(departure_station).replace('(', '').replace(')', '').split(', ')
    destination_list = connections(departure_station)
    connection_df = stop_df[stop_df['stop_id'].isin(destination_list['stop_id'])]
    connection_df = pd.merge(connection_df, destination_list[['origin', 'frequency', 'stop_id']], on='stop_id')
    origin_df = stop_df[stop_df['stop_id'].isin(departure_station)]
    return get_station(origin_df, connection_df)

def get_station(origin, connection):
    # generate a new map
    g = geocoder.ip('me')
    # fg={}
    # marker_cluster={}

    # Plot the departure station
    for index, row in origin.iterrows():
        folium_map = folium.Map(location=[g.lat, g.lng],
                                zoom_start=6,
                                # tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}.png'
                                # , attr=str("Tiles &copy; Esri &mdash; Source: USGS, Esri, TANA, DeLorme, and NPS"),
                                tiles='https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png'
                                , attr=str(
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>')
                                , width='100%')
        # porco_path_ = r"folium_add\porco.gif"
        # porco = folium.features.CustomIcon(icon_image=porco_path_, icon_size=(200,200))
        # folium.Marker(location=(46.028753,-5.975702),icon=porco).add_to(folium_map)
        current_origin = row['stop_id']
        current_name = row['stop_name']
        # fg["{}".format(current_origin)] = folium.FeatureGroup(name=current_name, show=False)
        # folium_map.add_child(fg["{}".format(current_origin)])
        # marker_cluster["{}".format(current_origin)] = MarkerCluster().add_to(fg["{}".format(current_origin)])
        document_path = os.getcwd() + '\\lhoukhoum\\static\\img\\station.png'
        icon_path_departure = document_path
        icon_departure = folium.features.CustomIcon(icon_image=icon_path_departure, icon_size=(20, 20))
        popup_text = "<br>{}<br>{}<br>"
        popup_text = popup_text.format(row["stop_name"],
                                       row["stop_id"])
        x_origin, y_origin = geometry.Point(row["geometry"]).coords.xy
        folium.Marker(location=(y_origin[0], x_origin[0]),
                      icon=icon_departure
                      # radius=radius,
                      # color=color,
                      , popup=popup_text,
                      # fill=True
                      ).add_to(folium_map)

        # Plot the connections
        for index, row in connection.iterrows():
            # Compute frequency here
            size = 20 * float(row['frequency'] / connection.frequency.mean())
            if size < 15:
                size = 15
            if size > 30:
                size = 30
            if row['origin'] == int(current_origin):
                document_path = os.getcwd() + '\\lhoukhoum\\static\\img\\placeholder.png'
                icon_path = document_path
                icon_station = folium.features.CustomIcon(icon_image=icon_path, icon_size=(size, size))
                # generate the popup message that is shown on click.
                popup_text = "<br>{}<br>{}<br>"
                popup_text = popup_text.format(row["stop_name"],
                                               row["stop_id"])
                # radius of circles
                # radius = 10
                # color="#FFCE00" # orange
                # color="#007849" # green
                # color = "#E37222"  # tangerine
                # color="#0375B4" # blue
                # color="#FFCE00" # yellow
                # color = "#0A8A9F"  # teal

                # add marker to the map

                x_connection, y_connection = geometry.Point(row["geometry"]).coords.xy
                folium.Marker(location=(y_connection[0], x_connection[0]),
                              icon=icon_station
                              # radius=radius,
                              # color=color,
                              , popup=popup_text,
                              # fill=True
                              ).add_to(folium_map)
                folium.PolyLine(locations=([[y_connection[0], x_connection[0]], [y_origin[0], x_origin[0]]]),
                                color="grey", weight=0.5, opacity=0.5).add_to(folium_map)

        # folium.LayerControl().add_to(folium_map)

        print("Map {} - {} saved".format(current_origin, current_name))

        return folium_map

