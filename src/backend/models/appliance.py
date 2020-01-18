from mongoengine import fields
from .user import User
from . import BaseModelMixin


class BaseApplianceMixin(BaseModelMixin):

    is_template = fields.BooleanField(default=False)
    _verify_user = fields.LazyReferenceField(User, db_field='verify_user_id')

    _create_user = fields.LazyReferenceField(User, required=True, db_field='create_user_id')
    _update_user = fields.LazyReferenceField(User, required=True, db_field='update_user_id')

    update_num = fields.IntField(default=1)
    updatable = fields.BooleanField(default=True)

    @property
    def create_user(self):
        try:
            return self._create_user.fetch()
        except User.DoesNotExist:
            return None

    @create_user.setter
    def create_user(self, create_user):
        self._create_user = create_user

    @property
    def update_user(self):
        try:
            return self._update_user.fetch()
        except User.DoesNotExist:
            return None

    @update_user.setter
    def update_user(self, update_user):
        self._update_user = update_user

    @property
    def verify_user(self):
        try:
            return self._verify_user.fetch()
        except User.DoesNotExist:
            return None

    @verify_user.setter
    def verify_user(self, verify_user):
        self._verify_user = verify_user
