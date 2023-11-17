#!/usr/bin/python3
'''Returns the json ok status'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    '''returns the json ok status'''
    return jsonify({'status': 'OK'})
