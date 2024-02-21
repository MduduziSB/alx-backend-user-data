#!/usr/bin/env python3
""" auth module """
import bcrypt
from db import DB

from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt hashpw.

       Args:
          password (str): The password to hash.

      Returns:
            bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generate a new UUID and return its string representation."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the given email and password.

        Args:
            email (str): The email of the new user.
            password (str): The password of the new user.

        Returns:
            User: A User object representing the new user.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided email and password combination is valid.

        Args:
            email (str): The email of the user.
            password (str): The password to check.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password
            )
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """Create a session for the user with the specified email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID created for the user.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get the user corresponding to the given session ID.

        Args:
            session_id (str): The session ID to search for.

        Returns:
            User or None: The corresponding User object, or None if not found.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id):
        """ Updates the corresponding user’s session ID to None """

        try:
            self._db.update_session(user_id, None)
        except Exception:
            return None
