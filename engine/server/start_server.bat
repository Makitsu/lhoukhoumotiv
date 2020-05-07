@ECHO OFF

set FLASK_APP=lhoukhoum
set FLASK_ENV=development
set SEND_FILE_MAX_AGE_DEFAULT=0
python -m flask run

start "http://127.0.0.1:5000/"

PAUSE