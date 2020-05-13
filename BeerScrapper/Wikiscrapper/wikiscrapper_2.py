# -*- coding: utf-8 -*-
from urllib import request
from urllib.request import urlretrieve
import wikipedia as w
from bs4 import BeautifulSoup as bs
from bs4 import UnicodeDammit
import re
import pandas as pd
import os
import difflib

result = {'initial_search':[],
          'name' : [],
          #'ratio' : [],
          'ville' : [],
          'type' : [],
          'summary' : [],
          'image_src':[],
          'wiki_link':[]}
#Script parameters
retrieve_images = 'yes'
retrieve_general_infos = 'no'
df = pd.read_csv('city_items.csv',sep=';')
print(df)
for index, row in df.iterrows():
    title_found = 0
    link_found = 0
    summary_found = 0
    image_found = 0
    #ratio_found = 0
    try:
        result['initial_search'].append(row['name'])
        result['ville'].append(row['city'].capitalize())
        result['type'].append(row['type'])
        # 1. Grab  the list from wikipedia.
        w.set_lang('fr')
        search = row['name'] + ' ' + '(' + row['city'] + ')'
        print(row['name'])
        search = w.search(search, results=5)
        s = w.page(search[0])
        print(search[0])
        ratio = difflib.SequenceMatcher(None, row['name'], search[0]).ratio()
        if ratio < 0.5:
            print("Warning ratio : ", ratio, "Vérifier url")
            print(s.url)
            print("[INTERGER !] Please change in the list below (order number) or enter 'p' to dismiss")
            new_search = w.search(row['name'],results=20)
            print(new_search)
            answer = input()
            if answer != 'p':
                s = w.page(new_search[int(answer)])
                print('new name : ', s.title)
        result['name'].append(s.title)
        title_found = 1
        summary = str(s.summary).splitlines()[0]
        print(summary)
        result['summary'].append(summary)
        summary_found = 1
        result['wiki_link'].append(s.url)
        link_found = 1
        print(s.title)
        print(s.url)
        html = request.urlopen(s.url).read()
        soup = bs(html, 'html.parser',from_encoding="utf-8")
        images = soup.findAll('img')
        allow = (".jpg", '.JPG')
        for image in images:
            try:
                source = image['src']
                print("http:" + source)
                if source.endswith(allow):
                    result['image_src'].append("http:" + source)
                    print('cest la bonne michou : ',"http:",source)
                    image_found =+ 1
                    break
            except AttributeError:
                print("attribute error with image - break")
                break
        if image_found == 0:
            result['image_src'].append("n/a")
        print(result)
        df = pd.DataFrame.from_dict(result)
        print(df)
        df.to_csv('list_city_items_3.csv', sep=";")
    except (w.exceptions.WikipediaException,w.exceptions.DisambiguationError,w.exceptions.PageError, IndexError, ValueError):
        if title_found == 0:
            result['name'].append('n/a')
        if image_found == 0:
            result['image_src'].append("n/a")
        if link_found == 0:
            result['wiki_link'].append("n/a")
        if summary_found == 0:
            result['summary'].append("n/a")
        print(result)
        df = pd.DataFrame.from_dict(result)
        print(df)
        df.to_csv('list_city_items_3.csv', sep=";")
df.drop_duplicates(subset=['name', 'ville'], keep='first')
df.to_csv('list_city_items_3.csv', sep=";")