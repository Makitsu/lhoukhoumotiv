"""               \o/ SAVE WATER DRINK BEER \o/
   main file for extracting bar and beer data from MisterGoodBeer
    - Loop on mistergoodbeer webpages to access bars in aphabetical order and extract infos from each bar
    - The data is saved in "data.csv" on the following "dict" format :
        {barName :  barAddress, HHStart, HHEnd, {beer1 : {HHprice, nHHprice, volume}, beer2 : {} ...}
"""

from dataScrapper import *
from saveData import *
from time import *
from string import *

"""Errors can occur as the script takes 5 hours to run, the two following variables allows to restart the script at the last iteration"""
INITIATE_alphabet = False
#if True, script loop from a to z, otherwise starts from the last letter of the previous run
INITIATE_links = False
#for each letter, a list of links (bar pages) is generated. If True, regenerate all the links corresponding to the letter, otherwise starts from the link the previous run stopped at

"""Generate links for list of bars beginning with letter 'i' or load the remaining list from previous iteration"""
if INITIATE_alphabet is True:
    alphabet = list(ascii_uppercase)
    alphabet = alphabet[3:] #Start from C
    saveAlphabet(alphabet)
else:
    alphabet = loadAlphabet()

""" Main loops : loop on generated links in the alphabet loop """
while len(alphabet)>0: # loop on alphabet

    # Extract corresponding bar URLs in the list or load it from previous iteration
    if INITIATE_links is True:
        bar_list_url = "https://www.mistergoodbeer.com/top-des-bars-en-" + alphabet[0] #Constructing letter i bar list URL
        links = barsLinkScrapper(bar_list_url) #Extracting bar suffix
        saveLinks(links)
    else:
        links = loadLinks()

    while len(links)>0: # loop on links
        bar_url = "https://www.mistergoodbeer.com" + links[0] #Constructing bar URL
        print('------------------------------------\n','URL en traitement :', bar_url)
        time_start=time()
        name_bar, info_bar = barScrapper(bar_url) #data extraction
        time_finish=time()
        appendBar(info_bar)
        links = links[1:]  #links list incrementation
        saveLinks(links)
        print('Le bar correspondant :', name_bar, 'a été traité avec succès!\n',time_finish-time_start,'s ont été nécessaires pour traiter ce bar\n', 'Bars restant à traiter :', len(links))

    alphabet = alphabet[1:]  # alphabet list incrementation
    saveAlphabet(alphabet)
    print('L\'ensemble des bars commençant par la lettre', alphabet[0], 'a été traitée\n La lettre suivante est alphabet(1)')
    INITIATE_links = True # We are changing letter so links have to be generated again

print('YOU ARE READY FOR DECONFINEMENT\n\o/       THE END         \o/')