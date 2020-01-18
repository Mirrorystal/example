from os import path
from . import db, BaseModelMixin
from flask import current_app
from .user import User
from mongoengine import fields
from datetime import datetime


def get_file_ext(filename):
    return path.splitext(filename)[1]


class Image(db.Document, BaseModelMixin):
    name = fields.StringField()
    type = fields.StringField()

    _create_user = fields.LazyReferenceField(User, required=True, db_field='create_user_id')

    @property
    def url(self):
        resource_context = current_app.config['STATIC_RESOURCE_CONTEXT']
        date_path = datetime.strftime(self.created_at, '%Y/%m')
        return path.join(resource_context, date_path, self.real_name)

    @property
    def real_name(self):
        return str(self.id) + get_file_ext(self.name)

    @property
    def create_user(self):
        return self._create_user.fetch()

    @create_user.setter
    def create_user(self, create_user):
        self._create_user = create_user
