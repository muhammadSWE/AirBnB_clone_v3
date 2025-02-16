#!/usr/bin/python3
"""Flask app for the API."""
from api.v1.views import app_views
from flask import Flask
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix="/api/v1")

@app.teardown_appcontext
def teardown_db(exception):
    """Call storage.close() on teardown of the Flask app context"""
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
