#!/usr/bin/env python3
""" Module providing endpoints for API status, errors, and statistics
"""
from flask import jsonify, abort
from api.v1.views import app_views

@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def handle_unauthorized() -> str:
    """ 
    GET /api/v1/unauthorized endpoint
    Raises a 401 Unauthorized error
    """
    abort(401, description="Unauthorized")

@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def handle_forbidden() -> str:
    """ 
    GET /api/v1/forbidden endpoint
    Raises a 403 Forbidden error
    """
    abort(403, description="Forbidden")

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status() -> str:
    """ 
    GET /api/v1/status endpoint
    Returns the status of the API
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats/', strict_slashes=False)
def get_object_statistics() -> str:
    """ 
    GET /api/v1/stats endpoint
    Returns:
        - the count of each type of object
    """
    from models.user import User  # Importing model for user statistics
    object_counts = {}
    object_counts['users'] = User.count()
    return jsonify(object_counts)
