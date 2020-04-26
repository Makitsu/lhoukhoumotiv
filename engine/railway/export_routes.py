import re

data = {'route_id':  [],
        'service_id':  [],
        'start_name': [],
        'stop_name': [],
        }

file = open("export_sncf/routes.txt", "r")
file.readline() #get rid of first line
for line in file:
    #split the line
    fields = line.split(",")
    #extract the data:
    route_id = fields[0]
    #determine start & stop
    start = "NA"
    stop = "NA"
    if fields[3].find('<>')>0 :
        res = re.split('<>', fields[3])
        start = res[0].replace('\"','').lower()
        stop = res[1].replace('\"','').lower()
    if fields[3].find(' - ')>0 :
        res = re.split(' - ', fields[3])
        start = res[0].replace('\"','').lower()
        stop = res[1].replace('\"','').lower()
    # add route
    data['route_id'].append(route_id)
    data['start_name'].append(start)
    data['stop_name'].append(stop)
    #print(" id : "+route_id+"\n start : "+start+"\n stop : "+stop)
# file.close()
#df = pd.DataFrame (data, columns = ['route_id','start_name','stop_name'])

#print(data)

file = open("export_sncf/trips.txt", "r")
file.readline() #get rid of first line

service_id = []
trip_id = []
start_time = []
stop_times = []
end_time = []

for route_id in data['route_id']:
    for line in file:
        # split the line
        fields = line.split(",")
        # extract the data:
        f_route_id = fields[0]
        if route_id == f_route_id :
            #print('new route added : ' + f_route_id)
            service_id.append(fields[1])
            trip_id.append(fields[2])
file.close()
#print(trip_id)





