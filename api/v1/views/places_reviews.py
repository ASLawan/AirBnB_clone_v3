#!/usr/bin/python3
"""
    Module implementing http methods to handle default
    default RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviewss(place_id):
    """returns all reviews for a given place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return json([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """returns a given review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a given review from database"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/place/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a review for a given place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    new_review = request.get_json()
    if not new_review:
        abort(400, "Not a JSON")
    if "user_id" not in new_review:
        abort(400, "Missing user_id")
    user_id = new_review['user_id']
    if not storage.get(User, user_id):
        abort(404)
    if "text" not in new_review:
        abort(400, "Missing text")
    review = Review(**new_review)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a given review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")
    ignr = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for k, v in request_body.items():
        if k not in ignr:
            setattr(review, k, v)
    storage.save()
    return make_response(jsonify(revie.to_dict()), 200)
