from wtforms import Field, widgets
from json import loads
from bson import ObjectId
import re


class JsonField(Field):
    widget = widgets.TextInput()

    def process_formdata(self, valuelist):
        if valuelist and len(valuelist) > 0:
            data = valuelist[0]
            self.data = loads(data)
        else:
            self.data = {}


class StringListFiled(Field):

    def process(self, formdata):
        self.data = []
        if not formdata:
            return
        for k in formdata:
            if k.startswith(self.name):
                self.data.append(formdata[k])


class ObjectIdField(Field):

    def process_formdata(self, valuelist):
        if valuelist and len(valuelist) > 0:
            match_result = re.match(r'^\w{24}$', valuelist[0])
            self.data = ObjectId(valuelist[0]) if match_result is not None else None
        else:
            self.data = None


class ObjectIdListField(StringListFiled):

    def process(self, formdata):
        super().process(formdata)
        result = []
        for oid in self.data:
            if re.match(r'^\w{24}$', oid) is not None:
                oid = ObjectId(oid)
                result.append(oid)
