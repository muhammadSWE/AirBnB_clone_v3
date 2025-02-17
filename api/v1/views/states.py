#!/usr/bin/python3
"""Blueprint for /api/v1/states route of the API."""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Return a JSON response containing all State objects."""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state(state_id):
    """Return a JSON response containing a State object."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a State object."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new State object."""
    state = State(**request.get_json())
    if state is None:
        return jsonify("Not a JSON"), 400
    if 'name' not in state.to_dict():
        return jsonify("Missing name"), 400
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a State object."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
