#!/usr/bin/python3
"""
    Module implementing http CRUD methods for places
    objects to handle default API actions

"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
import json
import os
import requests


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """returns list of all places objects in the database"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dic() for place in city.places])


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place object given its id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates place object under a given city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if "user_id" not in new_place:
        abort(400, "Missing user_id")
    user_id = new_place['user_id']
    if not storage.get(User, user_id):
        abort(400)
    if "name" not in new_place:
        abort(400, "Missing name")
    place = Place(**new_place)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.td_dict()), 201)


@app_views.route('/places/<place_id>', methods=['[PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """updates place object information"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    request_body = request.ge_json()
    if not request_body:
        abort(400, "Not a JSON")
    ignr = ['id', 'user_id', 'city_at', 'created_at', 'updated_at']
    for k, v in request_body.items():
        if k not in ignr:
            setattr(place, k, v)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
