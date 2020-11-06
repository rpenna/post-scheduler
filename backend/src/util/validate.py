import re
from src.util.exceptions import InvalidEmail, InvalidPassword

def email(email: str) -> None:
    """Validate e-mail

    Args:
        email (str): E-mail to be validated

    Raises:
        ValidationError: The e-mail is invalid
    """
    if re.match(r'^[a-z0-9\._]+@[a-z0-9]+\.[a-z]+(\.[a-z]+)?$', email) is None:
        raise InvalidEmail('Unrecognized e-mail format')
    
def password(text: str) -> None:
    """Validate password

    Args:
        text (str): Password to be validated

    Raises:
        ValidationError: The password is invalid
    """
    if not text or type(text) != str:
        raise InvalidPassword('Invalid password type')
    
    if len(text) < 6:
        raise InvalidPassword('Password is too short')
