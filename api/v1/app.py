#!/usr/bin/python3
'''The flask app that will run on the server'''
from flask import Flask
from api.v1.views import app_views
from models import storage
import os
from flask import jsonify

app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exc):
    '''teardown closing storage'''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
