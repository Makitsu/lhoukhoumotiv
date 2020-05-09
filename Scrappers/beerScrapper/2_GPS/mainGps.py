"""
    Takes bars address and converts them into GPS coordinates
    Saves 3 files : latitude_data and longitude_data
"""

from geopy import Nominatim
import csv

counter = 0
# There is a limited number of access to Nominatim (about one thousand). Multiple run of the script is neeeded (using VPN)
Initialisation = False
# if Initialisation is False, scripts takes the saved progress of the work for re-run

if Initialisation is False:
    with open('progress', mode='rb') as file:
        progress = int(file.read())
else:
    progress = 0

#Load file
with open("../1_mainScrapper/data.csv", mode='r', newline='', encoding='utf-8') as data:
    data = csv.DictReader(data, delimiter=';', fieldnames=['name', 'address', 'HH_start', 'HH_end', 'confidence_index'])


    while progress > counter:
        next(data)
        counter +=1

    while True:
        try:
            if counter%200 == 0: # print progress every 200 adresses processed
                print(counter, 'adresses ont été traitées')

            #call of Nomatim to generates GPS coordinates from address
            row = next(data)
            address = row['address']
            geolocator = Nominatim(user_agent="my-application", timeout=10)
            location = geolocator.geocode(address)

            if location is None:     #If address not found, save latitude and longitude as TBD
                latitude = "TBD"
                longitude = "TBD"
                with open('latitude_data.csv', mode='a') as file:
                    file.write("TBD"+'\n')
                with open('longitude_data.csv', mode='a') as file:
                    file.write("TBD"+'\n')
            else:     #Else save it in two separate files
                latitude = location.latitude
                longitude = location.longitude
                with open('latitude_data.csv', mode='a') as file:
                    file.write(str(location.latitude)+'\n')
                with open('longitude_data.csv', mode='a') as file:
                    file.write(str(location.longitude)+'\n')

            # Save counter to be able to re-run the code where it has stopped
            counter += 1
            with open('progress', mode='w') as file:
                    file.write(str(counter))
            #print(counter, address, latitude, longitude)

        except StopIteration:
            print('Itération interrompu.', counter, ' lignes ont été traitées')
            break

