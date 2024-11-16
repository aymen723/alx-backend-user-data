#!/usr/bin/env python3
"""
Define class SessionDBAuth
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Definition of SessionDBAuth class that persists session data
    in a database
    """

    def create_session(self, user_id=None):
        """
        Create a Session ID for a user_id
        Args:
           user_id (str): user ID
        Returns:
            A new session ID or None if creation fails
        """
        if user_id is None:
            return None
        
        # Generate session using parent method
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        
        # Create and save user session in database
        kw = {
            "user_id": user_id,
            "session_id": session_id
        }
        try:
            user_session = UserSession(**kw)
            user_session.save()
            return session_id
        except Exception as e:
            # Log exception if needed
            return None

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a user ID based on a session ID
        Args:
            session_id (str): Session ID
        Returns:
            user ID or None if session_id is None, invalid, or not found
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        try:
            user_sessions = UserSession.search({"session_id": session_id})
            if user_sessions:
                return user_sessions[0].user_id
        except Exception as e:
            # Log exception if needed
            return None
        return None

    def destroy_session(self, request=None):
        """
        Destroy a UserSession instance based on a
        Session ID from a request cookie
        Args:
            request: Flask request object
        Returns:
            True if session is successfully destroyed, False otherwise
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        try:
            user_sessions = UserSession.search({"session_id": session_id})
            if user_sessions:
                user_sessions[0].remove()
                return True
        except Exception as e:
            # Log exception if needed
            return False
        return False
