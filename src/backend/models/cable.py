from . import db
from .image import Image
from .device import Device
from .interface import Interface
from .equipment import Equipment
from .appliance import BaseApplianceMixin
from mongoengine import fields, CASCADE


class Cable(db.Document, BaseApplianceMixin):

    name = fields.StringField(default=None)
    signal_type = fields.StringField(default=None)
    shield_type = fields.StringField(default=None)
    note = fields.StringField(default=None)
    is_custom = fields.BooleanField(default=False)
    parameter_list = fields.StringField(default=None)

    images = fields.ListField(fields.ReferenceField(Image))

    _start_equipment = fields.LazyReferenceField(Equipment, db_field='start_equipment_id', reverse_delete_rule=CASCADE)
    _start_device = fields.LazyReferenceField(Device, db_field='start_device_id', reverse_delete_rule=CASCADE)
    _start_interface = fields.LazyReferenceField(Interface, db_field='start_interface_id', reverse_delete_rule=CASCADE)

    _end_equipment = fields.LazyReferenceField(Equipment, db_field='end_equipment_id', reverse_delete_rule=CASCADE)
    _end_device = fields.LazyReferenceField(Device, db_field='end_device_id', reverse_delete_rule=CASCADE)
    _end_interface = fields.LazyReferenceField(Interface, db_field='end_interface_id', reverse_delete_rule=CASCADE)

    meta = {
        'indexes': [
            ('is_deleted', 'is_template'),
            ('name', 'note', 'is_deleted', 'is_template'),
            ('_start_equipment', 'is_deleted', 'is_template'),
            ('_start_device', 'is_deleted', 'is_template'),
            ('_start_interface', 'is_deleted', 'is_template'),
            ('_end_equipment', 'is_deleted', 'is_template'),
            ('_end_device', 'is_deleted', 'is_template'),
            ('_end_interface', 'is_deleted', 'is_template'),
            ('_create_user', 'is_deleted', 'is_template'),
            ('created_at', 'is_deleted', 'is_template'),
         ]
    }

    @property
    def start_device(self):
        try:
            start_device = self._start_device.fetch()
            return start_device if not start_device.is_deleted or not self.is_template else None
        except Device.DoesNotExist:
            return None

    @start_device.setter
    def start_device(self, start_device):
        self._start_device = start_device

    @property
    def start_equipment(self):
        try:
            start_equipment = self._start_equipment.fetch()
            return start_equipment if not start_equipment.is_deleted or not self.is_template else None
        except Equipment.DoesNotExist:
            return None

    @start_equipment.setter
    def start_equipment(self, start_equipment):
        self._start_equipment = start_equipment

    @property
    def start_interface(self):
        try:
            start_interface = self._start_interface.fetch()
            return start_interface if not start_interface.is_deleted or not self.is_template else None
        except Interface.DoesNotExist:
            return None

    @start_interface.setter
    def start_interface(self, start_interface):
        self._start_interface = start_interface

    @property
    def end_device(self):
        try:
            end_device = self._end_device.fetch()
            return end_device if not end_device.is_deleted or not self.is_template else None
        except Device.DoesNotExist:
            return None

    @end_device.setter
    def end_device(self, end_device):
        self._end_device = end_device

    @property
    def end_equipment(self):
        try:
            end_equipment = self._end_equipment.fetch()
            return end_equipment if not end_equipment.is_deleted or not self.is_template else None
        except Equipment.DoesNotExist:
            return None

    @end_equipment.setter
    def end_equipment(self, end_equipment):
        self._end_equipment = end_equipment

    @property
    def end_interface(self):
        try:
            end_interface = self._end_interface.fetch()
            return end_interface if not end_interface.is_deleted or not self.is_template else None
        except Interface.DoesNotExist:
            return None

    @end_interface.setter
    def end_interface(self, end_interface):
        self._end_interface = end_interface
