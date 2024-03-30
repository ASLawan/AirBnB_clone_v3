#!/usr/bin/python3
"""
    Module implementing api routes

"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """returns status code in JSON"""
    return jsonify({'status': 'OK'})