import __init__
import pandas
import time
import requests
import pandas as pd
from ExpectError import ExpectTimeout


start = time.time()
data = pandas.read_csv('export_station.csv',sep=';')


summary = {
	'stop_id':[],
	'stop_name':[],
}

final_df = pd.DataFrame(columns=["destination", "departure_date", "arrival_date", "duration", "number_of_segments", "price", "currency",
                               "transportation_mean"])
requests_time = pd.DataFrame(columns=["uic_station","request_time","Nb_Results"])



for index, row in data.iterrows():
	looptime = time.time()
	try:
		resultats = __init__.search(
			departure_station='87391003',
			arrival_station=str(row['stop_id']),
			from_date="27/04/2020 08:00",
			to_date="27/04/2020 21:00")
		a = resultats.df()
		final_df = final_df.append(a)
		final_df = final_df.fillna(row['stop_id'])
		print(final_df)
		print(row['stop_id'], ": terminé")
		action_time = time.time() - looptime
		# print(action_time)
		nb_result = len(a)
		b = pd.DataFrame([[int(row['stop_id']), action_time, nb_result]], columns=["uic_station", "request_time","Nb_Results"])
		requests_time = requests_time.append(b)
		print(requests_time)

	except requests.ConnectionError:
		print(row['stop_id'], " : aucun voyage possible")
		action_time = time.time() - looptime
		# print(action_time)
		nb_result = len(a)
		b = pd.DataFrame([[int(row['stop_id']), action_time, nb_result]],
						 columns=["uic_station", "request_time", "Nb_Results"])
		requests_time = requests_time.append(b)
		print(requests_time)
		continue




final_df.to_csv('test_save1.csv',header=True,index=False,sep=';')
requests_time.to_csv('request_time.csv',header=True,Index=False,sep=';')
print(time.time() - start)