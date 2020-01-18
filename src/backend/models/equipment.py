from . import db
from .appliance import BaseApplianceMixin
from .image import Image
from mongoengine import fields


# 装置
class Equipment(db.Document, BaseApplianceMixin):
    name = fields.StringField()
    type = fields.StringField()
    location = fields.StringField()
    sn = fields.StringField()
    manufacturer = fields.StringField()
    note = fields.StringField()

    images = fields.ListField(fields.ReferenceField(Image))

    meta = {
        'indexes': [
            ('is_deleted', 'is_template'),
            ('name', 'note', 'is_deleted', 'is_template'),
            ('_create_user', 'is_deleted', 'is_template'),
            ('created_at', 'is_deleted', 'is_template'),
         ]
    }


