# -*- coding: utf-8 -*-
from urllib import request
from urllib.request import urlretrieve
import wikipedia as w
from bs4 import BeautifulSoup as bs
from bs4 import UnicodeDammit
import re
import pandas as pd
import os

#Script parameters
retrieve_images = 'yes'
retrieve_general_infos = 'no'

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
        imagedirname = dirname + "/images"
        test = os.path.exists(imagedirname)
        if not test:
            print("new image directory is created")
            os.mkdir(imagedirname)

        # retrieve image URL and format URL into urllib exigence ('http:')
        try:
            image_URL = "http:" + mytable.find('img', )["srcset"].split(" ")[0]
            image_name = 'images/' + row['title'] + '.jpg'  # build the image file name
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

