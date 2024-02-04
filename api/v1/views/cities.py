#!/usr/bin/python3
"""
City objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import abort, jsonify, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """ Get Cities by state"""
    city_list = []
    city_dict = storage.all(City)
    for city in city_dict.values():
        if state_id == city.state_id:
            city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def cities_id(city_id):
    """ Get City by state"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def cities_delete(city_id):
    """ Delete City by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def cities_post(state_id):
    """ Add city """
    data_object = request.get_json
    if type(data_object) is not dict:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data_object['state_id'] = state_id
    if 'name' not in data_object:
        abort(400, 'Missing name')
    new_city = City(**data_object)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def cities_put(city_id):
    """ Update city"""
    city_up = storage.get(City, city_id)
    if not city_up:
        abort(404)
    data_object = request.get_json
    if type(data_object) is not dict:
        abort(400, 'Not a JSON')
    for key, value in data_object.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city_up, key, value)
    storage.save()
    return jsonify(city_up.to_dict()), 200
