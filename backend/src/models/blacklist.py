from mongoengine import *
from datetime import datetime

class Blacklist(Document):
    token = StringField(
        max_length=500, 
        required=True
    )

    ts_blacklisted = DateTimeField(
        required=True,
        default=datetime.now()
    )
