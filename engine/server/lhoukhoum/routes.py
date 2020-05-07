from datetime import date

import folium
import geocoder
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, app
import pandas as pd
from shapely import geometry
from .lib.import_train import Station
from .lib.import_tool import get_map_html
from .lib.map_tool.map_generator import map_from_list, map_from_departure
from .lib.import_train.test_normal import search_fares
import os

document_path = os.getcwd() + '\\lhoukhoum\\static\\connections.csv'
print(document_path)

connections_df = pd.read_csv(document_path, sep=";")

city = 'Not defined'

bp = Blueprint('trip', __name__)


@bp.route('/', methods=('GET', 'POST'))
def homepage():
    if request.method == 'GET':
        return render_template('index.html', stations=Station()._get_stations_name())
    elif request.method == 'POST':
        return redirect('/')


@bp.route('/station', methods=('GET', 'POST'))
def station():
    if request.method == 'GET':
        return "to be implemented"
    elif request.method == 'POST':
        return redirect('/')


@bp.route('/station/destination/<city>', methods=('GET', 'POST'))
def station_destination(city):
    if request.method == 'GET':
        return render_template('destination.html', city=city)
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
        print(price_df)
        answer = {
            'arrival_code': price_df['name_arrival'].tolist(),
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


@bp.route('/destination', methods=['GET', 'POST'])
def destination():
    if request.method == 'POST':
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('destination.html')

@bp.route('/station/info',methods=['GET', 'POST'])
def station_info():
    document_path = os.getcwd() + '\\lhoukhoum\\static\\db\\results_wikiscrapping.csv'
    summary_info = pd.read_csv(document_path, sep=';', index_col=1)
    info = summary_info.to_dict('index')
    if request.method == 'POST':
        station = request.form.get('city_name')
        answer = {'city_name' : station,
                  'region' : info[station]['region'],
                  'departement' : info[station]['departement'],
                  'population' : info[station]['population'],
                  'densite' : info[station]['densite'],
                  'gentile' : info[station]['gentile'],
                  'altitude' : info[station]['altitude'],
                  'superficie' : info[station]['superficie'],
                  'city_img' : "url(/static/img/{}.jpg)".format(station)
        }
        print('city')
        print(answer)
        return answer

