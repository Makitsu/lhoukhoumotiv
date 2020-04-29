import datetime

import pandas
import time

from .lib.import_tool import import_trip



#batch to retrieve price of ticket for all departure station
#
#frequency: every night
def batch_price():
    import_trip(datetime.datetime.now(),87113001)

#batch to retrieve price of ticket for all departure station
#
#frequency: every 30 days

def batch_schedule():
    print('to be implemented')
