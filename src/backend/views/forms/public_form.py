# 存放一些公共表单
from wtforms import Form, StringField, DateTimeField, BooleanField
from . import ObjectIdListField, ObjectIdField
from views.forms import JsonField


# 批量操作表单。用于装置和接口的批量删除和批量设置模板
class ObjectIdListForm(Form):
    ids = ObjectIdListField()


# 装置和接口的查询表单
class PublicSearchForm(Form):
    searchKey = StringField()
    name = StringField()
    type = StringField()
    location = StringField()
    note = StringField()
    createUserId = ObjectIdField()
    createdAtStart = DateTimeField()
    createdAtEnd = DateTimeField()
    orderBy = JsonField()


# 用于回收站和模板的简单搜索
class SimpleSearchForm(Form):
    searchKey = StringField()
    orderBy = JsonField()

    verified = BooleanField()
