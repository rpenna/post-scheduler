import re
from mongoengine import ValidationError

def email(email: str) -> None:
    """Validate e-mail

    Args:
        email (str): E-mail to be validated

    Raises:
        ValidationError: The e-mail is invalid
    """
    if re.match(r'^[a-z0-9\._]+@[a-z0-9]+\.[a-z]+(\.[a-z]+)?$', email) is None:
        raise ValidationError('Invalid e-mail')
    
def password(text: str) -> None:
    """Validate password

    Args:
        text (str): Password to be validated

    Raises:
        ValidationError: The password is invalid
    """
    if not text or type(text) != str:
        raise ValidationError('Invalid password')
