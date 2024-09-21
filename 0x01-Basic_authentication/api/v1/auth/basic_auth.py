#!/usr/bin/env python3
""" Module of Basic auth """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Returns the Base64 part of the Authorization header """
        if not authorization_header or\
           not isinstance(authorization_header, str) or\
           not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]
