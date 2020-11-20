from src.models.user import User
from src.util import crypto
from src.util.exceptions import (
    InvalidPassword, 
    InvalidEmail,
    InvalidToken,
    ExpiredToken
)
from src import config

import jwt

from flask import jsonify, request, Response
from datetime import datetime, timedelta

class UserController:
    def __encode_auth_token(self, name: str) -> bytes:
        """Encode user's auth token

        Args:
            name (str): user identification

        Returns:
            str: token generated via jwt
        """
        try:
            dt_token_generated = datetime.now()

            payload = {
                'sub': name,
                'exp': dt_token_generated + timedelta(seconds=10),
                'iat': dt_token_generated
            }

            return jwt.encode(
                payload,
                config.token['key'],
                algorithm='HS256'
            )

        except Exception as error:
            return error

    def __decode_auth_token(self, auth_token: bytes) -> str:
        """Decodes auth_toke, returning user's name.

        Args:
            auth_token (bytes): token to be decoded

        Returns:
            str: user's name
        """
        try:
            payload = jwt.decode(auth_token, config.token['key'])

            return payload['sub']
        
        except jwt.ExpiredSignatureError as error:
            raise ExpiredToken

        except jwt.InvalidTokenError:
            raise InvalidToken

    # TODO: user sign up must check if user already exists
    def create(self) -> tuple:
        """Save user in the database

        Returns:
            tuple: (Response, int), Response content and its status code
        """
        try:
            user = User(
                name=request.json.get('name'),
                email=request.json.get('email'),
                password=crypto.encrypt(request.json.get('password'))
            )
            user.save()

            auth_token = self.__encode_auth_token(user.name)

            response = {
                'message': 'User created successfully',
                'auth_token': str(auth_token)
            }

            return jsonify(response), 201

        except (InvalidEmail, InvalidPassword) as error:
            return jsonify(
                {
                    'message': str(error)
                }
            ), 403
        
        #TODO: use the exceptions below when the auth token needs to be validated
        """ except (InvalidToken, ExpiredToken) as error:
            return jsonify(
                {
                    'message': str(error)
                }
            ), 401
        """

    def login(self) -> tuple:
        """Perfirm user's login, if password matchs the existing one.

        Returns:
            tuple: (Response, int), Response content and its status code
        """
        try:
            email = request.json.get('email')
            password = request.json.get('password')
            user = User.objects(email=email)

            if user and crypto.check_encrypted(password, user[0].password):
                auth_token = self.__encode_auth_token(user[0].email)
                return jsonify(
                    {
                        'auth_token': str(auth_token),
                        'message': 'User signed in successfully'
                    }
                ), 200
            return jsonify(
                {
                    'message': 'Invalid user or password'
                }
            ), 401
        
        except Exception as error:
            print(str(error))
            return jsonify(
                {
                    'message': 'Could not complete your request',
                    'error': str(error),
                }
            ), 403
