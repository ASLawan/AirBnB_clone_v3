#!/usr/bin/python3
"""
    Module implementing status and stats methods
    to return status and object numbers by class

"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns status code in JSON"""
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """returns number of instances of each object class"""
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
