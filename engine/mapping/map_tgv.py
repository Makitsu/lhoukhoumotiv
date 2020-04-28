import os

import folium
import pandas as pd
from shapely import geometry
from shapely import wkt
import geocoder

connection_df = pd.read_csv('../../data/temp/connections.csv',sep=";")

def connections(station_uic):
    df_connection = pd.DataFrame(columns=["origin","stop_id"])
    df = connection_df
    station_uic = [int(i) for i in station_uic]

    for index,row in df.iterrows():
        if row['stop_uic'] in station_uic:
            connections = row['connections'].replace('[','').\
                            replace(']','').split(', ')
            for connection in connections:
                df_temp = pd.DataFrame(columns=["origin","stop_id"])
                df_temp['origin'] = row["stop_uic"]
                df_temp["stop_id"] = [connection]
                df_connection = df_connection.append(df_temp)

    return df_connection

def plot_station(origin, connection, line):
    # generate a new map
    g = geocoder.ip('me')
    folium_map = folium.Map(location=[g.lat, g.lng],
                            zoom_start=6,
                            #tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}.png'
                            #, attr=str("Tiles &copy; Esri &mdash; Source: USGS, Esri, TANA, DeLorme, and NPS"),
                            tiles ='https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png'
                            , attr=str('&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>')
                            , width='100%')

    # Plot the departure station
    for index, row in origin.iterrows():
        icon_path_departure = r"C:\Users\lhoum\Documents\Project\lhoukhoumotiv\engine\mapping\folium_add\station.png"
        icon_departure = folium.features.CustomIcon(icon_image=icon_path_departure, icon_size=(20, 20))
        popup_text = "<br>{}<br>{}<br>"
        popup_text = popup_text.format(row["stop_name"],
                                       row["stop_id"])
        x, y = geometry.Point(row["geometry"]).coords.xy
        folium.Marker(location=(y[0], x[0]),
                  icon=icon_departure
                  # radius=radius,
                  # color=color,
                  ,popup=popup_text,
                  # fill=True
                  ).add_to(folium_map)

    # Plot the conections
    for index, row in connection.iterrows():
        icon_path = r"C:\Users\lhoum\Documents\Project\lhoukhoumotiv\engine\mapping\folium_add\placeholder.png"
        icon_station = folium.features.CustomIcon(icon_image=icon_path, icon_size=(20, 20))
        # generate the popup message that is shown on click.
        popup_text = "<br>{}<br>{}<br>"
        popup_text = popup_text.format(row["stop_name"],
                                       row["stop_id"])
        # radius of circles
        #radius = 10
        # color="#FFCE00" # orange
        # color="#007849" # green
        #color = "#E37222"  # tangerine
        # color="#0375B4" # blue
        # color="#FFCE00" # yellow
        #color = "#0A8A9F"  # teal

        # add marker to the map

        x,y = geometry.Point(row["geometry"]).coords.xy
        folium.Marker(location=(y[0],x[0]),
                            icon=icon_station
                            #radius=radius,
                            #color=color,
                            ,popup=popup_text,
                            #fill=True
                            ).add_to(folium_map)

    #for index, row in line.iterrows():

    return folium_map

def init(departure_station):
    stop_df = pd.read_pickle('../../data/temp/export_stop.pkl')
    departure_station = str(departure_station).replace('(', '').replace(')', '').split(', ')
    destination_list = connections(departure_station)
    connection_df = stop_df[stop_df['stop_id'].isin(destination_list['stop_id'])]
    #connection_df = pd.merge(connection_df,destination_list[['origin','stop_id']],on='stop_id')
    print(connection_df)
    origin_df = stop_df[stop_df['stop_id'].isin(departure_station)]
    #print(connection_df)
    #print(origin_df)
    ##plot
    folium_map = plot_station(origin_df,connection_df,destination_list)
    folium_map.save('../../data/temp/index.html')

# if os.path.isfile('save_df.csv') == True:
#     with open('save_df.csv', "r") as file:
#         draw_df = pd.read_csv(file, delimiter=";", error_bad_lines=False)
#         draw_df['geometry'] = draw_df['geometry'].apply(wkt.loads)
#         print('retrieve rail data from file...')
#
#
# def get_railway_in_base(start_id, stop_id):
#     test = draw_df[draw_df['id_start'] == int(start_id)]
#     test = test[test['id_stop'] == int(stop_id)]
#     test2 = draw_df[draw_df['id_stop'] == int(start_id)]
#     test2 = test2[test2['id_start'] == int(stop_id)]
#     if test.empty == False:
#         print('found duplicate')
#         return test['geometry']
#     elif test2.empty == False:
#         print('found duplicate')
#         return test2['geometry']
#     else:
#         return pd.DataFrame(columns=['id_start', 'id_stop', 'rail_id', 'geometry'])
#
# def get_railway_in_base(start_id, stop_id):
#     test = draw_df[draw_df['id_start'] == int(start_id)]
#     test = test[test['id_stop'] == int(stop_id)]
#     test2 = draw_df[draw_df['id_stop'] == int(start_id)]
#     test2 = test2[test2['id_start'] == int(stop_id)]
#     if test.empty == False:
#         print('found duplicate')
#         return test2['geometry']
#     elif test2.empty == False:
#         print('found duplicate')
#         return test['geometry']
#     else:
#         return pd.DataFrame(columns=['id_start', 'id_stop', 'rail_id', 'geometry'])
#
#
# # rail_df = get_railway_in_base(87686006,87763029)
# #
# # print(rail_df)

#save temp file

#Enter here the departure station(s) !!!! No string pls !!!! Thanks, la bise, le bécot
requests = 87575001, 87756056
init(requests)
#connections(requests)
