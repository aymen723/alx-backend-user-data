#!/usr/bin/env python3
""" Module for User Authentication Views
"""
import os
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def handle_login():
    """
    Handle user login by validating email and password
    Return:
        - JSON representation of user if authenticated
        - Error message if validation fails
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for user by email
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if any user's password is valid
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            session_cookie_name = os.getenv('SESSION_NAME')
            response.set_cookie(session_cookie_name, session_id)
            return response

    return jsonify({"error": "wrong password"}), 401

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def handle_logout():
    """
    Handle user logout by destroying session
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
