#!/usr/bin/python3
'''Handling RESTful API on amenities'''
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenity_list():
    '''Retrieves the list of all amenities'''
    a_list = []
    obj = storage.all('Amenity').values()
    for amenity in obj:
        a_list.append(amenity.to_dict())
    return jsonify(a_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_id(amenity_id):
    '''Retrieves the amenity based on the id'''
    try:
        amenity = storage.get('Amenity', str(amenity_id))
        return jsonify(amenity.to_dict())
    except Exception as e:
        return jsonify({'error': 'Not Found'}), 404


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''Deletes the amenity based on the id'''
    amenity = storage.get('Amenity', str(amenity_id))
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        return jsonify({'error': 'Error retrieving amenity'}), 404


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    '''Creates an amenity'''
    try:
        json_data = request.get_json()
        if not isinstance(json_data, dict):
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in json_data:
            return jsonify({'error': 'Missing name'}), 400
        new_amenity = Amenity(name=json_data['name'])
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201
    except Exception as e:
        return jsonify({'error': 'Error creating amenity'})


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''Updates the amenity based on the id'''
    amenity = storage.get('Amenity', str(amenity_id))
    if amenity is None:
        return jsonify({'error': 'Not found'}), 404
    json_data = request.get_json()
    if not isinstance(json_data, dict):
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
