import os
import os.path
import sys
import time

import geopandas as gpd
import geopy.distance
import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
from scipy.spatial.distance import cdist
from shapely import geometry
from shapely import wkt

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
#blockPrint()
start = time.time()

# RETRIEVE DATA

line_shape = gpd.read_file("../../data/shapefile/rail/formes-des-lignes-du-rfn.shp")[['code_ligne','libelle','mnemo', 'geometry']]
train_station = gpd.read_file("../../data/shapefile/station/liste-des-gares.shp")[['code_uic','code_ligne', 'geometry']]
line_info = gpd.read_file("../../data/shapefile/rail/lignes-lgv-et-par-ecartement.shp")[['code_ligne','lib_ligne','catlig','geometry']]

df_line = pd.DataFrame(line_shape,columns=['code_ligne','libelle','mnemo','geometry'])
df_line_rail = pd.DataFrame(line_info)
df_station = pd.DataFrame(train_station)

# TOOL FUNCTIONS

# Find closest point from a list of points
def closest_point(point, points):
    return points[cdist([point], points).argmin()]

# Order points by distance to a point
def get_ordered_list(points,point,*args):
    if args[0] == 'normal':
        points.sort(key = lambda p: geopy.distance.distance([p],[point]),reverse=False)
    else:
        points.sort(key=lambda p: geopy.distance.distance([p], [point]), reverse=True)
    return points

print(get_ordered_list([(0,0),(0.5,0.5)],(1,1),'reverse')[0])

# Function to return coordinates (as dataframe) of a station from station id (code UIC)
def build_boundary_station(station_id):
    station = df_station[df_station['code_uic'] == int(station_id)]
    none_idx = 0
    #case of foreign train station (no match in files)
    if station.empty:
        return station

    while station['geometry'].iloc[none_idx] is None:
        none_idx += 1

    x, y = station['geometry'].iloc[none_idx].coords.xy
    boundary_df = pd.DataFrame(list(zip(x, y)), columns=['lat', 'lon'])
    boundary_df['point'] = [(x, y) for x, y in zip(boundary_df['lat'], boundary_df['lon'])]

    return boundary_df

# GET ALL LINE POINTS AND STORE IT

if os.path.isfile('all_points.pkl') == False:
    print('Retrieve all line points...')
    # Initialize data structures
    line_point = {'code_line': [],
                  'lon': [],
                  'lat': [],
                  'point': []}

    for index, row in df_line.iterrows():
        if row['geometry'].geom_type == 'MultiLineString':
            # Put the sub-line coordinates into a list of sublists
            outcoords = [list(i.coords) for i in row['geometry']]
            for sublist in outcoords:

                test_df = df_line[df_line['code_ligne']==row['code_ligne']]
                test_df = test_df[test_df['mnemo'] == 'EXPLOITE']

                if test_df.empty == False:
                    for point in sublist:
                        line_point['code_line'].append(row['code_ligne'])
                        line_point['lat'].append(point[0])
                        line_point['lon'].append(point[1])
                        line_point['point'].append((point[0], point[1]))
        else:
            test_df = df_line[df_line['code_ligne'] == row['code_ligne']]
            test_df = test_df[test_df['mnemo'] == 'EXPLOITE']

            if test_df.empty == False:
                x, y = row['geometry'].coords.xy
                for xx in x:
                    yy = y[x.index(xx)]
                    line_point['code_line'].append(row['code_ligne'])
                    line_point['lat'].append(xx)
                    line_point['lon'].append(yy)
                    line_point['point'].append((xx, yy))
    join_df = pd.DataFrame(line_point, columns=['code_line', 'lon', 'lat', 'point'])

    join_df.to_pickle('all_points.pkl')
else:
    print('Retrieve all line points from file...')
    ###retrieve dataframe
    join_df = pd.read_pickle('all_points.pkl')

