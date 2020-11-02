from mongoengine import *

from ..util import validate
from .social_media import SocialMedia

class User(Document):
    email = StringField(
        max_length=100, 
        required=True, 
        unique=True, 
        primary_key=True,
        validation=validate.email
    )

    password = StringField(
        max_length=100, 
        required=True, 
        validation=validate.password
    )

    name = StringField(max_length=150)
    
    accounts = ListField(EmbeddedDocumentField(SocialMedia))
