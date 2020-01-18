from bson import ObjectId
from werkzeug.routing import BaseConverter


class ObjectIdConverter(BaseConverter):
    def __init__(self, _map):
        super().__init__(_map)
        self.regex = "[0-9a-z]{24}"

    def to_python(self, value):
        return ObjectId(value)

    def to_url(self, value):
        val = str(value)
        return super().to_url(val)
