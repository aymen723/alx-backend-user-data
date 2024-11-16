#!/usr/bin/env python3
"""
Main module to handle routing for the API
"""
from os import getenv
from api.v1.views import api_blueprint
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os

# Initialize Flask application
app = Flask(__name__)
app.register_blueprint(api_blueprint)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize authentication object based on environment variable
authentication = None
AUTH_METHOD = os.getenv("AUTH_TYPE")
if AUTH_METHOD == "auth":
    from api.v1.auth.auth import Auth
    authentication = Auth()
elif AUTH_METHOD == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    authentication = BasicAuth()
elif AUTH_METHOD == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    authentication = SessionAuth()
elif AUTH_METHOD == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    authentication = SessionExpAuth()
elif AUTH_METHOD == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    authentication = SessionDBAuth()

@app.before_request
def before_request_handler():
    """
    Execute before handling any request to filter and authenticate requests
    """
    if authentication is None:
        return  # No authentication configured
    else:
        # Set the current user on the request object
        setattr(request, "current_user", authentication.current_user(request))
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
        ]
        if authentication.require_auth(request.path, excluded_paths):
            session_token = authentication.session_cookie(request)
            # If no auth header or session token, abort with 401 Unauthorized
            if authentication.authorization_header(request) is None and session_token is None:
                abort(401, description="Unauthorized")
            # If user cannot be identified, abort with 403 Forbidden
            if authentication.current_user(request) is None:
                abort(403, description="Forbidden")

# Custom error handler for 404 Not Found
@app.errorhandler(404)
def not_found_handler(error) -> str:
    """ Handle 404 errors (Not Found) """
    return jsonify({"error": "Not found"}), 404

# Custom error handler for 401 Unauthorized
@app.errorhandler(401)
def unauthorized_handler(error) -> str:
    """ Handle 401 errors (Unauthorized) """
    return jsonify({"error": "Unauthorized"}), 401

# Custom error handler for 403 Forbidden
@app.errorhandler(403)
def forbidden_handler(error) -> str:
    """ Handle 403 errors (Forbidden) """
    return jsonify({"error": "Forbidden"}), 403

# Run the Flask application
if __name__ == "__main__":
    server_host = getenv("API_HOST", "0.0.0.0")
    server_port = getenv("API_PORT", "5000")
    app.run(host=server_host, port=server_port)
