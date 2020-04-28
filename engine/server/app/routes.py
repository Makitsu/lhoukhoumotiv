from flask import Blueprint, render_template, request, redirect, url_for
from source.constants import station_list

bp = Blueprint('trip', __name__)

@bp.route('/', methods=('GET', 'POST'))
def homepage():
    if request.method == 'GET':
        # gender = request.args['gender']
        # years = request.args['years']
        # date = request.args['date']
        # location = request.args['location']
        # return render_template('intersecting_routes.html',
        #                        gender=gender,
        #                        years=years,
        #                        date=date,
        #                        location=location)
        return render_template('homepage.html', stations=station_list)
    elif request.method == 'POST':
        return redirect('/')


@bp.route('/station', methods=('GET', 'POST'))
def station():
    if request.method == 'GET':
        return "to be implemented"
    elif request.method == 'POST':
        return redirect('/')

@bp.route('/station/map', methods=('GET', 'POST'))
def station_map():
    if request.method == 'GET':
        return "to be implemented"
    elif request.method == 'POST':
        return redirect('/')


@bp.route('/trip', methods=('GET', 'POST'))
def trip():
    if request.method == 'GET':
        return "to be implemented"
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