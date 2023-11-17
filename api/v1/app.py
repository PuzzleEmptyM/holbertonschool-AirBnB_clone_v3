#!/usr/bin/python3
'''The flask app that will run on the server'''
from flask import Flask
from api.v1.views import app_views
from models import storage
import os


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exc):
    '''teardown closing storage'''
    storage.close()


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)