def build_railway_bw_station(departure_id,end_id):
    print('build railway between ', departure_id ,' and ',end_id)
    # Initialize data structures
    result_rail = {'id_start': [],
                'id_stop': [],
                'rail_id': [],
                'geometry': []}
    #build start and end point of line
    start_df = build_boundary_station(departure_id)
    stop_df = build_boundary_station(end_id)
    #no match for foreign train stations
    if start_df.empty or stop_df.empty:
        print('invalid boundary point, maybe a foreign train station ?')
        return result_rail
    #get all points from database
    temp_df = join_df
    res=[start_df['point'].get(0)]
    #get closest point in rail
    rail_startpoint = [closest_point(x, list(temp_df['point'])) for x in start_df['point']][0]
    #position at this point
    current_point = rail_startpoint
    index = next(iter(temp_df[temp_df['point'] == current_point].index), 'no match')
    code = temp_df['code_line'].loc[index]
    temp_df = temp_df[temp_df['point'] != current_point]
    line_df = temp_df[temp_df['code_line'] == code]
    other_line_df = temp_df[temp_df['code_line'] != code]
    res.append(current_point)
    #get end point in rail
    rail_endpoint = [closest_point(x, list(temp_df['point'])) for x in stop_df['point']][0]
    distance_to_end = geopy.distance.distance([current_point], [rail_endpoint])
    #iterate over lines while ended point not reached
    index_end = next(iter(temp_df[temp_df['point'] == rail_endpoint].index), 'no match')
    code_end = temp_df['code_line'].loc[index_end]
    codes = []
    res=[]
    print('start :',rail_startpoint)
    print('stop :',rail_endpoint)
    print('rail endpoint line is ',code_end)
    #start search for railway
    try:
        while current_point != rail_endpoint:
            print('')
            #list closest point to current
            previous_distance_to_end = distance_to_end
            distance_out = distance_to_end
            closer_out = rail_endpoint
            #iterate while no other line closeby
            while distance_out.m > 100.0:
                print('taille de la ligne ', len(line_df))
                print('distance out : ', distance_out)
                closest_point_in_line = closest_point(current_point, list(line_df['point']))
                # closer from another line
                closer_out = closest_point(current_point, list(other_line_df['point']))
                distance_out = geopy.distance.distance([closer_out], [current_point])
                # measure new distance
                new_distance_to_end = geopy.distance.distance([closest_point_in_line], [rail_endpoint])
                # come closer:
                print('distance to end : ',distance_to_end)
                if new_distance_to_end < previous_distance_to_end:
                    current_point = closest_point_in_line
                    res.append(current_point)
                    line_df = line_df[line_df['point'] != current_point]
                    print('taille du dataframe ',len(temp_df))
                    temp_df = temp_df[temp_df['point'] != current_point]
                    distance_to_end = new_distance_to_end
                    previous_distance_to_end = new_distance_to_end
                else:
                    print('remove point')
                    # back to the previous point and get rid of the other
                    temp_df = temp_df[temp_df['point'] != closest_point_in_line]
                    line_df = line_df[line_df['point'] != closest_point_in_line]
                    if line_df.empty == True:
                        distance_out = 0
                    if distance_to_end == geopy.distance.distance([rail_endpoint], [rail_endpoint]):
                        break
            #closeby line
            this_line_code = other_line_df['code_line'].loc[other_line_df['point'] == closer_out]
            print('line closeby is now :',this_line_code.values[0])
            this_line_df = other_line_df[other_line_df['code_line'] == this_line_code.values[0]]

            boundary_current_line = get_ordered_list(line_df['point'].tolist(), rail_endpoint, 'normal')[0]
            boundary_this_line = get_ordered_list(this_line_df['point'].tolist(), rail_endpoint, 'normal')[0]
            distance_to_end_new_line = geopy.distance.distance([boundary_this_line], [rail_endpoint])
            distance_to_end_line = geopy.distance.distance([boundary_current_line], [rail_endpoint])
            if  distance_to_end_new_line > distance_to_end_line:
                print('remove wrong line ',this_line_code.values[0])
                print('distance to end',distance_to_end)
                #drop other line
                temp_df = temp_df[temp_df['code_line'] != this_line_code.values[0]]
                continue
            else:
                #jump to new line
                print('branch to new line ', this_line_code.values[0])
                print('distance to end',distance_to_end)
                current_point = closer_out
                # drop old line to go to the new one
                temp_df = temp_df[temp_df['code_line'] != code]
                code = this_line_code.values[0]
                if code not in codes:
                    codes.append(code)
                line_df = temp_df[temp_df['code_line'] == code]
                other_line_df = temp_df[temp_df['code_line'] != code]
                res.append(current_point)
                if code_end == code:
                    print('end line detected...')
                    #keep only end line !
                    temp_df = temp_df[temp_df['code_line'] == code]
                continue
        res.append(rail_endpoint)
    except:
        res.append(rail_endpoint)
    finally:
        if len(res) == 1:
            line = res[0]
        else:
            line = geometry.LineString(res)
        #retrieve all results
        result_rail['id_start'].append(departure_id)
        result_rail['id_stop'].append(end_id)
        result_rail['rail_id'].append(codes)
        result_rail['geometry'].append(line)

        return result_rail

