class InvalidPassword(Exception):
    def __init__(self, message='Invalid Password'):
        super().__init__(message)

class InvalidEmail(Exception):
    def __init__(self, message='Invalid Email'):
        super().__init__(message)
