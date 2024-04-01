#!/usr/bin/python3
"""
    Module to CRUD for users objects to handle
    default API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def get_users():
    """returns all users objects in the database"""
    users = storage.all(User)
    return jsonify([obj.to_dict() for obj in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_users(user_id):
    """returns user based on id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """deletes user based on id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """creates a new user object"""
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if "email" not in new_user:
        abort(400, "Missing email")
    if "password" not in new_user:
        abort(400, "Missing password")

    user = User(**new_user)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """updates a user object based on id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")
    ignore = ['id', 'email', 'created_at', 'updated_at']
    for k, v in request_body.items():
        if k not in ignore:
            setattr(user, k, v)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
