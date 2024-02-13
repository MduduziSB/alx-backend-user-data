#!/usr/bin/env python3
"""
Module for class Auth
"""
from flask import request
from typing import List, TypeVar
import fnmatch


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
        if path is None or not excluded_paths:
            return True
        for ex_path in excluded_paths:
            if fnmatch.fnmatch(path, ex_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Args:
        - request(Flask request object) with a default value "None"

        return:
        - None
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Args:
        - request(Flask request object) with a default value "None"

        return:
        - None
        """
        return None
