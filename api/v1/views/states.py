#!/usr/bin/python3
"""
    handles all default RESTFul API actions
"""
import json
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ Get All states """
    states_dict = storage.all(State)
    states_list = [state.to_dict() for state in states_dict.values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """ GET state by id """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def states_delete(state_id):
    """ DELETE state by id """
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify('{}')


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def states_post():
    """ Create new state """
    try:
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        if 'name' not in data_object:
            abort(400, 'Missing name')
        new_state = State(**data_object)
        storage.new(new_state)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def states_put(state_id):
    """ Update state """
    try:
        state_up = storage.get(State, state_id)
        if not state_up:
            abort(404)
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        for key, value in data_object.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state_up, key, value)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(state_up.to_dict()), 201
