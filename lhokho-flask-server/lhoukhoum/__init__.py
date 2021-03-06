import atexit
import datetime
import time
import redis
from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template

from . import routes
from . import batch


def create_app():
    app = Flask(__name__,static_folder= 'static')
    app.secret_key = "hello"
    app.register_blueprint(routes.bp)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=5)
    app.config.update(
        DEBUG=True,
        TEMPLATES_AUTO_RELOAD=True,
        SESSION_TYPE='filesystem'
    )
    scheduler = BackgroundScheduler(daemon=True)
    #batch to retrieve data
    scheduler.add_job(batch.batch_price, 'interval', days=1,start_date=datetime.datetime.now().replace(minute=17))

    #batch to retrieve sncf schedule
    scheduler.add_job(func=batch.batch_schedule(), trigger="interval",
                      week=4,
                      start_date=datetime.datetime.now()
                      )
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    try:
        # To keep the main thread alive
        return app
    except:
        # shutdown if app occurs except
        scheduler.shutdown()

