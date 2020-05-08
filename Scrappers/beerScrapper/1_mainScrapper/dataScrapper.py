"""
    functions useful to scrap and save :
        - BAR INFOS from mistergoodbeer bar pages
        - LINKS from mistergoodbeer alphabetical list of bar pages
"""

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re

def barScrapper(url):
    """
        - Scrap all bar infos from the inputed URL address
        - The data is saved in "data.csv" on the following "dict" format :
        {barName :  barAddress, HHStart, HHEnd, {beer1 : {HHprice, nHHprice, volume}, beer2 : {} ...}
    """
    while True:
        try:
            # HTML page loading with java
            session = HTMLSession()  # create an HTML Session object
            resp = session.get(url) # Use the object above to connect to needed webpage
            resp.html.render() # Run JavaScript code on webpage

            # HTML data extraction
            soup = BeautifulSoup(resp.html.html,'lxml')
            session.close()

            #General info about the bar
            general_info = soup.find(attrs={'class':'widget-pane-section-header'})
            name = general_info.find(attrs={'class':'widget-pane-section-header-hero-title'}).text #Nom du bar
            globals()[name]={} #Initialisation du dictionnaire de sauvegarde
            globals()[name]['name'] = name
            globals()[name]['address'] = general_info.find(attrs={'class':'widget-pane-section-header-hero-subtitle'}).text #addresse du bar
            HH = general_info.find_all(attrs={'class':'score-label'}) #Happy Hour
            if len(HH) == 1:
                HH = False
                globals()[name]['HH_start'] = 00
                globals()[name]['HH_end'] = 00
            else:
                HH = HH[1]
                HH = HH.find_all('span')[1] #Texte happy hour sous le format "de xxh à xxh"
                HH = HH.text.replace('minuit','24h')
                HH = HH.replace('h','') #Formatage du texte sous le format "de xx à xx"
                HH = [int(s) for s in HH.split() if s.isdigit()] #Extraction des heures de HH
                globals()[name]['HH_start'] = HH[0]
                globals()[name]['HH_end'] = HH[1]
            break
        except IndexError as e:
            print(e,'--> on reload la page')

    confidence_index = general_info.find(attrs={'class':'widget-pane-section-header-checks'})
    globals()[name]['confidence_index'] = [int(s) for s in confidence_index.text.split() if s.isdigit()][0]

    #Beers and Price info
    all_beers_info = soup.find(attrs={'class':'widget-pane-section-beer'})
    beer_items = all_beers_info.find_all(attrs={'class':'beer-item-container beer-item-container-clickable'})

    i=0
    beers = {}
    while i < len(beer_items):
        beer_item = beer_items[i]
        beer_name = beer_item.find(attrs={'class':'beer-item-container-name'}).text
        HH_attr = beer_item.find(attrs={'class':'beer-item-container-prices-price-item-happy-hour beer-item-container-prices-price-item'})
        if HH_attr is not None:
            beer_HH_price = HH_attr.find(attrs={'class':'beer-item-container-prices-price-item-price'}).text
        nHH_attr = beer_item.find(lambda tag: tag.name=='div' and tag.get('class')==['beer-item-container-prices-price-item']) #BeautifulSoup ne fait pas match exact --> on passe par une fonction lambda pour forcer l'exactitude
        if nHH_attr is not None:
            beer_nHH_price = nHH_attr.find(attrs={'class':'beer-item-container-prices-price-item-price'}).text
        volume_attr = beer_item.find(attrs={'class':'beer-icon-and-volume'})
        beer_volume = volume_attr.find_all('span')[1]
        beer_volume = beer_volume.text.split(" ")[0]
        beers[beer_name]={}
        if HH_attr is not None:
            beers[beer_name]['HHprice'] = beer_HH_price
        if nHH_attr is not None:
            beers[beer_name]['nHHprice'] = beer_nHH_price
        beers[beer_name]['volume'] = beer_volume
        i += 1

    beer_additional = all_beers_info.find(attrs={'beer-item-container-link'})
    if beer_additional is not None:
        beers['others'] = 'TBD'

#print('une erreur est survenue dans la récupération des données [barScrapper], barScrapper est relancé')

    globals()[name]['beers'] = beers
    return name, globals()[name]

def barsLinkScrapper(url):
    """
        - scrap bars link
        - save it in file
    """

    # HTML page loading with java
    session = HTMLSession()  # create an HTML Session object
    resp = session.get(url)  # Use the object above to connect to needed webpage
    print(resp)
    resp.html.render()  # Run JavaScript code on webpage

    # links data extraction
    links = []
    soup = BeautifulSoup(resp.html.html, 'lxml')
    page_items = soup.find(attrs={'class': 'columns is-multiline'})
    #print(page_items)
    for link in page_items.find_all('a',href = re.compile("^.app")):
        links.append(link.get('href'))
    return links