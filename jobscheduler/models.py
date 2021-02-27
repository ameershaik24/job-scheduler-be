from mongoengine import *
from django.utils import timezone
from datetime import datetime

def notifications_default():
    return {"phones": [], "emails": []}

def request_default():
    return {"url":"", "method":""}

def created_default():
    return str(timezone.now())

class Requests(Document):
    status = StringField(max_length=200, default="Created", required=True)
    name = StringField(max_length=200, required=True)
    notifications = DictField(default=notifications_default)
    timezone = StringField(max_length=3, default="UTC")
    request = DictField(default=request_default)
    request_interval_seconds = IntField()
    tolerated_failures = StringField()
    created = StringField(default=created_default)
    updated = DateTimeField(default=datetime.utcnow)
