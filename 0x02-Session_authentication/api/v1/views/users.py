#!/usr/bin/env python3
""" Module for User Views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - JSON representation of all User objects
    """
    users = [user.to_json() for user in User.all()]
    return jsonify(users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - user_id (User ID)
    Return:
      - JSON representation of the User object
      - 404 error if the User ID does not exist
    """
    if not user_id:
        abort(404)
    if user_id == "me":
        if not request.current_user:
            abort(404)
        return jsonify(request.current_user.to_json())
    user = User.get(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - user_id (User ID)
    Return:
      - Empty JSON response if User is deleted successfully
      - 404 error if the User ID does not exist
    """
    if not user_id:
        abort(404)
    user = User.get(user_id)
    if not user:
        abort(404)
    user.remove()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body parameters:
      - email (required)
      - password (required)
      - last_name (optional)
      - first_name (optional)
    Return:
      - JSON representation of the created User object
      - 400 error if User creation fails
    """
    try:
        user_data = request.get_json()
    except Exception:
        return jsonify({'error': "Wrong format"}), 400

    if not user_data:
        return jsonify({'error': "Wrong format"}), 400
    if not user_data.get("email"):
        return jsonify({'error': "email missing"}), 400
    if not user_data.get("password"):
        return jsonify({'error': "password missing"}), 400

    try:
        user = User()
        user.email = user_data.get("email")
        user.password = user_data.get("password")
        user.first_name = user_data.get("first_name")
        user.last_name = user_data.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Path parameter:
      - user_id (User ID)
    JSON body parameters (optional):
      - last_name
      - first_name
    Return:
      - JSON representation of the updated User object
      - 404 error if the User ID does not exist
      - 400 error if update fails
    """
    if not user_id:
        abort(404)
    user = User.get(user_id)
    if not user:
        abort(404)

    try:
        update_data = request.get_json()
    except Exception:
        return jsonify({'error': "Wrong format"}), 400

    if not update_data:
        return jsonify({'error': "Wrong format"}), 400
    if 'first_name' in update_data:
        user.first_name = update_data.get('first_name')
    if 'last_name' in update_data:
        user.last_name = update_data.get('last_name')

    user.save()
    return jsonify(user.to_json()), 200
