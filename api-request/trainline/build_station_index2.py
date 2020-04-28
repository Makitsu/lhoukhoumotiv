import pandas as pd
import io
import requests
import numpy

_STATIONS_CSV_FILE = "https://raw.githubusercontent.com/\
trainline-eu/stations/master/stations.csv"

csv_content = requests.get(_STATIONS_CSV_FILE).content
df = pd.read_csv(io.StringIO(csv_content.decode('utf-8')),
                 sep=';', index_col=0, low_memory=False)
df = df[df.is_suggestable == 't']
df = df[df.country == 'FR']
df_mini = df.filter(['name','uic8_sncf'])
df_mini= df_mini[~numpy.isnan(df_mini['uic8_sncf'])]
df_mini['uic8_sncf'] =df_mini['uic8_sncf'].astype(int)
#df_mini = df_mini.join(df.filter(['uic8_sncf']))
df_mini['name'] = df_mini['name'].str.lower()
print(df_mini)
df_mini.to_csv("stations_mini5.csv", sep=';', encoding='utf-8', header=False, index=True)