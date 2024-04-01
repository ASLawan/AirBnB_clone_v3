#!/usr/bin/python3

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
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    stats = {}

    for cls in classes:
        cls_count = storage.count(cls)
        stats[cls.lower()] = cls_count
    return jsonify(stats)
