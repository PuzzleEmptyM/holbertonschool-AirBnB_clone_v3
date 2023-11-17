#!/usr/bin/python3
'''Handling RESTful API on state'''
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state_list():
    '''Retrieves the list of all states'''
    obj = storage.all('State').to_dict()
    return jsonify(obj)

@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id():
    '''Retrieves the state based on id'''
    try:
        