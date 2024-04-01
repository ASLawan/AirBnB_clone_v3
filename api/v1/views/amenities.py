#!/usr/bin/python3
"""
    Module implementing CRUD for Amenity objects
    to handle API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """returns all amenities objects"""
    amenities = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in amenities.values()])


@app_views.route('/amenities/<amenities_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """returns an amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenity/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity object based on ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """creates an amenity object"""
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if "name" not in new_amenity:
        abort(400, "<Missing name")
    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.asve()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates and amenity object based on id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    for k, v in request_body.items():
        if k not in ignore:
            setattr(amenity, k, v)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
