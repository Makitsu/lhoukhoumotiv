import os

import folium
import pandas as pd
from shapely import geometry
from shapely import wkt

def plot_station(station):
    # generate a new map
    folium_map = folium.Map(location=[48.8534, 2.3488],
                            zoom_start=7,
                            tiles="CartoDB dark_matter",
                            width='100%')

    # for each row in the data, add a cicle marker
    for index, row in station.iterrows():

        # generate the popup message that is shown on click.
        popup_text = "<br>{}<br>{}<br>"
        popup_text = popup_text.format(row["stop_name"],
                                       row["stop_id"])

        # radius of circles
        radius = 10

        # color="#FFCE00" # orange
        # color="#007849" # green
        color = "#E37222"  # tangerine
        # color="#0375B4" # blue
        # color="#FFCE00" # yellow
        #color = "#0A8A9F"  # teal


        # add marker to the map
        x,y = geometry.Point(row["geometry"]).coords.xy
        folium.CircleMarker(location=(y[0],x[0]),
                            radius=radius,
                            color=color,
                            popup=popup_text,
                            fill=True).add_to(folium_map)
    return folium_map

stop_df = pd.read_pickle('../../data/temp/export_stop.pkl')
print(stop_df)
##plot
folium_map = plot_station(stop_df)

if os.path.isfile('save_df.csv') == True:
    with open('save_df.csv', "r") as file:
        draw_df = pd.read_csv(file, delimiter=";", error_bad_lines=False)
        draw_df['geometry'] = draw_df['geometry'].apply(wkt.loads)
        print('retrieve rail data from file...')


def get_railway_in_base(start_id, stop_id):
    test = draw_df[draw_df['id_start'] == int(start_id)]
    test = test[test['id_stop'] == int(stop_id)]
    test2 = draw_df[draw_df['id_stop'] == int(start_id)]
    test2 = test2[test2['id_start'] == int(stop_id)]
    if test.empty == False:
        print('found duplicate')
        return test['geometry']
    elif test2.empty == False:
        print('found duplicate')
        return test2['geometry']
    else:
        return pd.DataFrame(columns=['id_start', 'id_stop', 'rail_id', 'geometry'])

def get_railway_in_base(start_id, stop_id):
    test = draw_df[draw_df['id_start'] == int(start_id)]
    test = test[test['id_stop'] == int(stop_id)]
    test2 = draw_df[draw_df['id_stop'] == int(start_id)]
    test2 = test2[test2['id_start'] == int(stop_id)]
    if test.empty == False:
        print('found duplicate')
        return test2['geometry']
    elif test2.empty == False:
        print('found duplicate')
        return test['geometry']
    else:
        return pd.DataFrame(columns=['id_start', 'id_stop', 'rail_id', 'geometry'])

# rail_df = get_railway_in_base(87686006,87763029)
#
# print(rail_df)

#save temp file
folium_map.save('../../data/temp/index.html')