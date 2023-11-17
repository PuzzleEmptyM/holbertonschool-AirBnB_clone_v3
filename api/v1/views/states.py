#!/usr/bin/python3
'''Handling RESTful API on state'''
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state_list():
    '''Retrieves the list of all states'''
    s_list = []
    obj = storage.all('State').values()
    for state in obj:
        s_list.append(state.to_dict())
    return jsonify(s_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    '''Retrieves the state based on id'''
    try:
        state = storage.get('State', str(state_id))
        return jsonify(state.to_dict())
    except:
        return jsonify({'error': 'Not found'}), 404


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_id(state_id):
    '''Deletes the state based on id'''
    try:
        state = storage.get('State', str(state_id))
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    except:
        return jsonify({'error': 'Error retrieving state'}), 404

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''Creates a state'''