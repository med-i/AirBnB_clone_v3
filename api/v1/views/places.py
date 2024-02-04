#!/usr/bin/python3
"""
Place objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ Get places """
    place_list = []
    place_dict = storage.all(Place)
    for place in place_dict.values():
        if city_id == place.city_id:
            place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def places_id(place_id):
    """ Get place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def places_delete(place_id):
    """ DELETE PLACE"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def places_post(city_id):
    """ ADD place """
    data_object = request.get_json()
    if type(data_object) is not dict:
        abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data_object['city_id'] = city_id
    if 'user_id' not in data_object:
        abort(400, 'Missing user_id')
    if 'name' not in data_object:
        abort(400, 'Missing name')
    user = storage.get(User, data_object['user_id'])
    if not user:
        abort(404)
    new_place = Place(**data_object)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def places_put(place_id):
    """ Update place"""
    place_up = storage.get(Place, place_id)
    if not place_up:
        abort(404)
    data_object = request.get_json()
    if type(data_object) is not dict:
        abort(400, 'Not a JSON')
    for key, value in data_object.items():
        if key not in ['id', 'created_at',
                       'updated_at', 'user_id', 'city_id']:
            setattr(place_up, key, value)
    storage.save()
    return jsonify(place_up.to_dict()), 200
