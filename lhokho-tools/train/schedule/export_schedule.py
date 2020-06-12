import datetime
import pandas as pd

import shapely.geometry as geometry

calendar = {'service_id':  [],
        'week':  [],
        'start_date': [],
        'stop_date': []
        }
calendar_file = open("../../data/export_sncf/calendar.txt", "r")
calendar_file.readline() # get rid of first line
for line in calendar_file:
    fields = line.split(",")
    calendar['service_id'].append(fields[0])
    calendar['week'].append(fields[1:8])
    calendar['start_date'].append(fields[8])
    calendar['stop_date'].append(fields[9])
calendar_file.close()

#Function to find date_range by service id
def find_date_by_service_id(service_id):
    date_range=[]
    #check if stop id in stop_summary
    for cur_service_id in calendar['service_id']:
        # split the line
        if cur_service_id == service_id:
            idx = calendar['service_id'].index(cur_service_id)
            week = calendar['week'][idx]
            start_date = calendar['start_date'][idx]
            year = start_date[0:4]
            month = start_date[4:6]
            day = start_date[6:8]
            date = datetime.datetime(int(year), int(month), int(day))
            #date_range.append(date)
            stop_date = calendar['stop_date'][idx]
            year = stop_date[0:4]
            month = stop_date[4:6]
            day = stop_date[6:8]
            s_date = datetime.datetime(int(year), int(month), int(day))
            count = 0
            while date <= s_date:
                if week[date.weekday()] == '1':
                    date_range.append(date)
                date = date + datetime.timedelta(hours=24)

    return date_range

##Stop data
stop_summary = {'stop_id': [], 'stop_name': [], 'point_wgs84': []}
file = open("../../data/export_sncf/stops.txt", "r")
file.readline()  # get rid of first line
for line in file:
    # split the line
    fields = line.split(",")
    stop_summary['stop_id'].append(fields[0].replace('OCE', '').replace('StopPoint:TGV-', '')
                                   .replace('StopPoint:OUIGO-', '')
                                   .replace('StopArea:', '')
                                   .replace('StopPoint:TGV INOUI-', ''))
    stop_summary['stop_name'].append(fields[1].replace('Gare de ', '').replace('"', ''))
    stop_summary['point_wgs84'].append(geometry.Point(float(fields[3]), float(fields[4])))
file.close()
# print(stop_summary['stop_id'][0])
# print(stop_summary['stop_name'][0])
# print(stop_summary['point_wgs84'][0])

def find_location_by_stop_id(stop_id,stops):
    for current_stop_id in stop_summary['stop_id']:
        if current_stop_id == stop_id:
            idx = stop_summary['stop_id'].index(current_stop_id)
            return stop_summary['point_wgs84'][idx]
    return geometry.Point(50,-4) #default location of Paris ?

def find_stop_name(stop_id,stops):
    #check if stop id in stop_summary
    if stop_id in stops['stop_id']:
        idx = stops['stop_id'].index(stop_id)
        #retrieve related stop name
        related_stop = stops['stop_name'][idx]
        return related_stop
    else:
        return "stop not found :"+stop_id


#Function to find date_range by trip id (using link between service id and trip id)
trips = {'route_id':  [],
        'service_id':  [],
        'trip_id': [],
        }

trips_file = open("../../data/export_sncf/trips.txt", "r")
trips_file.readline()
for line in trips_file:
    # split the line
    fields = line.split(",")
    trips['route_id'].append(fields[0])
    trips['service_id'].append(fields[1])
    trips['trip_id'].append(fields[2])
trips_file.close()

#Function to find date by trip id
def find_date_by_trip_id(trip_id):
    # check if stop id in stop_summary
    for cur_trip_id in trips['trip_id']:
        if cur_trip_id == trip_id:
            idx = trips['trip_id'].index(cur_trip_id)
            return find_date_by_service_id(trips['service_id'][idx])
    return []


##Times data
file = open("../../data/export_sncf/stop_times.txt", "r")
file.readline() #get rid of first line

#Initialize data structures
trip_summary = { 'trip_id':[] ,
                 'trip_date':[],
                 'time':[],
                 'stop':[],
                 'stop_by_name':[],
                 'stop_position_lon':[],
                 'stop_position_lat':[]}
times = []
stops = []
stops_by_name = []
stops_position = []
current_trip_id = "Not defined"
#start loop over stop_times
for line in file:
    # split the line
    fields = line.split(",")
    for date in find_date_by_trip_id(fields[0]):
        trip_summary['trip_id'].append(fields[0])
        #print(fields[1].split(':')[0])
        hours = int(fields[1].split(':')[0])
        minutes = int(fields[1].split(':')[1])
        if hours >= 24:
            hour_delta= hours-24
            date = date + datetime.timedelta(days=1)
            date = date.replace(hour=hour_delta,minute=minutes)
        else:
            date = date.replace(hour=hours,minute=minutes)
        trip_summary['trip_date'].append(date)
        trip_summary['time'].append(fields[1])
        stop_id = fields[3]\
            .replace('StopPoint:OCETGV INOUI-', '')\
            .replace('StopPoint:OCETGV-', '')\
            .replace('StopPoint:OCEOUIGO-','')
        stops.append(stop_id)
        trip_summary['stop'].append(stop_id)
        trip_summary['stop_by_name'].append(find_stop_name(stop_id,stop_summary))
        trip_summary['stop_position_lon'].append(find_location_by_stop_id(stop_id,stop_summary).y)
        trip_summary['stop_position_lat'].append(find_location_by_stop_id(stop_id,stop_summary).x)
file.close()

# print(trip_summary['trip_id'][0])
# print(trip_summary['trip_date'][0])
# print(trip_summary['time'][0])
# print(trip_summary['stop'][0])
# print(trip_summary['stop_by_name'][0])
# print(trip_summary['stop_position_lon'][0])
# print(trip_summary['stop_position_lat'][0])

#Method to calculte trip theoretical progression
def calculate_trip_progression(given_trip_id,given_time):
    store_trip_time = []
    shift = 0
    for trip_id in trip_summary['trip_id']:
        if trip_id == given_trip_id:
            idx = trip_summary['trip_id'].index(trip_id)
            #introduce shift to take into account multiple values for one trip id
            store_trip_time.append(trip_summary['trip_date'][idx+shift])
            shift += 1
    if min(store_trip_time) > given_time:
        #trip not happened yet
        return 0
    elif given_time > max(store_trip_time):
        #trip already done by given time
        return 100
    else:
        t = given_time.day *3600 + given_time.hour * 60 + given_time.minute
        tt = min(store_trip_time)
        t_min = tt.day *3600 + tt.hour * 60 + tt.minute
        tu = max(store_trip_time)
        t_max = tu.day * 3600 + tu.hour * 60 + tu.minute
        progress = int(100*(t - t_min ) / (t_max- t_min))
        return progress

#print(calculate_trip_progression('OCESN002369F250256992',datetime.datetime(2020,4,3,14,50)))

#tests
df = pd.DataFrame(trip_summary,
                      columns=['trip_id', 'trip_date', 'time', 'stop_by_name', 'stop', 'stop_position_lon',
                               'stop_position_lat'])


print('number of trip in april : '+str(len(df['trip_date'])))
#df = df[df['trip_date'].between(datetime.datetime(2020,4,23,00,00),datetime.datetime(2020,4,23,23,59))]

print('number of trip today : '+str(len(df['trip_date'])))

print(df.head(1))

df.to_pickle('../../data/temp/train_schedule.pkl')
df.to_csv('../../data/temp/train_schedule.csv',sep=';', header=True , index=False)