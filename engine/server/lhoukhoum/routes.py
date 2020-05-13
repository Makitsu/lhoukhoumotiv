from datetime import date

import folium
import geocoder
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
import pandas as pd
from shapely import geometry
from .lib.import_train import Station
from .lib.import_tool import get_map_html
from .lib.map_tool.map_generator import map_from_list, map_from_departure
from .lib.import_train.test_normal import search_fares
import os

city = 'Not defined'

bp = Blueprint('trip', __name__)


@bp.route('/', methods=('GET', 'POST'))
def homepage():
    if request.method == 'GET':
        if session['live'] == True:
            return render_template('index.html', stations=Station()._get_stations_name())
        else:
            return render_template('homepage.html')
    elif request.method == 'POST':
        return redirect('/')

@bp.route("/alive", methods=["POST", "GET"])
def alive():
    if request.method == "GET":
        session.permanent = True
        return session['live']
    else:
        return redirect('/')

@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form.get('user')
        password = request.form.get('password')
        print('attempt connection user: ',user)
        if user in session["user"]:
            idx = session["user"].index(user)
            if password in session["password"]:
                session['live'] = True
                redirect('/')
                return jsonify([session['details'][idx]])
            else:
                return 'wrong password'
        else:
            return 'user not registered'
    else:
        return redirect('/')

@bp.route("/logout", methods=["POST", "GET"])
def logout():
    if request.method == "POST":
        session.permanent = True
        session['live'] = False
        return redirect('/')
    else:
        return redirect('/')

@bp.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        session.permanent = True
        user = request.form.get('user')
        password = request.form.get('password')
        print('attempt register user: ', user)
        print(session['user'])
        if user in session["user"]:
            return 'user already registered'
        else:
            session['user'].append(user)
            session['password'].append(password)
            session['details'].append([])
            return 'user created'

    else:
        return redirect('/')


@bp.route('/session')
def updating_session():
    print('refresh session')
    session['live'] = False
    session['user'] = ['maxime']
    session['password'] = ['maxtoo']
    session['details']=[]
    user_details = {'nom': 'maxime',
                    'prenom': 'lhoumeau',
                    'age': '25',
                    'user-id': '311900723',
                    'cards': ['TGV MAX'],
                    'cards-id': ['13653993'],
                    'token': 'MA6GdheENfAnQjoHGyC3'
                    }
    session['details'].append(user_details)
    res = str(session.items())
    return res





@bp.route('/destination', methods=('GET', 'POST'))
def destination():
    if request.method == 'GET':
        city = request.args.get('city')
        destination = city.capitalize()
        print(destination)
        return render_template('destination.html', city=destination)
    elif request.method == 'POST':
        return redirect('/')



@bp.route('/station/connection', methods=('GET', 'POST'))
def station_connection():
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        start_station = request.form.get('start_station')
        current_station = Station().from_name(start_station)
        return jsonify(current_station._get_connection_name())


@bp.route('/station/map', methods=('GET', 'POST'))
def station_map():
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        start_station = request.form.get('start_station')
        current_uic = Station().from_name(start_station).code_uic
        return map_from_departure(current_uic)._repr_html_()


@bp.route('/station/map/selection', methods=('GET', 'POST'))
def station_map_absolute():
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        print(request.form)
        start_station = request.form.get('start_station')
        stop_station = str(request.form.get('stop_station')).split(',')
        print(start_station)
        print(stop_station)
        print(len(stop_station))
        current_uic = Station().from_name(start_station).code_uic
        stops_uic = []
        for station in stop_station:
            stops_uic.append(Station().from_name(station).code_uic)

        return map_from_list(current_uic, stops_uic)._repr_html_()


@bp.route('/station/price', methods=('GET', 'POST'))
def station_price():
    if request.method == 'GET':
        return "not used as get request"
    elif request.method == 'POST':
        start_station = request.form.get('start_station')
        stop_station = request.form.get('stop_station')
        select_date = request.form.get('trip_date')

        start_tl = Station().from_name(start_station).code_tl
        stop_tl = Station().from_name(stop_station).code_tl
        passengers = [{'id': '3c29a998-270e-416b-83f0-936b606638da', 'age': 39,
                       'cards': [], 'label': '3c29a998-270e-416b-83f0-936b606638da'}]
        print('current code is ', start_tl)
        price_df = search_fares(select_date, start_tl, stop_tl, passengers, True)
        price_df['cents'] = price_df['cents'] / 100
        price_df.sort_values(by=['cents'], inplace=True, ascending=True)
        cities = []
        for station in price_df['name_arrival'].tolist():
            cities.append(Station().from_name(stop_station).city)

        answer = {
            'city': cities,
            'time': price_df['departure_date'].tolist(),
            'price': price_df['cents'].tolist(),
            'type': price_df['train_name'].to_list(),
            'category': price_df['travel_class_seg'].tolist()
        }

        return jsonify(answer)


@bp.route('/trip', methods=('GET', 'POST'))
def trip():
    if request.method == 'GET':
        return render_template('index.html', stations=Station()._get_stations_name())
    elif request.method == 'POST':
        return redirect('/')


@bp.route('/trip/map', methods=('GET', 'POST'))
def trip_map():
    if request.method == 'GET':
        departure_station = request.args['years']
        departure = request.args['date']
        return "to be implemented"
    elif request.method == 'POST':
        return redirect('/')


@bp.route('/station/info', methods=['GET', 'POST'])
def station_info():
    document_path = os.getcwd() + '\\lhoukhoum\\static\\db\\results_wikiscrapping.csv'
    document_path2 = os.getcwd() + '\\lhoukhoum\\static\\db\\results_wikiscrapping2.csv'
    summary_info = pd.read_csv(document_path, sep=';',index_col=0)
    dest = request.form.get('city_name')
    print(dest)
    info = summary_info[summary_info['ville'] == dest].iloc[0] #first row of filtered df
    if request.method == 'POST':
        answer = {'city_name': dest,
                  'region': info['region'],
                  'departement': info['departement'],
                  'population': info['population'],
                  'densite': info['densite'],
                  'gentile': info['gentile'],
                  'altitude': info['altitude'],
                  'superficie': info['superficie'],
                  'city_img': "url(/static/img/{}.jpg)".format(dest)
                  }
        print('city')
        print(answer)
        return answer
