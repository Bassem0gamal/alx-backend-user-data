#!/usr/bin/env python3
""" Module of Basic auth """
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
import base64
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Returns the Base64 part of the Authorization header """
        if not authorization_header or\
           not isinstance(authorization_header, str) or\
           not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Returns the decoded value of a Base64 string """
        if not base64_authorization_header or\
           not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """ Returns the user email and password from the Base64 decoded """
        if not decoded_base64_authorization_header or\
           not isinstance(decoded_base64_authorization_header, str) or\
           ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> User:
        """ Returns the User instance based on his email and password """
        if not user_email or not isinstance(user_email, str) or\
           not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None
        return None

    def current_user(self, request=None) -> User:
        """ Overload auth and retrieves the user """
        auth_header = self.authorization_header(request)
        base64 = self.extract_base64_authorization_header(auth_header)
        decoded_header_auth = self.decode_base64_authorization_header(base64)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_header_auth)
        return self.user_object_from_credentials(user_email, user_pwd)
