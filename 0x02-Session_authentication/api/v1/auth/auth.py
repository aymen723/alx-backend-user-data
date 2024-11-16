#!/usr/bin/env python3
"""
Definition of class Auth
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Manages the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication
        Args:
            path (str): URL path to be checked
            excluded_paths (List[str]): List of paths that do not require authentication
        Returns:
            bool: True if path is not in excluded_paths, else False
        """
        if not path:
            return True
        if not excluded_paths:
            return True

        # Normalize paths by removing trailing slashes for consistent comparison
        path = path.rstrip('/')
        for excluded_path in excluded_paths:
            # Normalize excluded_path similarly
            normalized_excluded = excluded_path.rstrip('/')
            # Handle wildcard match (e.g., "path/*")
            if normalized_excluded.endswith('*'):
                if path.startswith(normalized_excluded[:-1]):
                    return False
            elif path == normalized_excluded:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from a request
        Args:
            request (Flask request object): Request object
        Returns:
            str: The value of the Authorization header, or None if not present
        """
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on request information
        Args:
            request (Flask request object): Request object
        Returns:
            TypeVar('User'): A User instance or None
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie from a request
        Args:
            request (Flask request object): Request object
        Returns:
            str: Value of the session cookie, or None if not found
        """
        if not request:
            return None
        session_name = os.getenv('SESSION_NAME', '_my_session_id')  # Default value
        return request.cookies.get(session_name)
