import os
import binascii

from . import db, BaseModelMixin
from mongoengine import fields
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256


class Token(fields.EmbeddedDocument):
    value = fields.StringField(required=True)
    expired_at = fields.DateTimeField()


class User(db.Document, BaseModelMixin):
    username = fields.StringField()
    _password = fields.StringField(db_field='password')
    email = fields.EmailField(unique=True)
    avatar = fields.StringField(default=None)
    position = fields.StringField()  # 职位
    department = fields.StringField()  # 部门
    phone = fields.StringField()

    equipment_num = fields.LongField(default=0)  # 装置数量
    device_num = fields.LongField(default=0)  # 设备数量
    interface_num = fields.LongField(default=0)  # 接口数量
    cable_num = fields.LongField(default=0)  # 线缆数量

    login_num = fields.LongField(default=0)
    search_num = fields.LongField(default=0)

    author_type = fields.IntField(default=0)
    author_editable = fields.BooleanField(default=True)
    deletable = fields.BooleanField(default=True)
    is_active = fields.BooleanField(default=True)
    token = fields.EmbeddedDocumentField(Token, default=None)

    is_anonymous = False

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return self.is_active and self.token is not None and self.token.expired_at > datetime.now()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        self._password = pbkdf2_sha256.hash(pwd)

    def check_password(self, pwd):
        return pbkdf2_sha256.verify(pwd, self._password)

    def refresh_token(self, token_expired_time):
        self.token.expired_at = datetime.now() + timedelta(seconds=token_expired_time)
        return self.save()

    def generate_token(self, token_expired_time):
        token = binascii.hexlify(os.urandom(20) + str(self.id).encode('utf-8')).decode()
        expired_at = datetime.now() + timedelta(seconds=token_expired_time)
        self.token = Token(value=token, expired_at=expired_at)
        self.login_num += 1
        self.save()
        return self.token.value
