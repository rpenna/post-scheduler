import pytest

from src.util import crypto

password_parameters = [
    'lowercaselettersonly',
    'UPPERCASELETTERSONLY',
    'UpperAndLowerCaseLetters',
    'special_chars',
    'speci@lChars',
    'sp&cialChars',
    'spec!alChars',
    '$pecialChars',
    'numbers123',
    '123456',
]

@pytest.mark.parametrize('password', password_parameters)
def test_crypto_right_password(password: str):
    encrypted_password = crypto.encrypt(password)
    assert crypto.check_encrypted(password, encrypted_password)


@pytest.mark.parametrize('password', password_parameters)
def test_crypto_wrong_password(password: str):
    encrypted_password = crypto.encrypt(password)
    
    assert not crypto.check_encrypted(
        password + 'wrong_password',
        encrypted_password
    )
