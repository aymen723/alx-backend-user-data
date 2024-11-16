#!/usr/bin/env python3
"""
Define SessionExpAuth class
"""
import os
from datetime import (
    datetime,
    timedelta
)
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Definition of class SessionExpAuth that adds an
    expiration date to a Session ID
    """

    def __init__(self):
        """
        Initialize the class with a session duration from an environment variable.
        If the environment variable is not set, defaults to 0 (no expiration).
        """
        try:
            duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """
        Create a Session ID for a given user ID and store session data with creation time.
        Args:
            user_id (str): User ID
        Returns:
            str: New session ID or None if user_id is None
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        
        # Store user session data with creation timestamp
        session_data = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_data
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a user ID based on a session ID if the session is still valid.
        Args:
            session_id (str): Session ID
        Returns:
            str: User ID or None if session is invalid or expired
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        
        # Retrieve session data
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None:
            return None

        # Check if the session has expired
        created_at = user_details.get("created_at")
        if created_at is None:
            return None
        if self.session_duration <= 0:
            return user_details.get("user_id")

        # Verify if the session is still within the allowed window
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None  # Session has expired

        return user_details.get("user_id")
