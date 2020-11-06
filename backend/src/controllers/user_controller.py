from src.models.user import User
from src.util import crypto
from src.util.exceptions import InvalidPassword, InvalidEmail

from flask import jsonify, request, Response

class UserController:
    def create_user(self) -> str:
        """Save user in the database

        Returns:
            str: a JSON-formatted string as HTTP response
        """
        try:
            user = User(
                name=request.json.get('name'),
                email=request.json.get('email'),
                password=crypto.encrypt(request.json.get('password'))
            )

            user.save()

            return Response(status=201)

        except (InvalidEmail, InvalidPassword) as error:
            return jsonify(
                {
                    'message': str(error)
                }
            ), 403
