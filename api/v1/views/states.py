#!/usr/bin/python3
'''Handling RESTful API on state'''
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


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
    except Exception as e:
        return jsonify({'error': 'Not found'}), 404


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_id(state_id):
    '''Deletes the state based on id'''
    state = storage.get('State', str(state_id))
    if state is not None:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        return jsonify({'error': 'Error retrieving state'}), 404


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''Creates a state'''
    try:
        json_data = request.get_json()
        if not isinstance(json_data, dict):
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in json_data:
            return jsonify({'error': 'Missing name'}), 400
        new_state = State(name=json_data['name'])
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    except Exception as e:
        return jsonify({'error': 'Error creating state'})


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Updates a state object'''
    state = storage.get('State', str(state_id))
    if state is None:
        return jsonify({'error': 'Not Found'}), 404
    json_data = request.get_json()
    if not isinstance(json_data, dict):
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
