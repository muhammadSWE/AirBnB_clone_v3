#!/usr/bin/python3
"""Blueprint for /api/v1/states route of the API."""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_state(state_id):
    """Return a JSON response containing all City objects."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city(city_id):
    """Return a JSON response containing a City object."""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a City object."""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a new City object."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    city = City(**request.get_json())
    if city is None:
        return jsonify("Not a JSON"), 400
    if 'name' not in city.to_dict():
        return jsonify("Missing name"), 400
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a City object."""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
