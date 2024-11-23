#!/usr/bin/env python3
"""
Flask app
"""
from flask import (
    Flask,
    request,
    jsonify,
    abort,
    redirect,
    url_for
)

from auth import Auth

app = Flask(__name__)
auth_service = Auth()  # Renamed from AUTH to auth_service


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    Return JSON response:
    {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    Register new users
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = auth_service.register_user(email, password)  # Updated variable name
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    Log in a user if the credentials provided are correct, and create a new
    session for them.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not auth_service.valid_login(email, password):  # Updated variable name
        abort(401)

    session_id = auth_service.create_session(email)  # Updated variable name
    resp = jsonify({"email": f"{email}", "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Log out a logged-in user and destroy their session
    """
    session_id = request.cookies.get("session_id", None)
    user = auth_service.get_user_from_session_id(session_id)  # Updated variable name
    if user is None or session_id is None:
        abort(403)
    auth_service.destroy_session(user.id)  # Updated variable name
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    Return a user's email based on session_id in the received cookies
    """
    session_id = request.cookies.get("session_id")
    user = auth_service.get_user_from_session_id(session_id)  # Updated variable name
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Generate a token for resetting a user's password
    """
    email = request.form.get("email")
    try:
        reset_token = auth_service.get_reset_password_token(email)  # Updated variable name
    except ValueError:
        abort(403)

    return jsonify({"email": f"{email}", "reset_token": f"{reset_token}"})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    Update a user's password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        auth_service.update_password(reset_token, new_password)  # Updated variable name
    except ValueError:
        abort(403)

    return jsonify({"email": f"{email}", "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
