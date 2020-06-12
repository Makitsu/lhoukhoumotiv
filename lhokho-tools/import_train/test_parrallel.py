import __init__
import multiprocessing
import pandas as pd
import time
import requests
import datetime
from .test_normal import *

_USER_AGENT = ['CaptainTrain/1510236308(web) (Ember 2.12.2)',
               'CaptainTrain/5221(d109181b0) (iPhone8,4; iOS 13.1.2; Scale/2.00)',
               'CaptainTrain/1574360965(web) (Ember 3.5.1)']
               #'CaptainTrain/43(4302) Android/4.4.2(19)']


final_df = pd.DataFrame(
    columns=["destination", "departure_date", "arrival_date", "duration", "number_of_segments", "price", "currency",
             "transportation_mean"])
requests_time = pd.DataFrame(columns=["uic_station", "request_time"])

start = time.time()
fixed_time = datetime.datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")

def connections(station_uic):
    df_connection = pd.DataFrame(columns=["station_uic_dest"])
    df = pd.read_csv('connections.csv', sep=';')

    for index, row in df.iterrows():
        if row['stop_uic'] == station_uic:
            connections = row['connections'].replace('[', ''). \
                replace(']', '').split(', ')
            for connection in connections:
                df_temp = pd.DataFrame([[connection]], columns=["station_uic_dest"])
                df_connection = df_connection.append(df_temp)

    return df_connection

departure_id = 87113001
df_connections = connections(departure_id)

def worker(departure_station, arrival_station,looptime,waittime,user_nb,q):
    print('Worker: ', departure_station, ' -> ', arrival_station,'sleep during ',waittime)
    print('user: ',_USER_AGENT[user_nb])
    data_df = pd.DataFrame(
        columns=["destination", "departure_date", "arrival_date", "duration", "number_of_segments", "price", "currency",
                 "transportation_mean"])
    check_time_df = pd.DataFrame(columns=["uic_station", "request_time"])
    time.sleep(waittime)
    try:
        resultats = __init__.search(
            departure_station=str(departure_station),
            arrival_station=str(arrival_station),
            from_date="02/05/2020 08:00",
            to_date="02/05/2020 21:00",
            user_agent=_USER_AGENT[user_nb])

        a = resultats.df()
        data_df = data_df.append(a)
        data_df = data_df.fillna(arrival_station)
        print(data_df)
        q.put(data_df)
        #print('length of queue : ',q)
        print(arrival_station, ": terminé")
        action_time = time.time() - looptime
        print("Temps total requête : ", action_time)

    except requests.ConnectionError as e:
        print(arrival_station, " : aucun voyage possible - {}".format(e))
        action_time = time.time() - looptime
        print("Temps total requête (error - connection) : ", action_time)
        pass

    except TimeoutError:
        action_time = time.time() - looptime
        print("Temps total requête (error - TimeOut) : ", action_time)
        pass
    """thread worker function"""

    return check_time_df,data_df

def listener(q):
    final_df = pd.DataFrame(q.get(),
        columns=["destination", "departure_date", "arrival_date", "duration", "number_of_segments", "price", "currency",
                 "transportation_mean"])
    '''listens for messages on the q, writes to file. '''
    print('print into csv file')
    print(final_df)

if __name__ == '__main__':
    jobs = []
    # must use Manager queue here, or will not work
    manager = multiprocessing.Manager()
    q = manager.Queue()
    pool = multiprocessing.Pool(4)
    # put listener to work first
    watcher = pool.apply_async(listener, (q,))

    waittime = 0
    user_nb = 0
    for index, row in df_connections.iterrows():
        looptime = time.time()
        job = pool.apply_async(worker, (departure_id,row['station_uic_dest'],looptime,waittime,user_nb, q))
        #p = multiprocessing.Process(target=worker, args=(d))
        if user_nb == 2:
            user_nb = 0
            waittime = 0
        else:
            user_nb += 1
            waittime += 0
        jobs.append(job)
    # for job in jobs:
    #     job.start()
    # collect results from the workers through the pool result queue
    for job in jobs:
        job.get()

    pool.close()
    pool.join()

    print('\npopping items from queue:')
    cnt = 0
    while not q.empty():
        print('item no: ', cnt)
        cnt += 1
        final_df = q.get()
        print(final_df)
        final_df.to_csv('../temp/tl_export_{}.csv'.format(fixed_time), header=True, index=False, sep=';', mode='a')


    #requests_time.to_csv('../temp/request_time_{}.csv'.format(datetime), header=True, index=False, sep=';')
    print(time.time() - start)







