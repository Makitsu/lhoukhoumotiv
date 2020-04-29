import pandas as pd
import pandas

def connections(station_uic):
    df_connection = pd.DataFrame(columns=["station_uic_dest"])
    df = pandas.read_csv('connections.csv',sep=';')

    for index,row in df.iterrows():
        if row['stop_uic'] == station_uic:
            connections = row['connections'].replace('[','').\
                            replace(']','').split(', ')
            for connection in connections:
                df_temp = pd.DataFrame([[connection]],columns=["station_uic_dest"])
                df_connection = df_connection.append(df_temp)

    return df_connection