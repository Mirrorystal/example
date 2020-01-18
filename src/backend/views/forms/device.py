from wtforms import Form, StringField, validators
from views.helper.exceptions import FormLoadException
from models.equipment import Equipment
from . import ObjectIdField
from .public_form import PublicSearchForm


class CreateOrUpdateForm(Form):
    name = StringField(validators=[validators.DataRequired()])
    type = StringField(validators=[validators.DataRequired()])
    location = StringField(validators=[validators.DataRequired()])
    system = StringField(validators=[validators.DataRequired()])
    sn = StringField(validators=[validators.DataRequired()])
    manufacturer = StringField(validators=[validators.DataRequired()])
    note = StringField()
    parentEquipmentId = ObjectIdField(validators=[validators.DataRequired()])

    def load(self, device):
        device.name = self.name.data
        device.type = self.type.data
        device.location = self.location.data
        device.system = self.system.data
        device.sn = self.sn.data
        device.manufacturer = self.manufacturer.data
        device.note = self.note.data
        try:
            parent_equipment = Equipment.objects().get(id=self.parentEquipmentId.data)
        except Equipment.DoesNotExist:
            raise FormLoadException('装置不存在，id: ' + str(self.parentEquipmentId.data))
        else:
            device.parent_equipment = parent_equipment.id


class SearchForm(PublicSearchForm):
    sn = StringField()
    manufacturer = StringField()
    parentEquipmentId = ObjectIdField()
    system = StringField()

