from . import db
from .user import User
from mongoengine import fields, ReferenceField
from datetime import datetime


class Keyword(db.Document):
    word = fields.StringField(default=None)  # 用户查询关键词
    frequency = fields.IntField(default=0)  # 查询次数
    user = fields.ListField(ReferenceField(User))  # 查询者ID
    create_at = fields.DateTimeField(default=datetime.utcnow())
    update_at = fields.DateTimeField(default=datetime.utcnow())
