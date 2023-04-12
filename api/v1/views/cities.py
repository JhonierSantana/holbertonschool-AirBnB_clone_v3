#!/usr/bin/python3
"""City flask handler"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def retrieves_cities_by_state_id(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    all_cities = [all_cities.to_dict() for all_cities in state.cities]
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrieves_city_by_id(city_id):
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deletes_city_by_id(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    city_dict = request.get_json()
    if not city_dict:
        abort(400, 'Not a JSON')

    if 'name' not in city_dict.keys():
        abort(400, 'Missing name')

    new_city = City(**city_dict)
    setattr(new_city, 'state_id', state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city_by_id(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')

    for key, value in body.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
