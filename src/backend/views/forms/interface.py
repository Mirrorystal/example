from wtforms import Form, StringField, validators
from views.helper.exceptions import FormLoadException
from . import ObjectIdField
from .public_form import PublicSearchForm
from models.equipment import Equipment
from models.device import Device


class CreateOrUpdateForm(Form):
    name = StringField(validators=[validators.DataRequired()])
    type = StringField(validators=[validators.DataRequired()])
    protocol = StringField(validators=[validators.DataRequired()])
    location = StringField(validators=[validators.DataRequired()])
    note = StringField()
    pcl = StringField(validators=[validators.DataRequired()])
    parentDeviceId = ObjectIdField(validators=[validators.DataRequired()])

    def load(self, interface):
        interface.name = self.name.data
        interface.type = self.type.data
        interface.protocol = self.protocol.data
        interface.location = self.location.data
        interface.note = self.note.data
        interface.pcl = self.pcl.data
        try:
            parent_device = Device.objects().get(id=self.parentDeviceId.data)
            parent_equipment = parent_device.parent_equipment
        except Device.DoesNotExist:
            raise FormLoadException('设备不存在，id: ' + str(self.parentDeviceId.data))
        except Equipment.DoesNotExist:
            raise FormLoadException('设备所属的装置不存在，设备id: ' + str(self.parentDeviceId.data))
        else:
            interface.parent_device = parent_device.id
            interface.parent_equipment = parent_equipment.id


class SearchForm(PublicSearchForm):
    protocol = StringField(validators=[validators.Length(max=125)], default=None)
    parentEquipmentId = ObjectIdField()
    parentDeviceId = ObjectIdField()

