from . import db
from .user import User
from mongoengine import fields
from datetime import datetime


class Setting(db.Document):
    departments = fields.ListField(default=[])
    positions = fields.ListField(default=[])
    shield_types = fields.ListField(default=[])
    splice_types = fields.ListField(default=[])
    interface_protocol = fields.ListField(default=[])

    update_at = fields.DateTimeField(default=datetime.now())
    update_user = fields.ReferenceField(User, required=True, db_field='update_user_id')
