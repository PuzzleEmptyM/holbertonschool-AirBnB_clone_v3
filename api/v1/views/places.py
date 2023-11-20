#!/usr/bin/python3
'''Handling RESTful API on places'''
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def place_list(city_id):
    '''Retrieves the list of all place objects'''
    p_list = []
    places = storage.all('Place').values()
    city = storage.get('City', str(city_id))
    if city is None:
        return jsonify({'error': 'Not Found'}), 404
    else:
        for place in places:
            if place.city_id == city_id:
                p_list.append(place.to_dict())
    return jsonify(p_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place_id(place_id):
    '''Retrieves place object based on id'''
    try:
        place = storage.get('Place', str(place_id))
        return jsonify(place.to_dict())
    except Exception:
        return jsonify({'error': 'Not Found'}), 404


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''Deletes the place object based on id'''
    place = storage.get('Place', str(place_id))
    if place is not None:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        return jsonify({'error': 'Error retrieving place'}), 404


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''Creates Place'''
    json_data = request.get_json()
    if not isinstance(json_data, dict):
        return jsonify({'error': 'Not a JSON'}), 400
    city = storage.get('City', str(city_id))
    if city is None:
        return jsonify({'error': 'Not Found'}), 404
    if 'user_id' not in json_data:
        return jsonify({'error': 'Missing user_id'}), 400
    if 'name' not in json_data:
        return jsonify({'error': 'Missing name'})
    places = request.get_json()
    user = storage.get(User, places['user_id'])
    if user is None:
        return jsonify({'error': 'Not Found'}), 404
    places['city_id'] = city_id
    new_place = Place(**places)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''Updates the place based on id'''
    json_data = request.get_json()
    place = storage.get('Place', str(place_id))
    if not isinstance(json_data, dict):
        return jsonify({'error': 'Not a JSON'})
    if place is None:
        return jsonify({'error': 'Not Found'}), 404
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
