#!/usr/bin/python3
"""
User object that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, jsonify, request
import json


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def all_users():
    users_dict = storage.all(User)
    users_list = [user.to_dict() for user in users_dict.values()]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def users_id(user_id):
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def users_delete(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def users_post():
    try:
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        if 'email' not in data_object:
            abort(400, 'Missing email')
        if 'password' not in data_object:
            abort(400, 'Missing password')
        new_user = User(**data_object)
        storage.new(new_user)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def users_put(user_id):
    try:
        user_up = storage.get(User, user_id)
        if not user_up:
            abort(404)
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        for key, value in data_object.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user_up, key, value)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(user_up.to_dict()), 200
