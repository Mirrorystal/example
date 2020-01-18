from wtforms import Form, validators
from wtforms.fields import StringField


class UpdateSettingForm(Form):

    nameString = ["departments", "positions", "shieldTypes", "spliceTypes", "interfaceProtocol"]
    name = StringField(validators=[validators.any_of(nameString)])
    value = StringField(validators=[validators.length(max=125)])

