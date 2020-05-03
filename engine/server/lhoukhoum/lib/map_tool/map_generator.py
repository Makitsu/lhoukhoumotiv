import os
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from shapely import geometry
import time
from datetime import date
from engine.server.lhoukhoum.lib.ouisncf.__init__ import Station

start = time.time()

def export_map(departure_station,Date=date.today(),prix_min=0,prix_max=300,time_min=0,time_max=1000):
    connections = pd.read_csv('../ouisncf/temp/oui_export_{}.csv'.format(Date),sep=";")
    connections = connections[connections['departure_code'] == departure_station]
    connections = connections[connections['price'].between(prix_min,prix_max+1)]
    #connections = connections[connections['travel_time'].between(time_min*60000,time_max*60000)]
    # generate a new map
    # Plot the departure station
    lat_departure = Station.from_code(departure_station).lat
    lon_departure = Station.from_code(departure_station).lon
    folium_map = folium.Map(location=[lat_departure,lon_departure],
                            zoom_start=6,
                            # tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}.png'
                            # , attr=str("Tiles &copy; Esri &mdash; Source: USGS, Esri, TANA, DeLorme, and NPS"),
                            tiles='https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png'
                            , attr=str('&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>')
                            , width='100%')
    #current_origin = row['stop_id']
    #current_name = row['stop_name']
        # fg["{}".format(current_origin)] = folium.FeatureGroup(name=current_name, show=False)
        # folium_map.add_child(fg["{}".format(current_origin)])
        # marker_cluster["{}".format(current_origin)] = MarkerCluster().add_to(fg["{}".format(current_origin)])
    icon_path_departure = r"folium_add\station.png"
    icon_departure = folium.features.CustomIcon(icon_image=icon_path_departure, icon_size=(20, 20))
    popup_text = "<br>{}<br>{}<br>"
    popup_text = popup_text.format(Station.from_code(departure_station)._get_stations_name(),departure_station)
    folium.Marker(location=(lat_departure, lon_departure),
                      icon=icon_departure
                      # radius=radius,
                      # color=color,
                      , popup=popup_text,
                      # fill=True
                      ).add_to(folium_map)
    arrival_list = connections.drop_duplicates(subset='arrival_code')
    for index, row in arrival_list.iterrows():
        # Compute frequency here
        #size = 20 * connections['arrival_code'].count / connections['arrival_code']
        #if size < 15:
            #size = 15
        #if size > 30:
            #size = 30
        icon_path = r"folium_add\placeholder.png"
        icon_station = folium.features.CustomIcon(icon_image=icon_path, icon_size=(20, 20))
        # generate the popup message that is shown on click.
        popup_text = "<br>{}<br>{}<br>"
        popup_text = popup_text.format(Station.from_code(row['arrival_code']).name, departure_station)
        # radius of circles
        # radius = 10
        # color="#FFCE00" # orange
        # color="#007849" # green
        # color = "#E37222"  # tangerine
        # color="#0375B4" # blue
        # color="#FFCE00" # yellow
        # color = "#0A8A9F"  # teal

        # add marker to the map
        lat_arrival = Station.from_code(row['arrival_code']).lat
        lon_arrival = Station.from_code(row['arrival_code']).lon
        folium.Marker(location=(lat_arrival, lon_arrival),
                      icon=icon_station
                      # radius=radius,
                      # color=color,
                      , popup=popup_text,
                      # fill=True
                      ).add_to(folium_map)
        folium.PolyLine(locations=([[lat_departure, lon_departure], [lat_arrival, lon_arrival]]),
                        color="grey", weight=0.5, opacity=0.5).add_to(folium_map)




        # folium.LayerControl().add_to(folium_map)
    folium_map.save('porco.html')
    print("Map saved")

export_map("FRPMO",prix_max=40)