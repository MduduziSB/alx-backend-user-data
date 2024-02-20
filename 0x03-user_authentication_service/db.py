#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
            email (str): The email of the user
            hashed_password (str): The hashed password of the user

        Returns:
            User: The created User object
        """
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments representing filters for the
            query.

        Returns:
            User: The first user found matching the filters.

        Raises:
            NoResultFound: If no user is found matching the filters.
            InvalidRequestError: If wrong query arguments are passed.
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
            return user
        except (NoResultFound, InvalidRequestError):
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes based on user_id.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing attributes.

        Returns:
            None

        Raises:
            ValueError: If an invalid argument is passed.
            NoResultFound: If no user is found matching the user_id.
            InvalidRequestError: If wrong query arguments are passed.
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(User, key):
                    setattr(user, key, value)
                else:
                    raise ValueError
            self._session.add(user)
            self._session.commit()
        except (NoResultFound, InvalidRequestError):
            raise