draw_df = pd.DataFrame(columns=['id_start', 'id_stop', 'rail_id', 'geometry'])

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
        return test['geometry']
    else:
        return pd.DataFrame(columns=['id_start', 'id_stop', 'rail_id', 'geometry'])


###retrieve dataframe
# save_df = pd.read_pickle('train_schedule.pkl')
# ct = 1
#
# try:
#     init = False
#     for trip_id in list(save_df['trip_id'].unique()):
#         sort_df = save_df[save_df['trip_id'] == trip_id]
#         stops = list(sort_df['stop'])
#         if len(stops) > 1:
#             print('TRIP :' + trip_id + ' - ' + str(ct) + '/' + str(len(save_df['trip_id'].unique())))
#             count = 0
#             for stop in stops:
#                 if count > 0 & count < len(stops) - 1:
#                     current_stop = int(stop)
#                     previous_stop = int(stops[count - 1])
#                     if get_railway_in_base(previous_stop,stop).empty:
#                         if previous_stop != stop:
#                             if init == False:
#                                 cur = build_railway_bw_station(previous_stop, stop,2)
#                                 if len(cur) > 0:
#                                     cur_df = pd.DataFrame(cur, columns=['id_start', 'id_stop', 'rail_id', 'geometry'])
#                                     cur_df.to_csv('save_df.csv',sep=';', mode='a', header=True, index=False)
#                                     draw_df.append(cur_df)
#                                 init = True
#                             else:
#                                 cur = build_railway_bw_station(previous_stop,stop,2)
#                                 cur_df = pd.DataFrame(cur, columns=['id_start', 'id_stop', 'rail_id', 'geometry'])
#                                 cur_df.to_csv('save_df.csv',sep=';', mode='a', header=False , index=False)
#                                 draw_df.append(cur_df)
#                 count += 1
#             ct += 1
# except:
#     #draw_df.to_pickle('draft_lines.pkl')
#     traceback.print_exc()


# test_station = df_station[df_station['code_uic'].isin({87611004})]
#
# test_station2 = df_station[df_station['code_uic'].isin({87581009})]
#
# test_station3 = df_station[df_station['code_uic'].isin({87581009})]

#Bordeaux 87581009
#Matabiau 87611004
#Rennes 87471003
#Montparnasse 87391003
#St Malo 87478107
#
# test_line2 = df_line[df_line['code_ligne'].isin(test_station2['code_ligne'])]
#
# test_line_join = test_line2[test_line2['code_ligne'].isin(test_line['code_ligne'])]
#
# print(test_line_join.head())
#
# test_lgv_gdf = gpd.GeoDataFrame(lgv_df, geometry=lgv_df['geometry'])

# test_line_gdf2 = gpd.GeoDataFrame(test_line2, geometry=test_line2['geometry'])
# test_line_join = gpd.GeoDataFrame(test_line_join, geometry=test_line_join['geometry'])

## PLOTTING

cur_df = pd.DataFrame(build_railway_bw_station(87773002,87686006), columns=['id_start', 'id_stop', 'rail_id', 'geometry'])

crs = {'init': 'epsg:4326'}
gdf = gpd.GeoDataFrame(cur_df, crs=crs, geometry=cur_df['geometry'])
# print(df_line)

#test_line = df_line[df_line['code_ligne'].isin({'553000'})
# test_line_gdf = gpd.GeoDataFrame(test_line, geometry=test_line['geometry'])
# print(test_line_gdf)
#st-malo 87478107
#rennes 87471003
#mont 87391003
#
# test_line = df_line[df_line['code_ligne'].isin({'441000'})]
# test_line_gdf = gpd.GeoDataFrame(test_line, geometry=test_line['geometry'])
#
fig, ax = plt.subplots(figsize=(15, 15))
gdf.geometry.plot(color = 'blue',ax=ax)
#test_line_gdf.geometry.plot(color = 'red',ax=ax)

mplleaflet.show(fig=fig, crs=gdf.crs)


# test_lgv_gdf.geometry.plot(color = 'purple',ax=ax)


#

# #gdf.geometry.plot(color = 'red',ax=ax)
# fig, ax = plt.subplots(figsize=(15, 15))
# gpd_res.geometry.plot(color = 'blue',ax=ax)
# #test = find_railway_bw_station(87391003,87471003)
#
# mplleaflet.show(fig=fig, crs=gdf.crs)
# #find_railway_bw_station(87471003,87478107).geometry.plot(color = 'blue',ax=ax)
# #test_lgv_gdf.geometry.plot(color = 'purple',ax=ax)

# plt.show()
print(time.time() - start)