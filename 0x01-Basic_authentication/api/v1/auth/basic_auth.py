#!/usr/bin/env python3
"""
BasicAuth module
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth definition
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """
        Computes Base64 part of the Authorization header
        for a Basic Authentication:
        """

        if authorization_header is None or \
           not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None
        base64_part = authorization_header.split('Basic ')[1].strip()
        return base64_part

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        Retrieves decoded value of a Base64 string base64_authorization_header
        """
        if base64_authorization_header is None or \
           not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except BaseException:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """
        Retrieves user email and password from the Base64 decoded value
        """

        if decoded_base64_authorization_header is None or \
           not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        Retrievs User instance based on his email and password
        """

        if user_email is None or not isinstance(user_email, str) or \
           user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            check_users = User.search({'email': user_email})
        except Exception:
            return None

        for user in check_users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> User:
        """Retrieves the user"""
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)

        if not auth_header or not base64_header or not decoded_header:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if not user_email or not user_pwd:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
