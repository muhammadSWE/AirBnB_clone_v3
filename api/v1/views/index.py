#!/usr/bin/python3
"""Blueprint for the API."""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return a JSON response indicating the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route('/obj_counts', methods=['GET'], strict_slashes=False)
def obj_counts():
    """Return a JSON response indicating the status of the API."""
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }

    obj_counts = {}
    for key, value in classes.items():
        obj_counts[key] = storage.count(value)

    return jsonify(obj_counts)
