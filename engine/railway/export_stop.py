import shapely.geometry as geometry
import pandas as pd

#Get all TGV
print('Read data from TGV stop file...')
tgv_station = pd.read_csv('../../data/export_sncf/station_tgv.csv',delimiter=';')
print(list(tgv_station['Gare']))

##Stop data
def find_station_in_tgv(station_sncf_name):
    station_sncf_name = station_sncf_name.lower()
    station_sncf_name = station_sncf_name.replace(' - ',' ').replace('-',' ')\
        .replace('-',' ').replace('.','')\
        .replace('ã©','e').replace('ã¨','e')\
        .replace('ã®','i').replace('ãª','e')\
        .replace('ã«','e')\
        .replace('ã¢','a').replace('ã»','u')\
        .replace('ã´','o').replace('st-','saint-') \
        .replace(' 1 2', '') \
        .replace('sud ', 'sud de ') \
        .replace(' (deux sevr)', '') \
        .replace('gare du nord', 'nord') \
        .replace(' chal. les eaux', '') \
        .replace(' s v gare','')\
        .replace(' (hte savoie)','').replace('a.','')\
        .replace('st ','saint ').replace('ã§','c').replace('s loir','sur loir')
    if station_sncf_name.find('chal les eaux') != -1:
        return 'Chambéry - Challes-les-Eaux;Savoie',['TGV inOui','Thalys (saisonnier)']
    if station_sncf_name.find('maurienne') != -1:
        return 'Saint-Jean-de-Maurienne - Vallée de l\'Arvan',['TGV inOui']
    if station_sncf_name.find('verton') != -1:
        return 'Rang-du-Fliers - Verton',['TGV inOui','TERGV']
    if station_sncf_name.find('gervais') != -1:
        return 'Saint-Gervais-les-Bains-Le Fayet',['TGV inOui (saisonnier)']
    if station_sncf_name.find('creusot') != -1:
        return 'Le Creusot - Montceau - Montchanin',['TGV inOui']
    if station_sncf_name.find('aeropt') != -1:
        return 'Aéroport Charles-de-Gaulle TGV',['TGV inOui','Ouigo','Thalys']
    if station_sncf_name.find('biganos') != -1:
        return 'Facture-Biganos',['TGV inOui','Thalys (saisonnier)']
    for elem in list(tgv_station['Gare']):
        type = tgv_station[tgv_station['Gare'] == elem]['Type_de_train'].iloc[0]
        type = type.split('-')
        station = elem.lower()
        station = station.replace(' - ',' ').replace('-',' ')\
        .replace('é','e').replace('è','e')\
        .replace('î','i').replace('ê','e')\
        .replace('ë','e')\
        .replace(' - challes-les-eaux','')\
        .replace('â','a').replace('û','u')\
        .replace('ô','o').replace('ç','c')
        if station.find(station_sncf_name) != -1:
            return elem, type
    print('not found: ', station_sncf_name)

    return 'Not found',['Unknown types']

print('Read data from stop file...')
stop_summary = { 'stop_id':[],'stop_name':[],'train_type':[],'geometry':[]}
file = open("../../data/export_sncf/stops.txt", "r")
file.readline() #get rid of first line
for line in file:
    # split the line
    fields = line.split(",")
    train_station = fields[1].replace('Gare de ', '').replace('"', '')
    current_station, type_of_train = find_station_in_tgv(train_station)
    if  current_station != 'Not found':
        stop_summary['stop_id'].append(fields[0].replace('OCE', '').replace('StopPoint:TGV-', '')
                                       .replace('StopPoint:OUIGO-', '')
                                       .replace('StopArea:', '')
                                       .replace('StopPoint:TGV INOUI-', ''))
        stop_summary['train_type'].append(type_of_train)
        stop_summary['stop_name'].append(current_station)
        stop_summary['geometry'].append(geometry.Point(float(fields[4]),float(fields[3])))
file.close()
#match


stop_df = pd.DataFrame(stop_summary, columns = ['stop_id','stop_name','train_type','geometry'])
stop_df = stop_df.groupby('stop_name').agg({'stop_id':'first',
                             'train_type': 'first',
                             'geometry':'first' }).reset_index()

print(stop_df['train_type'])

stop_df.to_csv('../../data/temp/export_stop.csv',sep=';', header=True , index=False)