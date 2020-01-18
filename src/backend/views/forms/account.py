from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import Form, StringField, PasswordField, validators

from . import JsonField, ObjectIdListField

"""用户"""


class LoginForm(Form):
    username = StringField(validators=[validators.Email(), validators.DataRequired(), ])
    password = StringField(validators=[validators.DataRequired(), validators.Length(min=8, max=24)])


class SearchForm(Form):
    searchKey = StringField(validators=[validators.Length(max=125)], default=None)
    position = StringField(validators=[validators.Length(max=125)], default=None)
    department = StringField(validators=[validators.Length(max=125)], default=None)
    orderBy = JsonField()


class UpdateForm(Form):
    phone = StringField(validators=[validators.Length(max=11, min=11)])
    username = StringField(validators=[validators.Length(max=40)])
    position = StringField()
    department = StringField()
    avatar = StringField()

    def load(self, user):
        user.phone = self.phone.data
        user.username = self.username.data
        user.position = self.position.data
        user.department = self.department.data
        user.avatar = self.avatar.data


class CreateForm(UpdateForm):
    email = StringField(validators=[validators.Email(), validators.DataRequired()])

    def load(self, user):
        super().load(user)
        user.email = self.email.data


class DeleteForm(Form):
    userIds = ObjectIdListField(validators=[validators.DataRequired()], default=None)


class PasswordUpdateForm(Form):
    newPassword = PasswordField('New Password', [validators.InputRequired(), validators.DataRequired(),
                                                 validators.Length(min=8, max=25)])


class ImportUserForm(Form):
    file = FileField(validators=[FileRequired(), FileAllowed(['xlsx'], 'Excel only!')])
