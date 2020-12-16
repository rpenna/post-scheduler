# source: https://blog.tecladocode.com/learn-python-encrypting-passwords-python-flask-and-passlib/
from passlib.context import CryptContext
from src.util import validate

crypt_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

def encrypt(text: str) -> str:
    """Encrypt a text

    Args:
        text (str): text to be encrypted

    Returns:
        str: encrypted text, or empty string if text is None
    """
    validate.password(text)
    return crypt_context.hash(text)

def check_encrypted(text: str, encrypted: str) -> bool:
    """Check if the text is equal to the encrypted value

    Args:
        text (str): Text to be checked
        encrypted (str): Encrypted version to be compared

    Returns:
        bool: True if the text is equal to the encrypted version
    """
    return crypt_context.verify(text, encrypted)
