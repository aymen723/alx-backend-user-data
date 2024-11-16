#!/usr/bin/env python3
"""
Definition of the BasicAuth class
"""
import base64
from .auth import Auth
from typing import TypeVar

from models.user import User


class BasicAuth(Auth):
    """ Implements methods for Basic Authorization protocol
    """
    def get_base64_authorization_token(self, authorization_header: str) -> str:
        """
        Extracts the Base64 token from the Authorization header for Basic Auth
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        token = authorization_header.split(" ")[-1]
        return token

    def decode_base64_token(self, base64_token: str) -> str:
        """
        Decodes a Base64-encoded string
        """
        if base64_token is None:
            return None
        if not isinstance(base64_token, str):
            return None
        try:
            encoded_bytes = base64_token.encode('utf-8')
            decoded_bytes = base64.b64decode(encoded_bytes)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_token: str) -> (str, str):
        """
        Extracts user email and password from a decoded Base64 string
        """
        if decoded_token is None:
            return (None, None)
        if not isinstance(decoded_token, str):
            return (None, None)
        if ':' not in decoded_token:
            return (None, None)
        email, password = decoded_token.split(":", 1)
        return (email, password)

    def find_user_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns a User instance based on provided email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def get_current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves a User instance based on the given request
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.get_base64_authorization_token(auth_header)
            if token is not None:
                decoded_token = self.decode_base64_token(token)
                if decoded_token is not None:
                    email, password = self.extract_user_credentials(decoded_token)
                    if email is not None:
                        return self.find_user_from_credentials(email, password)
        return None
