#!/usr/bin/python3
"""
    Module implemeting routes for City object
    to handle API actions
"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities'. methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """returns cities of a given state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """returns city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a given city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates a new city object for a given city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    new_city = request.get_json()
    if not new_city:
        abort(400, "Not a JSON")
    if 'name' not in new_city:
        abort(400, "Missing name")
    city = City(**new_city)
    setattr(city, 'state_id', state_id)
    storage.new(city)
    stoarage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """updates city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for k, v in request_body.items():
        if k not in ignored_keys:
            setattr(city, k, v)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
