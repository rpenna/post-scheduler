from src.models.user import User
from src.models.blacklist import Blacklist

from src.util import crypto
from src.util.exceptions import (
    InvalidPassword, 
    InvalidEmail,
    InvalidToken,
    ExpiredToken,
    TokenNotDeclared
)
from src import config

import jwt
import mongoengine
import pytz

from flask import jsonify, request, Response
from datetime import datetime, timedelta

class UserController:
    def __encode_auth_token(self, email: str) -> bytes:
        """Encode user's auth token

        Args:
            email (str): user identification

        Returns:
            str: token generated via jwt
        """
        try:
            dt_token_generated = datetime.now()
            local = pytz.timezone('America/Sao_Paulo')
            dt_token_generated = local.localize(datetime.now(), is_dst=None)
            local_dt_utc = dt_token_generated.astimezone(pytz.utc)

            payload = {
                'sub': email,
                'exp': local_dt_utc + timedelta(seconds=60),
                'iat': local_dt_utc
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
            str: user's e-mail
        """
        try:
            payload = jwt.decode(auth_token, config.token['key'])

            return payload['sub']
        
        except jwt.ExpiredSignatureError as error:
            raise ExpiredToken

        except jwt.InvalidTokenError:
            raise InvalidToken

    def __get_auth_token(self) -> str:
        """Gets authorization token from headers

        Returns:
            str: Authorization token. If None, returns empty string
        
        Raises:
            TokenNotDeclared: excepction raised when the token has not been
            found on headers
        """
        try:
            authorization = request.headers.get('Authorization')
            if authorization is None:
                raise TokenNotDeclared

            return authorization.split('Bearer ')[1]
        
        except IndexError:
            raise TokenNotDeclared

    def __insert_into_blacklist(self, token: str) -> None:
        """Insert token into blacklist

        Args:
            token (str): Token to be inserted
        """
        blacklist = Blacklist(token=token)
        blacklist.save()
    
    def __is_token_blacklisted(self, token: str) -> bool:
        """Search for token in blacklist and inform wheter it's blacklisted or
        not

        Args:
            token (str): Token to be found

        Returns:
            bool: True if token is blacklisted, False if not
        """
        blacklist = Blacklist.objects(token=token)

        return len(blacklist) > 0

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
            user.save(force_insert=True)

            auth_token = self.__encode_auth_token(user.name)

            response = {
                'message': 'User created successfully'
            }

            return jsonify(response), 201

        except (InvalidEmail, InvalidPassword) as error:
            return jsonify(
                {
                    'message': str(error)
                }
            ), 403
        
        except mongoengine.errors.NotUniqueError as error:
            return jsonify(
                {
                    'error': str(error),
                    'message': 'User already exists'
                }
            ), 403

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
                        'auth_token': auth_token.decode('utf-8'),
                        'message': 'User signed in successfully'
                    }
                ), 201
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

    def get(self) -> tuple:
        """Find user using the auth token and return its data

        Returns:
            tuple: (Response, int), Response object and its status code
        """
        try:
            token = self.__get_auth_token()
            
            if self.__is_token_blacklisted(token):
                print('blacklisted')
                raise InvalidToken
            
            email = self.__decode_auth_token(token)
            
            user = User.objects(email=email)

            if user:
                return jsonify(
                    {
                        'name': user[0].name,
                        'email': user[0].email
                    }
                ), 200
            
            else:
                self.__insert_into_blacklist(token)
                raise InvalidToken

        except (InvalidToken, ExpiredToken, TokenNotDeclared) as error:
            return jsonify(
                {
                    'message': str(error)
                }
            ), 401
        
        except Exception as error:
            return jsonify({
                'error': str(error)
            }), 404

    def logout(self) -> tuple:
        """Perform user's logout by using his auth token

        Returns:
            tuple: (Response, int), HTTP Response object and its status code
        """
        try:
            token = self.__get_auth_token()

            if not self.__is_token_blacklisted(token):
                self.__insert_into_blacklist(token)
            
            email = self.__decode_auth_token(token)
            user = User.objects(email=email)

            if user:    
                return jsonify(
                    {
                        'message': 'User logged out successfully'
                    }
                ), 201
            
            else:
                raise InvalidToken

        except (InvalidToken, ExpiredToken, TokenNotDeclared) as error:
            return jsonify(
                {
                    'message': str(error)
                }
            ), 401
