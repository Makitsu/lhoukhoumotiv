#Scrap France city blasons from "https://armorialdefrance.fr"
from bs4 import BeautifulSoup as bs
from string import *
import pickle
from requests_html import HTMLSession
import os
from urllib import request
from time import *
import csv
import pandas as pd
import re

def saveAlphabet(alphabet):
    with open('alphabet', mode='wb') as file:
        my_pyckler = pickle.Pickler(file)
        my_pyckler.dump(alphabet)

def loadAlphabet():
    with open('alphabet', mode='rb') as file:
        my_unpickler = pickle.Unpickler(file)
        alphabet = my_unpickler.load()
    return alphabet


# SCRAPPER MAIN #

#Scrapper parameters
INITIATE_alphabet = True
indexURL = "https://armorialdefrance.fr/liste_alpha.php?initiale="
Errors = []

#Load most populated France communes
file = pd.read_csv('communes.csv', sep =";",encoding='windows-1252')

#Loop on list of communes
for i, j in file.iterrows():
    first_letter = j[2][0]

    # HTML page loading
    session = HTMLSession()  # create an HTML Session object
    resp = session.get(indexURL+first_letter)  # Use the object above to connect to needed webpage
    # HTML data extraction
    soup = bs(resp.html.html, 'lxml')
    session.close()

    # retrieve searched city link
    links_page = soup.find(attrs={'class':"en_retrait"})
    result = links_page.find("a", string = j[2].upper())

    try:
        link = "https://armorialdefrance.fr/" + result.get('href')
        print(link)

        # HTML page loading
        session = HTMLSession()  # create an HTML Session object
        resp = session.get(link)  # Use the object above to connect to needed webpage

        # HTML data extraction
        soup = bs(resp.html.html, 'lxml')
        session.close()

        # final data extraction

        #check existence of image directory
        dirname = os.path.dirname(__file__)
        blasondirname = dirname + "/images/blasons"
        test = os.path.exists(blasondirname)
        if not test:
            print("new blason directory is created")
            os.mkdir(blasondirname)

        data = soup.find_all('div',{"id":"corps"})[1]
        blason_pathname = "images/blasons/" + data.find('b').contents[0].strip().replace("/","-") +".jpg"
        blason_image_link = data.find('img')['href']
        request.urlretrieve(blason_image_link, blason_pathname)

        #Following script progress
        print(j[2], "has been processed\n")
    except AttributeError:
        Errors.append(j[2])
        pass

print(Errors)


