#!/usr/bin/python3
'''Handling RESTful API on cities'''
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_list(state_id):
    '''Retrieves the list of all cities for a specific state'''
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'Not found'}), 404

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id):
    '''Retrieves a city based on id'''
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    '''Deletes a city based on id'''
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    '''Creates a city'''
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'error': 'Not found'}), 404

    try:
        json_data = request.get_json()
        if not isinstance(json_data, dict):
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in json_data:
            return jsonify({'error': 'Missing name'}), 400
        new_city = City(name=json_data['name'], state_id=state_id)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201
    except Exception:
        return jsonify({'error': 'Error creating city'})


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''Updates a city object'''
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'error': 'Not found'}), 404

    try:
        json_data = request.get_json()
        if not isinstance(json_data, dict):
            return jsonify({'error': 'Not a JSON'}), 400

        for key, value in json_data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    except Exception:
        return jsonify({'error': 'Error updating city'})
