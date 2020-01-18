from datetime import datetime
from mongoengine import fields
from flask_mongoengine import MongoEngine

db = MongoEngine()


class BaseModelMixin:
    is_deleted = fields.BooleanField(default=False)
    created_at = fields.DateTimeField(default=datetime.now)
    updated_at = fields.DateTimeField(default=datetime.now)
