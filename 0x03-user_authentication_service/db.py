#!/usr/bin/env python3
"""
DB module to manage database interactions for user authentication.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """
    DB class for handling user-related database operations.
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance.
        Creates the SQLite database and initializes its schema.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)  # Reset the database schema
        Base.metadata.create_all(self._engine)  # Create tables
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object.
        Creates a new session if one does not already exist.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Creates a User object and saves it to the database.
        Args:
            email (str): User's email address.
            hashed_password (str): User's hashed password.
        Returns:
            User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user by matching attributes provided as keyword arguments.
        Args:
            **kwargs: Key-value pairs of attributes to match.
        Returns:
            User: The matching User object.
        Raises:
            InvalidRequestError: If an invalid attribute is provided.
            NoResultFound: If no user matches the criteria.
        """
        try:
            query = self._session.query(User)
            for key, value in kwargs.items():
                if not hasattr(User, key):
                    raise InvalidRequestError(f"Invalid attribute: {key}")
                query = query.filter(getattr(User, key) == value)
            user = query.one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the provided attributes.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes in the database.
        Args:
            user_id (int): ID of the user to update.
            **kwargs: Key-value pairs of attributes to update.
        Raises:
            ValueError: If the user is not found or an invalid attribute is provided.
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError(f"User with ID {user_id} does not exist.")

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)
        self._session.commit()
