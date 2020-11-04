import pytest
from mongoengine import ValidationError

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
]

@pytest.mark.parametrize(
    'email, should_raise_validation_error', 
    validate_email_function_test_parameters
)
def test_validate_email(email: str, should_raise_validation_error: bool):
    try:
        validate.email(email)
    except ValidationError:
        assert should_raise_validation_error


@pytest.mark.parametrize(
    'text, should_raise_validation_error',
    validate_password_function_test_parameters
)
def test_validate_password(text: str, should_raise_validation_error: bool):
    try:
        validate.password(text)
    except ValidationError:
        assert should_raise_validation_error
