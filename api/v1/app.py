#!/usr/bin/python3
"""
    Module implementing api with flask framework

"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
import os


app = Flask(__name__)


app.register_blueprint(app_views, url_prefix="/api/v1")


@app.errorhandler(404)
def not_found(error):
    """handles the not found error, 404"""
    return jsonify(error='Not found'), 404


@app.teardown_appcontext
def teardown_storage(exception):
    """class close to close storage session"""
    storage.close()


if __name__ == "__main__":
    HBNB_API_HOST = os.getenv('HBNB_API_HOST')
    HBNB_API_PORT = os.getenv('HBNB_API_PORT')
    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
