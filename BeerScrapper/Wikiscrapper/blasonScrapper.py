#Scrap France city blasons from "https://armorialdefrance.fr"
from bs4 import BeautifulSoup as bs
from string import *
import pickle
from requests_html import HTMLSession
import os
from urllib import request
from time import *

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

if INITIATE_alphabet is True:
    alphabet = list(ascii_uppercase)
    alphabet = alphabet[0:] #Start from C
    saveAlphabet(alphabet)
else:
    alphabet = loadAlphabet()

indexURL = "https://armorialdefrance.fr/liste_alpha.php?initiale="

nb_total = 0
while len(alphabet)>0:
    tic = time()
    nb_commune = 0

    # HTML page loading with java
    session = HTMLSession()  # create an HTML Session object
    resp = session.get(indexURL+alphabet[0])  # Use the object above to connect to needed webpage

    # HTML data extraction
    soup = bs(resp.html.html, 'lxml')
    session.close()

    # retrieve link list for each alphabet letter
    links = []
    links_page = soup.find(attrs={'class':"en_retrait"})
    for link in links_page.find_all("a"):
        links.append("https://armorialdefrance.fr/" + link.get('href'))

        #iterate in each "commune" page
        for i in range(0,len(links)):

            # HTML page loading with java
            session = HTMLSession()  # create an HTML Session object
            resp = session.get(links[i])  # Use the object above to connect to needed webpage

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
            nb_commune +=1
            if nb_commune % 100 == 0:
                print(blason_image_link)

        nb_total += nb_commune
        toc = time()
        delay = toc - tic
    print('letter', alphabet[0],'has been processed\n',nb_commune, 'are beginning with this letter\n', nb_total, 'commune in total have been processed\n', delay, "has been necessary to this step" )

    alphabet = alphabet[1:]  # alphabet list incrementation
    saveAlphabet(alphabet)
