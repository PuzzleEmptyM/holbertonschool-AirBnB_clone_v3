#!/usr/bin/python3
'''Handling RESTful API on Review'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def place_reviews_list(place_id):
    '''Retrieves the list of all reviews of a place'''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    r_list = [review.to_dict() for review in place.reviews]
    return jsonify(r_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_id(review_id):
    '''Retrieves the review based on id'''
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''Deletes the review based on id'''
    review = storage.get('Review', review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''Creates a review'''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    try:
        json_data = request.get_json()
        if not isinstance(json_data, dict):
            abort(400, 'Not a JSON')
        if 'user_id' not in json_data:
            abort(400, 'Missing user_id')
        user = storage.get('User', json_data['user_id'])
        if user is None:
            abort(404)
        if 'text' not in json_data:
            abort(400, 'Missing text')
        new_review = Review(user_id=json_data['user_id'],
                            place_id=place_id, **json_data)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201
    except Exception:
        abort(400, 'Error creating review')


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    '''Updates a review object'''
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)

    try:
        json_data = request.get_json()
        if not isinstance(json_data, dict):
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if key not in ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    except Exception:
        abort(400, 'Error updating review')
