#!/usr/bin/env python3
"""
Definition of class SessionAuth
"""
from uuid import uuid4
from typing import TypeVar
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Implements Session Authorization protocol methods """
    
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user with user_id
        Args:
            user_id (str): User's ID
        Returns:
            None if user_id is None or not a string,
            otherwise a Session ID as a string
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a user ID based on a session ID
        Args:
            session_id (str): Session ID
        Returns:
            User ID or None if session_id is None or not a string
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance based on a cookie value
        Args:
            request: Request object containing the session cookie
        Returns:
            User instance or None
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Deletes a user session
        Args:
            request: Request object
        Returns:
            True if session is successfully deleted, False otherwise
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        self.user_id_by_session_id.pop(session_cookie, None)
        return True
