import __init__
import pandas
import time
import requests
import pandas as pd
from datetime import datetime
from ExpectError import ExpectTimeout
from runtest import connections

start = time.time()
data = pandas.read_csv('export_station.csv',sep=';')
datetime = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")

summary = {
	'stop_id':[],
	'stop_name':[],
}

final_df = pd.DataFrame(columns=["destination", "departure_date", "arrival_date", "duration", "number_of_segments", "price", "currency",
                               "transportation_mean"])
requests_time = pd.DataFrame(columns=["uic_station","request_time"])

departure_id = 87391003
df_connections = connections(departure_id)

for index, row in df_connections.iterrows():
	looptime = time.time()
	#with ExpectTimeout(60):
	try:
		resultats = __init__.search(
			departure_station=str(departure_id),
			arrival_station=str(row['station_uic_dest']),
			from_date="30/04/2020 08:00",
			to_date="30/04/2020 21:00")
		a = resultats.df()
		final_df = final_df.append(a)
		final_df = final_df.fillna(row['station_uic_dest'])
		print(final_df)
		print(row['station_uic_dest'], ": terminé")
		action_time = time.time() - looptime
		print("Temps total requête : ",action_time)
		nb_result = len(a)
		b = pd.DataFrame([[int(row['station_uic_dest']), action_time, nb_result]],
						 columns=["uic_station", "request_time", "Nb_Results"])
		requests_time = requests_time.append(b)

	except requests.ConnectionError:
		print(row['station_uic_dest'], " : aucun voyage possible")
		action_time = time.time() - looptime
		print("Temps total requête (Error - connection) : ", action_time)
		nb_result = 0
		b = pd.DataFrame([[int(row['station_uic_dest']), action_time, nb_result]],
						 columns=["uic_station", "request_time", "Nb_Results"])
		requests_time = requests_time.append(b)

	except TimeoutError:
		action_time = time.time() - looptime
		print("Temps total requête (error - TimeOut) : ", action_time)
		nb_result = 0
		b = pd.DataFrame([[int(row['station_uic_dest']), action_time, nb_result]],
						 columns=["uic_station", "request_time", "Nb_Results"])
		requests_time = requests_time.append(b)
		pass

		# finally:
		# 	action_time = time.time() - looptime
		# 	print("Timeout - Forcing")
		# 	#print(action_time)
		# 	continue



final_df.to_csv('../../api-request/trainline/temp/tl_export_{}.csv'.format(datetime),header=True,index=False,sep=';')
requests_time.to_csv('../../api-request/trainline/temp/request_time_{}.csv'.format(datetime),header=True,index=False,sep=';')
print(time.time() - start)