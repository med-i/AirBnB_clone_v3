#!/usr/bin/python3
"""
Review object that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from flask import abort, jsonify, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """ Get reviews by place"""
    review_list = []
    review_dict = storage.all(Review)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for review in review_dict.values():
        if place_id == review.place_id:
            review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_by_id(review_id):
    """ Get Review"""
    review = storage.get(Place, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    """ Delete Review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def places_review_post(place_id):
    """ ADD review """
    data_object = request.get_json()
    if type(data_object) is not dict:
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data_object['place_id'] = place_id
    if 'user_id' not in data_object:
        abort(400, 'Missing user_id')
    if 'text' not in data_object:
        abort(400, 'Missing text')
    user = storage.get(User, data_object['user_id'])
    if not user:
        abort(404)
    new_place_review = Review(**data_object)
    storage.save()
    return jsonify(new_place_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def review_put(review_id):
    """ Update Review """
    review_up = storage.get(Review, review_id)
    if not review_up:
        abort(404)
    data_object = request.get_json()
    if type(data_object) is not dict:
        abort(400, 'Not a JSON')
    for key, value in data_object.items():
        if key not in ['id', 'created_at', 'updated_at',
                       'user_id', 'place_id']:
            setattr(review_up, key, value)
    storage.save()
    return jsonify(review_up.to_dict()), 200
