#!/usr/bin/env python3
"""
Module for class Auth
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    class Auth definition
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Args:
        - path(str)
        - excluded_paths(List of str)

        return:
        boolian value
        """
        if not path or not excluded_paths:
            return True

        if path.endswith('/'):
            path = path[:-1]

        for exc in excluded_paths:
            if exc.endswith('*'):
                if path.startswith(exc[:-1]):
                    return False
            elif path == exc.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Args:
        - request(Flask request object) with a default value "None"

        return:
        - None
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Args:
        - request(Flask request object) with a default value "None"

        return:
        - None
        """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request """
        if request is None:
            return None
        sess_name = os.getenv('SESSION_NAME')
        if sess_name is None:
            return None
        return request.cookies.get(sess_name)
