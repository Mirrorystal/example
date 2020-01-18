from . import db
from .image import Image
from .appliance import BaseApplianceMixin
from .equipment import Equipment
from mongoengine import fields, CASCADE


class Device(db.Document, BaseApplianceMixin):
    name = fields.StringField(default=None)
    type = fields.StringField(default=None)
    location = fields.StringField(default=None)
    system = fields.StringField(default=None)
    sn = fields.StringField(default=None)
    manufacturer = fields.StringField(default=None)
    note = fields.StringField(default=None)

    _parent_equipment = fields.LazyReferenceField(Equipment, db_field='parent_equipment_id', reverse_delete_rule=CASCADE)
    images = fields.ListField(fields.ReferenceField(Image))

    meta = {
        'indexes': [
            ('is_deleted', 'is_template'),
            ('name', 'note', 'is_deleted', 'is_template'),
            ('_parent_equipment', 'is_deleted', 'is_template'),
            ('_create_user', 'is_deleted', 'is_template'),
            ('created_at', 'is_deleted', 'is_template'),
         ]
    }

    @property
    def parent_equipment(self):
        try:
            equipment = self._parent_equipment.fetch()
            return equipment if not equipment.is_deleted or not self.is_template else None
        except Equipment.DoesNotExist:
            return None

    @parent_equipment.setter
    def parent_equipment(self, parent_equipment):
        self._parent_equipment = parent_equipment
