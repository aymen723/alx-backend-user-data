#!/usr/bin/env python3
"""
Definition of authentication-related functions and the Auth class.
"""
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import (
    TypeVar,
    Union
)

from db import DB
from user import User

U = TypeVar(User)


def _hash_password(password: str) -> bytes:
    """
    Hashes a password string using bcrypt and returns it as bytes.
    Args:
        password (str): Password in string format.
    Returns:
        bytes: The hashed password.
    """
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a new UUID and returns its string representation.
    Returns:
        str: The generated UUID as a string.
    """
    return str(uuid4())


class Auth:
    """
    Auth class to manage user authentication, registration, and sessions.
    """

    def __init__(self) -> None:
        """
        Initialize the Auth class with a database instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user and returns the User object.
        Args:
            email (str): The email address of the new user.
            password (str): The password for the new user.
        Returns:
            User: The newly created user object.
        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a user's login credentials.
        Args:
            email (str): The user's email address.
            password (str): The user's password.
        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        return bcrypt.checkpw(password.encode("utf-8"), user_password)

    def create_session(self, email: str) -> Union[None, str]:
        """
        Creates a session ID for a user and updates their session_id attribute.
        Args:
            email (str): The user's email address.
        Returns:
            Union[None, str]: The session ID if successful, or None if the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, U]:
        """
        Retrieves a user object using a session ID.
        Args:
            session_id (str): The session ID of the user.
        Returns:
            Union[None, User]: The user object if found, or None otherwise.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a user's session by setting their session_id to None.
        Args:
            user_id (int): The ID of the user.
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset token for a user to reset their password.
        Args:
            email (str): The user's email address.
        Returns:
            str: The generated reset token.
        Raises:
            ValueError: If no user is found with the given email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password using a reset token.
        Args:
            reset_token (str): The reset token provided to the user.
            password (str): The new password for the user.
        Raises:
            ValueError: If the reset token is invalid or expired.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
