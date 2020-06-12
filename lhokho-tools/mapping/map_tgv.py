import os

import folium
from folium.plugins import MarkerCluster
import pandas as pd
from shapely import geometry
import geocoder
import time

start = time.time()

connections_df = pd.read_csv('../../data/temp/connections.csv',sep=";")

def connections(station_uic):
    df_connection = pd.DataFrame(columns=["origin","stop_id","frequency"])
    df = connections_df
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

def plot_station(origin, connection):
    # generate a new map
    g = geocoder.ip('me')
    #fg={}
    #marker_cluster={}


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
        #fg["{}".format(current_origin)] = folium.FeatureGroup(name=current_name, show=False)
        #folium_map.add_child(fg["{}".format(current_origin)])
        #marker_cluster["{}".format(current_origin)] = MarkerCluster().add_to(fg["{}".format(current_origin)])
        icon_path_departure = r"folium_add\station.png"
        icon_departure = folium.features.CustomIcon(icon_image=icon_path_departure, icon_size=(20, 20))
        popup_text = "<br>{}<br>{}<br>"
        popup_text = popup_text.format(row["stop_name"],
                                       row["stop_id"])
        x_origin, y_origin = geometry.Point(row["geometry"]).coords.xy
        folium.Marker(location=(y_origin[0], x_origin[0]),
                  icon=icon_departure
                  # radius=radius,
                  # color=color,
                  ,popup=popup_text,
                  # fill=True
                  ).add_to(folium_map)

        # Plot the connections
        for index, row in connection.iterrows():
            # Compute frequency here
            size = 20 * float(row['frequency']/connection.frequency.mean())
            if size < 15:
                size = 15
            if size > 30:
                size = 30
            if row['origin'] == int(current_origin):
                icon_path = r"folium_add\placeholder.png"
                icon_station = folium.features.CustomIcon(icon_image=icon_path, icon_size=(size, size))
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

                x_connection,y_connection = geometry.Point(row["geometry"]).coords.xy
                folium.Marker(location=(y_connection[0],x_connection[0]),
                                    icon=icon_station
                                    #radius=radius,
                                    #color=color,
                                    ,popup=popup_text,
                                    #fill=True
                                    ).add_to(folium_map)
                folium.PolyLine(locations=([[y_connection[0],x_connection[0]],[y_origin[0],x_origin[0]]]),
                                            color="grey", weight=0.5, opacity=0.5).add_to(folium_map)

        #folium.LayerControl().add_to(folium_map)
        folium_map.save('../../engine/server/lhoukhoum/static/map/porco.html'.format(current_origin,current_name))
        print("Map {} - {} saved".format(current_origin,current_name))

def init(departure_station):
    stop_df = pd.read_pickle('../../data/temp/export_stop.pkl')
    departure_station = str(departure_station).replace('(', '').replace(')', '').split(', ')
    destination_list = connections(departure_station)
    connection_df = stop_df[stop_df['stop_id'].isin(destination_list['stop_id'])]
    connection_df = pd.merge(connection_df,destination_list[['origin','frequency','stop_id']],on='stop_id')
    origin_df = stop_df[stop_df['stop_id'].isin(departure_station)]
    plot_station(origin_df,connection_df)
    #print(origin_df)
    ##plot

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
#PARIS
#requests = 87113001, 87686006, 87391003, 87271007
#POITIERS
#requests = 87575001
#BREST
#requests = 87113001,87212027,87182014,87214056,87171926,87147322,87193003,87192039,87191007,87722025,87723197,87694109,87111849,87141002,87182063,87300822,87300863,87713040,87725689,87775007,87773002,87318964,87319012,87751008,87725002,87763029,87713545,87756056,87757674,87757625,87757526,87755447,87755009,87144451,87144006,87144014,87141150,87212225,87215012,87174003,87174276,87175042,87171009,87172270,87172007,87172254,87223263,87313882,87271494,87342014,87703975,87688887,87773200,87781278,87781005,87781104,87784009,87286005,87713131,87345009,87393702,87571240,87575001,87583005,87581009,87396002,87484006,87481002,87471003,87478404,87413013,87411017,87381509,87393009,87393579,87487603,87142109,87686006,87755629,87762906,87756486,87761007,87764001,87765107,87765008,87753004,87725705,87743005,87741009,87745000,87745497,87745646,87745679,87742320,87742007,87726000,87713412,87718007,87615286,87611004,87747006,87741132,87746008,87271007,87281071,87317586,87317263,87281006,87345025,87342006,87286302,87317065,87317057,87286716,87286732,87286542,87343004,87391003,87586008,87611244,87473009,87473207,87474338,87474007,87473108,87473181,87474239,87471300,87476606,87476200,87476002,87471508,87474098,87476317,87474155,87478107,87478073,87486019,87481705,87481754,87481788,87481747,87481762,87396408,87486449,87582478,87582668,87582643,87584052,87571216,87575142,87673202,87673004,87673400,87677120,87677005,87485300,87485227,87485003,87485490,87324095,87571000,87672253,87672006,87671339,87671008
requests = 87113001
init(requests)
#connections(requests)


print(time.time()-start)