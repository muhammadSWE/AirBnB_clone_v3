#!/usr/bin/python3
"""Unit tests for api/v1/views/index.py"""
import unittest
from api.v1.views import app_views
from flask import jsonify


class TestIndex(unittest.TestCase):
  """Tests for api/v1/views/index.py"""
  def test_status(self):
    """Tests that the status route returns a JSON response"""
    with app_views.app.test_client() as client:
      response = client.get('/api/v1/status')
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.get_json(), {'status': 'OK'})
