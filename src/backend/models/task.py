from . import db
from .user import User
from datetime import datetime
from mongoengine import fields


class TaskFile(fields.EmbeddedDocument):
    name = fields.StringField()
    mimetype = fields.StringField()
    path = fields.StringField()


class Task(db.Document):
    name = fields.StringField()
    status = fields.StringField()
    params = fields.DictField(default={})
    file = fields.EmbeddedDocumentField(TaskFile)
    result = fields.DictField(default={})
    create_user = fields.ReferenceField(User, required=True, db_field='create_user_id')
    created_at = fields.DateTimeField(default=datetime.now)

    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILURE = 'failure'
