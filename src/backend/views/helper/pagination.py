from functools import wraps
from flask import request
from werkzeug.exceptions import HTTPException
from wtforms import Form, validators, IntegerField
from flask_mongoengine import Pagination
from flask_restful import marshal, fields
from flask_restful.utils import unpack

pagination_fields = {
    'page': fields.Integer,
    'pageSize': fields.Integer,
    'pageCount': fields.Integer,
    'totalCount': fields.Integer
}


class PaginationForm(Form):
    page = IntegerField(validators=[validators.NumberRange(min=1)], default=1)
    pageSize = IntegerField(validators=[validators.NumberRange(min=1)], default=10)


class RestPagination(Pagination):
    def __init__(self, data, page, per_page):
        try:
            super().__init__(data, page, per_page)
        except HTTPException as error:
            if error.code == 404:
                self.items = []
                self.page = page
                self.per_page = per_page
                self.total = len(data)
            else:
                raise error


class pagination_marshal_with(object):
    def __init__(self, _fields, envelope=None):
        self.fields = {
            'meta': fields.Nested(pagination_fields),
            'items': fields.List(fields.Nested(_fields))
        }
        self.envelope = envelope

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            resp = f(*args, **kwargs)
            if isinstance(resp, tuple):
                data, code, headers = unpack(resp)
                return marshal(self._build_response(data), self.fields, self.envelope), code, headers
            else:
                return marshal(self._build_response(resp), self.fields, self.envelope)
        return wrapper

    @staticmethod
    def _build_response(data):
        form = PaginationForm(request.args)
        pagination = RestPagination(data, form.page.data, form.pageSize.data)
        return {
            'meta': {
                'page': form.page.data,
                'pageSize': form.pageSize.data,
                'pageCount': pagination.pages,
                'totalCount': pagination.total
            },
            'items': pagination.items
        }


def build_order_by(query, order_by):
    if len(order_by) > 0:
        key, sort = order_by.popitem()
        sort = '-' if sort == 'desc' else ''
        return query.order_by(sort + key)
    return query.order_by('-created_at')
