#!/usr/bin/python3
"""
Amenity objects that handles all default RESTFul API actions
"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities():
    """ Get all amenities """
    amenities_dict = storage.all(Amenity)
    amenities_list = [amenity.to_dict() for amenity in amenities_dict.values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenities_id(amenity_id):
    """ Get amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict()),
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenities_delete(amenity_id):
    """ Delete Amenity """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify('{}')


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def amenities_post():
    """ Add Amenity """
    data_object = request.get_json()
    if type(data_object) is not dict:
        return abort(400, 'Not a JSON')
    if 'name' not in data_object:
        return abort(400, 'Missing name')
    new_amenity = Amenity(**data_object)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenities_put(amenity_id):
    """ Update Amenity """
    amenity_up = storage.get(Amenity, amenity_id)
    if not amenity_up:
        abort(404)
    data_object = request.get_json()
    if type(data_object) is not dict:
        abort(400, 'Not a JSON')
    for key, value in data_object.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_up, key, value)
    storage.save()
    return jsonify(amenity_up.to_dict()), 200
