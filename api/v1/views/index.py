#!/usr/bin/python3
"""Blueprint for the API."""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.engine import classes

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return a JSON response indicating the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Return a JSON response indicating the status of the API."""
    object_counts = {}

    for class_name, class_type in classes.items():
        object_counts[class_name] = storage.count(class_type)

    return jsonify(object_counts)
