from datetime import date

import folium
import geocoder
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, app
import pandas as pd
from shapely import geometry
from .lib.import_train import Station
from .lib.import_tool import get_map_html
from .lib.map_tool.map_generator import ptp_map_serveur
import os

document_path = os.getcwd()+'\\lhoukhoum\\static\\connections.csv'
print(document_path)

connections_df = pd.read_csv(document_path, sep=";")


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
        return get_map_html(87113001)._repr_html_()
    elif request.method == 'POST':
        start_station = request.form.get('start_station')
        current_uic = Station().from_name(start_station).code_uic
        return get_map_html(current_uic)._repr_html_()

@bp.route('/station/map/absolute', methods=('GET', 'POST'))
def station_map_absolute():
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        start_station = request.form.get('start_station')
        stop_station = request.form.get('stop_station')
        print(start_station)
        print(stop_station)
        current_uic = Station().from_name(start_station).code_uic
        arrival_uic = Station().from_name(stop_station).code_uic

        return ptp_map_serveur(current_uic,arrival_uic)._repr_html_()

@bp.route('/station/info', methods=('GET', 'POST'))
def station_info():
    if request.method == 'GET':
        return "not used as get request"
    elif request.method == 'POST':
        document_path = os.getcwd() + '\\lhoukhoum\\static\\db\\db_2020-05-05.csv'
        print(document_path)
        #retrieve daily db
        db_df = pd.read_csv(document_path, sep=';')
        start_station = request.form.get('start_station')
        current_code = Station().from_name(start_station).code_fr
        print('current code is ',current_code)
        answer_df = db_df[db_df['departure_code'] == current_code]
        print(answer_df)
        answer = {
            'arrival_code': [],
            'price': answer_df['price'].tolist(),
            'type': answer_df['type'].to_list(),
            'category': answer_df['category'].tolist()
        }
        for elem in answer_df['arrival_code'].tolist():
            answer['arrival_code'].append(Station().from_code(elem).name)
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
