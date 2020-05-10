# -*- coding: utf-8 -*-
import random
from urllib import request
from urllib.request import urlretrieve
import wikipedia as w
from bs4 import BeautifulSoup as bs
from bs4 import UnicodeDammit
import re
import pandas as pd
import os

#Script parameters
retrieve_images = 'no'
retrieve_general_infos = 'yes'
_STOP_CITY = ['Vannes', 'Auray', 'Lorient', 'Vitré', 'Quimper', 'Quimperlé', 'Rosporden', 'Saint-Malo', 'Dol-de-Bretagne', 'La Roche-sur-Yon', 'Saint-Nazaire', 'La Baule-Escoublac', 'Le Croisic', 'Pornichet', 'Le Pouliguen', 'Sablé-sur-Sarthe', "Les Sables-d'Olonne", 'Biganos', 'Arcachon', 'La Teste-de-Buch', 'Libourne', 'Vendôme', 'Châtellerault', 'Dax', 'Bayonne', 'Biarritz', 'Saint-Jean-de-Luz', 'Hendaye', 'Niort', 'Surgères', 'La Rochelle', "Saint-Maixent-l'École", 'Chasseneuil-du-Poitou', 'Tours', 'Orthez', 'Pau', 'Lourdes', 'Tarbes']

def scrapping_online_list():
    # 1. Grab  the list from wikipedia.
    w.set_lang('fr')
    s = w.page(w.search('Liste des communes de France les plus peuplées')[0])
    print(type(s.url))
    html = request.urlopen(s.url).read()
    soup = bs(html, 'html.parser')
    
    summary = {'title':[],
               'link':[]
               }
    
    mytable = soup.findAll('table')[0].tbody
    for row in mytable.find_all("tr")[1:]:
        col = row.find_all("td")
        try:
            link = col[2].find('a')
            summary['title'].append(link.get('title'))
            summary['link'].append('https://fr.wikipedia.org' + link.get('href'))
        except IndexError:
            pass
    
    df = pd.DataFrame.from_dict(summary)
    print(df)
    result = {'ville' : [],
              'region' : [],
              'departement':[],
              'population':[],
              'population_aire' : [],
              'densite':[],
              'gentile':[],
              'altitude':[],
              'superficie':[]
              #'image_src':[]
              }
    for index, row in df.iterrows():
        #print(row['link'])
        page = bs(request.urlopen(row['link']).read(), 'html.parser',from_encoding="utf-8")
        print(page.original_encoding)
        mytable = page.find("table", class_="infobox_v2")
    
        # retrieve cities presentation images
        if retrieve_images == 'yes':
    
            #check existence of image directory
            dirname = os.path.dirname(__file__)
            imagedirname = dirname + "/images/wiki"
            test = os.path.exists(imagedirname)
            if not test:
                print("new image directory is created")
                os.mkdir(imagedirname)
    
            # retrieve image URL and format URL into urllib exigence ('http:')
            try:
                image_URL = "http:" + mytable.find('img', )["srcset"].split(" ")[0]
                image_name = 'images/wiki/' + row['title'] + '.jpg'  # build the image file name
                request.urlretrieve(image_URL, image_name)  # save the image in local file
            except AttributeError:
                print(row['title'], "is so worthless it doesn't deserve an image on wiki")
    
        # retrieve cities general info
        if retrieve_general_infos == 'yes':
            result['ville'].append(row['title'])
            departement_found = 0
            region_found = 0
            population_found = 0
            pop_aire_found = 0
            densite_found = 0
            gentile_found = 0
            altitude_found = 0
            superficie_found = 0
            #image_found = 0
            try:
                for tr in mytable.findAll('tr'):
                    #trText = tr.text
                    try:
                        a = tr.find('th').find('a')
                        if 'title' in a.attrs:
                            if a['title'] == "Région française":
                                region_found =+ 1
                                b = tr.find('td').find('a')
                                result['region'].append(b.string)
                            if a['title'] == "Département français":
                                departement_found =+ 1
                                b = tr.find('td').find('a')
                                result['departement'].append(b.string)
                            if a['title'] == "Chiffres de population de la France":
                                population_found =+ 1
                                b = tr.find('td')
                                b = b.contents[0].replace(u'\xa0', u'')
                                result['population'].append(b)
                            if a['title'] == "Aire urbaine (France)":
                                pop_aire_found =+ 1
                                b = tr.find('td')
                                b = b.contents[0].replace(u'\xa0', u'')
                                result['population_aire'].append(b)
                            if a['title'] == "Densité de population":
                                densite_found =+ 1
                                b = tr.find('td')
                                b = b.contents[0].replace(u'\xa0', u'')
                                result['densite'].append(b)
                            if a['title'] == "Gentilé":
                                gentile_found =+ 1
                                b = tr.find('td')
                                b = b.text.replace('\n', '')
                                result['gentile'].append(b)
                            if a['title'] == "Altitude":
                                altitude_found =+ 1
                                b = tr.find('td')
                                b = b.text.replace('\xa0', '').replace('\n','')
                                result['altitude'].append(b)
                            if a['title'] == "Aire (géométrie)":
                                superficie_found =+ 1
                                b = tr.find('td')
                                b = b.text.replace('\xa0', '').replace("\n","")
                                result['superficie'].append(b)
                    except AttributeError:
                        continue
                    except KeyError:
                        continue
            except AttributeError:
                if departement_found == 0:
                    result['departement'].append("N/A")
                if region_found == 0:
                    result['region'].append("N/A")
                if population_found == 0:
                    result['population'].append("N/A")
                if pop_aire_found == 0:
                    result['population_aire'].append("N/A")
                if densite_found == 0:
                    result['densite'].append("N/A")
                if gentile_found == 0:
                    result['gentile'].append("N/A")
                if altitude_found == 0:
                    result['altitude'].append("N/A")
                if superficie_found == 0:
                    result['superficie'].append("N/A")
                continue
            if departement_found == 0:
                result['departement'].append("N/A")
            if region_found == 0:
                result['region'].append("N/A")
            if population_found == 0:
                result['population'].append("N/A")
            if pop_aire_found == 0:
                result['population_aire'].append("N/A")
            if densite_found == 0:
                result['densite'].append("N/A")
            if gentile_found == 0:
                result['gentile'].append("N/A")
            if altitude_found == 0:
                result['altitude'].append("N/A")
            if superficie_found == 0:
                result['superficie'].append("N/A")
            # if image_found == 0:
            #     result['image_src'].append("N/A")
            print(result)
    
        df = pd.DataFrame.from_dict(result)
        df.to_csv('results_wikiscrapping.csv',sep=";")

