from . import db
from .image import Image
from .device import Device
from .equipment import Equipment
from .appliance import BaseApplianceMixin
from mongoengine import fields, CASCADE


class Interface(db.Document, BaseApplianceMixin):
    name = fields.StringField()
    type = fields.StringField()
    protocol = fields.StringField()
    location = fields.StringField()
    note = fields.StringField()
    pcl = fields.StringField()

    _parent_device = fields.LazyReferenceField(Device, db_field='parent_device_id', reverse_delete_rule=CASCADE)
    _parent_equipment = fields.LazyReferenceField(Equipment, db_field='parent_equipment_id', reverse_delete_rule=CASCADE)

    images = fields.ListField(fields.ReferenceField(Image))

    meta = {
        'indexes': [
            ('is_deleted', 'is_template'),
            ('name', 'note', 'is_deleted', 'is_template'),
            ('_parent_device', 'is_deleted', 'is_template'),
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

    @property
    def parent_device(self):
        try:
            device = self._parent_device.fetch()
            return device if not device.is_deleted or not self.is_template else None
        except Device.DoesNotExist:
            return None


    @parent_device.setter
    def parent_device(self, parent_device):
        self._parent_device = parent_device
