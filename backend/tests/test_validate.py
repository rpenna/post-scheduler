import pytest
from src.util.exceptions import InvalidPassword, InvalidEmail

from src.util import validate

validate_email_function_test_parameters = [
    ('rachel_green@friends.com', False),
    ('rachel.green@friends.com', False),
    ('rachelgreen@friends.com', False),
    ('1rachel_green@friends.com', False),
    ('.rachel_green@friends.com', False),
    ('rachel_green@friends.com.br', False),
    ('rachel_green@friends.com.br.fail', True),
    ('rachel_green@friends', True),
    ('rachel@green@friends.com', True),
    ('rachel@green@friends.com', True),
    ('rachel^green@friends.com', True),
    ('rachel^green@friends.com', True),
]

validate_password_function_test_parameters = [
    ('password_test', False),
    (['password_test'], True),
    (
        {
            'password': 'password_test'
        }, 
        True
    ),
    (123456, True),
    (True, True),
    (123.45, True),
    ('short', True),
    ('', True),
]

@pytest.mark.parametrize(
    'email, should_raise_invalid_email', 
    validate_email_function_test_parameters
)
def test_validate_email(email: str, should_raise_invalid_email: bool):
    try:
        validate.email(email)
    except InvalidEmail:
        assert should_raise_invalid_email


@pytest.mark.parametrize(
    'text, should_raise_invalid_password',
    validate_password_function_test_parameters
)
def test_validate_password(text: str, should_raise_invalid_password: bool):
    try:
        validate.password(text)
    except InvalidPassword:
        assert should_raise_invalid_password
