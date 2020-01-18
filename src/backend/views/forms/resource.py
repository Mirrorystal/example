from wtforms import Form
from flask_uploads import IMAGES
from flask_wtf.file import FileField, FileAllowed, FileRequired


class ImageUploadForm(Form):
    file = FileField(validators=[FileRequired(), FileAllowed(IMAGES, 'Images only!')])
