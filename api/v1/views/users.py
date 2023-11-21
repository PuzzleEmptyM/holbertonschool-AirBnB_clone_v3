#!/usr/bin/python3
'''Handling RESTful API on User'''
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def user_list():
    '''Retrieves the list of all users'''
    u_list = []
    obj = storage.all('User').values()
    for user in obj:
        u_list.append(user.to_dict())
    return jsonify(u_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_id(user_id):
    '''Retrieves the user based on id'''
    try:
        user = storage.get('User', str(user_id))
        return jsonify(user.to_dict())
    except Exception:
        return jsonify({'error': 'Not found'}), 404


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    '''Deletes the user based on id'''
    user = storage.get('User', str(user_id))
    if user is not None:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        return jsonify({'error': 'Error retrieving user'}), 404


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''Creates a user'''
    try:
        json_data = request.get_json()
        if not isinstance(json_data, dict):
            return jsonify({'error': 'Not a JSON'}), 400
        if 'email' not in json_data:
            return jsonify({'error': 'Missing email'}), 400
        if 'password' not in json_data:
            return jsonify({'error': 'Missing password'}), 400
        new_user = User(email=json_data['email'], password=json_data
                        ['password'])
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201
    except Exception:
        return jsonify({'error': 'Error creating user'})


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''Updates a user object'''
    user = storage.get('User', str(user_id))
    if user is None:
        return jsonify({'error': 'Not Found'}), 404
    json_data = request.get_json()
    if not isinstance(json_data, dict):
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in json_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