def scrapping_station_list():
    result = {'ville': [],
              'region': [],
              'departement': [],
              'population': [],
              'densite': [],
              'gentile': [],
              'altitude': [],
              'superficie': []}
    for elem in _STOP_CITY:
        w.set_lang('fr')
        print(elem + '(ville)')
        result['ville'].append(elem)
        try:
            s = w.page(w.search(elem,results=1,suggestion=False)[0])
        except w.DisambiguationError as e:
            print(e.options)
            s = min(e.options, key=len) + '(ville)'
            print(s)
            s = w.page(s)
        except w.PageError:
            try:
                s = w.page(elem)
            except w.PageError:

                print(elem, ' - Entrer le département')
                x = input()
                result['departement'].append(x)
                print(elem, ' - Entrer la région')
                x = input()
                result['region'].append(x)
                print(elem, ' - Entrer la population')
                x = input()
                result['population'].append(x)
                print(elem, ' - Entrer la densité')
                x = input()
                result['densite'].append(x)
                print(elem, ' - Entrer le gentillé')
                x = input()
                result['gentile'].append(x)
                print(elem, ' - Entrer altitude')
                x = input()
                result['altitude'].append(x)
                print(elem, ' - Entrer superficie')
                x = input()
                result['superficie'].append(x)

                continue
        print(s.url)
        print(s.title)
        html = request.urlopen(s.url).read()
        page = bs(html, 'html.parser',from_encoding="utf-8")
        mytable = page.find("table", class_="infobox_v2")

        # retrieve cities presentation images
        if retrieve_images == 'yes':
            images = page.findAll('img')
            allow = (".jpg", '.JPG')
            # check existence of image directory
            dirname = os.path.dirname(__file__)
            imagedirname = dirname + "/images/wiki_from_list"
            test = os.path.exists(imagedirname)
            if not test:
                print("new image directory is created")
                os.mkdir(imagedirname)

            # retrieve image URL and format URL into urllib exigence ('http:')
            for image in images:
                try:
                    img_src = 'http:' + image['srcset'].split(" ")[0]
                    print(img_src)
                    if img_src.endswith(allow):
                        image_name = 'images/wiki_from_list/' + elem + '.jpg'  # build the image file name
                        request.urlretrieve(img_src, image_name)  # save the image in local file
                        print('cest la bonne michou : ', img_src)
                        break
                except AttributeError:
                    print("Attribute error - Loupé c'est balot")
                    break
        # retrieve cities general info
        if retrieve_general_infos == 'yes':
            departement_found = 0
            region_found = 0
            population_found = 0
            densite_found = 0
            gentile_found = 0
            altitude_found = 0
            superficie_found = 0
            # image_found = 0
            try:
                for tr in mytable.findAll('tr'):
                    # trText = tr.text
                    try:
                        a = tr.find('th').find('a')
                        if 'title' in a.attrs:
                            if a['title'] == "Région française":
                                region_found = + 1
                                b = tr.find('td').find('a')
                                result['region'].append(b.string)
                            if a['title'] == "Département français":
                                departement_found = + 1
                                b = tr.find('td').find('a')
                                result['departement'].append(b.string)
                            if a['title'] == "Chiffres de population de la France":
                                population_found = + 1
                                b = tr.find('td')
                                b = b.contents[0].replace(u'\xa0', u'')
                                result['population'].append(b)
                            if a['title'] == "Densité de population":
                                densite_found = + 1
                                b = tr.find('td')
                                b = b.contents[0].replace(u'\xa0', u'')
                                result['densite'].append(b)
                            if a['title'] == "Gentilé":
                                gentile_found = + 1
                                b = tr.find('td')
                                b = b.text.replace('\n', '')
                                result['gentile'].append(b)
                            if a['title'] == "Altitude":
                                altitude_found = + 1
                                b = tr.find('td')
                                b = b.text.replace('\xa0', '').replace('\n', '')
                                result['altitude'].append(b)
                            if a['title'] == "Aire (géométrie)":
                                superficie_found = + 1
                                b = tr.find('td')
                                b = b.text.replace('\xa0', '').replace("\n", "")
                                result['superficie'].append(b)
                    except AttributeError:
                        continue
                    except KeyError:
                        continue
            except AttributeError:
                print('Attribute Error')
                if departement_found == 0:
                    print(elem, ' - Entrer le département')
                    x = input()
                    departement_found = + 1
                    result['departement'].append(x)
                if region_found == 0:
                    print(elem, ' - Entrer la région')
                    x = input()
                    region_found =+1
                    result['region'].append(x)
                if population_found == 0:
                    print(elem, ' - Entrer la population')
                    x = input()
                    population_found =+1
                    result['population'].append(x)
                if densite_found == 0:
                    print(elem, ' - Entrer la densité')
                    x = input()
                    densite_found =+ 1
                    result['densite'].append(x)
                if gentile_found == 0:
                    print(elem, ' - Entrer le gentillé')
                    x = input()
                    gentile_found =+ 1
                    result['gentile'].append(x)
                if altitude_found == 0:
                    print(elem, ' - Entrer altitude')
                    x = input()
                    altitude_found =+ 1
                    result['altitude'].append(x)
                if superficie_found == 0:
                    print(elem, ' - Entrer superficie')
                    x = input()
                    superficie_found =+ 1
                    result['superficie'].append(x)
                continue
            except:
                print('General except for ', elem)
                if departement_found == 0:
                    print(elem, ' - Entrer le département')
                    x = input()
                    result['departement'].append(x)
                if region_found == 0:
                    print(elem, ' - Entrer la région')
                    x = input()
                    result['region'].append(x)
                if population_found == 0:
                    print(elem, ' - Entrer la population')
                    x = input()
                    result['population'].append(x)
                if densite_found == 0:
                    print(elem, ' - Entrer la densité')
                    x = input()
                    result['densite'].append(x)
                if gentile_found == 0:
                    print(elem, ' - Entrer le gentillé')
                    x = input()
                    result['gentile'].append(x)
                if altitude_found == 0:
                    print(elem, ' - Entrer altitude')
                    x = input()
                    result['altitude'].append(x)
                if superficie_found == 0:
                    print(elem, ' - Entrer superficie')
                    x = input()
                    result['superficie'].append(x)
                continue
            print('Elem manquant pour : ', elem)
            if departement_found == 0:
                print(elem, ' - Entrer le département')
                x = input()
                result['departement'].append(x)
            if region_found == 0:
                print(elem, ' - Entrer la région')
                x = input()
                result['region'].append(x)
            if population_found == 0:
                print(elem, ' - Entrer la population')
                x = input()
                result['population'].append(x)
            if densite_found == 0:
                print(elem, ' - Entrer la densité')
                x = input()
                result['densite'].append(x)
            if gentile_found == 0:
                print(elem, ' - Entrer le gentillé')
                x = input()
                result['gentile'].append(x)
            if altitude_found == 0:
                print(elem, ' - Entrer altitude')
                x = input()
                result['altitude'].append(x)
            if superficie_found == 0:
                print(elem, ' - Entrer superficie')
                x = input()
                result['superficie'].append(x)
            print(result)
            df = pd.DataFrame.from_dict(result)
            print(df)
            df.to_csv('results_wikiscrapping_final_3.csv', sep=";",header=False)

df = pd.read_csv('results_wikiscrapping_final.csv',sep=';')

print(df['gentile'])