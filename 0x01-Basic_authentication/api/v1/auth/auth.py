#!/usr/bin/env python3
"""
Definition of the Auth class
"""
from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """
    Handles API authentication
    """
    def is_auth_required(self, endpoint: str, bypass_paths: List[str]) -> bool:
        """
        Checks if authentication is needed for a specific endpoint
        Args:
            - endpoint (str): URL endpoint to evaluate
            - bypass_paths (List of str): List of endpoints that do not require
              authentication
        Returns:
            - True if endpoint is not in bypass_paths, otherwise False
        """
        if endpoint is None:
            return True
        elif bypass_paths is None or bypass_paths == []:
            return True
        elif endpoint in bypass_paths:
            return False
        else:
            for path in bypass_paths:
                if path.startswith(endpoint):
                    return False
                if endpoint.startswith(path):
                    return False
                if path[-1] == "*":
                    if endpoint.startswith(path[:-1]):
                        return False
        return True

    def get_authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from a request object
        """
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def get_current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves a User instance based on request details
        """
        return None
