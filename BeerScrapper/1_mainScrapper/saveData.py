"""
    Contains all saving and loading functions
"""

import csv
import os
import pickle

def appendBar(info_bar):
    with open('data', mode='a', newline='', encoding='utf-8') as data:
        fieldnames = info_bar.keys()
        writer = csv.DictWriter(data, fieldnames=fieldnames,delimiter=';')
        if os.path.getsize('data')==0:
            writer.writeheader()
        writer.writerow(info_bar)

def loadData():
    with open("data.csv", mode='r', newline='') as data:
        data = csv.reader(data, delimiter=';')
        return data

def saveLinks(links):
    with open('links', mode='wb') as file:
        my_pyckler = pickle.Pickler(file)
        my_pyckler.dump(links)

def loadLinks():
    with open('links', mode='rb') as file:
        my_unpickler = pickle.Unpickler(file)
        links = my_unpickler.load()
    return links

def saveAlphabet(alphabet):
    with open('alphabet', mode='wb') as file:
        my_pyckler = pickle.Pickler(file)
        my_pyckler.dump(alphabet)

def loadAlphabet():
    with open('alphabet', mode='rb') as file:
        my_unpickler = pickle.Unpickler(file)
        alphabet = my_unpickler.load()
    return alphabet