from wtforms import Form, StringField, validators
from .public_form import PublicSearchForm


class CreateOrUpdateForm(Form):
    name = StringField(validators=[validators.DataRequired()])
    type = StringField(validators=[validators.DataRequired()])
    location = StringField(validators=[validators.DataRequired()])
    sn = StringField(validators=[validators.DataRequired()])
    manufacturer = StringField(validators=[validators.DataRequired()])
    note = StringField()

    def load(self, equipment):
        equipment.name = self.name.data
        equipment.type = self.type.data
        equipment.location = self.location.data
        equipment.sn = self.sn.data
        equipment.manufacturer = self.manufacturer.data
        equipment.note = self.note.data


class SearchForm(PublicSearchForm):
    sn = StringField()
    manufacturer = StringField()
