import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


### railway
rail_code = gpd.read_file("shapefile/rail/lignes-lgv-et-par-ecartement.shp")[['code_ligne','catlig', 'geometry']]

rail2 = gpd.read_file("shapefile/rail/formes-des-lignes-du-rfn.shp")

rail_df = pd.DataFrame(rail_code)

rail2_df = pd.DataFrame(rail2)

rail_df = rail_df[rail_df['catlig'].isin({'Ligne Ã\xa0 grande vitesse'})]

rail2_df = rail2_df[rail2_df['code_ligne'].isin(rail_df['code_ligne'].values)]

rail2_df = rail2_df[rail2_df['mnemo'] == 'EXPLOITE']

my_rail_df = gpd.GeoDataFrame(rail2_df, geometry=rail2_df['geometry'])
#print(my_rail_df)

### station
station = gpd.read_file("shapefile/station/liste-des-gares.shp")[['code_ligne','geometry']]
station_df = pd.DataFrame(station)

my_station_df = gpd.GeoDataFrame(station_df, geometry=station_df['geometry'])


### france map

france = gpd.read_file("shapefile/france/departements-20180101.shp")[['code_insee', 'geometry']]


df = pd.DataFrame(france)
df = df.drop(df[df.code_insee == '2A'].index)
df = df.drop(df[df.code_insee == '2B'].index)
d = {'69D':'69','69M':'69'}

df = df.replace(d)
df = df.drop(df[df.code_insee == '69M'].index)
df = df.drop(df[df.code_insee.astype(int) > 97].index)

my_geo_df = gpd.GeoDataFrame(df, geometry=df['geometry'])


### plot
fig, ax = plt.subplots(figsize=(15, 15))

my_geo_df.plot(color = 'purple',alpha = 0.1,ax=ax)
my_rail_df.geometry.plot(color = 'red',ax=ax)
#my_station_df.geometry.plot(color = 'red',ax=ax)

plt.show()
