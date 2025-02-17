#!/usr/bin/python3
"""Blueprint for /api/v1/users route of the API."""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Return a JSON response containing all User objects."""
    return jsonify(
        [user.to_dict() for user in storage.all(User).values()]
        )


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user(user_id):
    """Return a JSON response containing a User object."""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a User object."""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new User object."""
    user = User(**request.get_json())
    if user is None:
        return jsonify("Not a JSON"), 400
    if 'email' not in user.to_dict():
        return jsonify("Missing email"), 400
    if 'password' not in user.to_dict():
        return jsonify("Missing password"), 400
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a User object."""
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
