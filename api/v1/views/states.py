#!/usr/bin/python3
"""State flask handler"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/api/v1/states/', methods=['GET'], strict_slashes=False)
def retrieves_states():
    """
    Retrieve list of all State objects.
    """
    empy_list = []
    for state in storage.all(State).values():
        empy_list.append(state.to_dict())
    return jsonify(empy_list)


@app_views.route('/api/v1/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieves_state_by_id(state_id):
    """
    Delete State object with given id
    Raise 404 error if id not linked to any State object
    Returns and empty dictionary with status code 200
    """
    for state in storage.all(State).values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def deletes_state_by_id(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create State via POST
    If HTTP body request is not valid JSON, raise 400 error, Not JSON
    If dictionary doesn't contain key name, raise 400 error with
    message Missing name
    Return new State with status code 201
    """
    new_state_dict = request.get_json()
    if not new_state_dict:
        abort(400, 'Not a JSON')
    if 'name' not in new_state_dict.keys():
        abort(400, 'Missing name')
    new_state = State(**new_state_dict)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_by_id(state_id):
    """
    Update State object via PUT
    If the state_id is not linked to any State object, raise 404 error
    If the HTTP body request is not valid JSON, raise 400 error, Not a JSON
    Update the State object with all key-value pairs of dictionary
    Ignore keys: id, created_at, updated_at   
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')

    for key, value in body.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
