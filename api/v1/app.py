#!/usr/bin/python3
"""Flask app for the API."""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import environ

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Call storage.close() on teardown of the Flask app context"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return a JSON-formatted 404 status code response."""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = environ.get('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
