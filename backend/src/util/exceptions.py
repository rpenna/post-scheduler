class InvalidPassword(Exception):
    def __init__(self, message='Invalid Password'):
        super().__init__(message)

class InvalidEmail(Exception):
    def __init__(self, message='Invalid Email'):
        super().__init__(message)

class InvalidToken(Exception):
    def __init__(self, message='Invalid token'):
        super().__init__(message)

class ExpiredToken(Exception):
    def __init__(self, message='The token has expired'):
        super().__init__(message)
