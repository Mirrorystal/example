from copy import copy
from functools import wraps
from datetime import datetime
from flask_login import current_user
from flask import request, jsonify
from flask_restful import marshal
from ..helper.exceptions import FormLoadException
from ..forms.public_form import ObjectIdListForm, SimpleSearchForm
from .pagination import build_order_by
from mongoengine.queryset.visitor import Q


class base_view(object):

    def __init__(self, document, fields):
        self.fields = fields
        self.document = document

    def __call__(self, func):

        @wraps(func)
        def decorated_view(oid, model=None):
            if model is None:
                try:
                    model = self.document.objects.get(id=oid, is_deleted=False)
                except self.document.DoesNotExist:
                    return jsonify(ok=False, msg='not found'), 404
            if model.is_deleted:
                return jsonify(ok=False, msg='not found'), 404
            return marshal(model, self.fields)

        return decorated_view


class base_create(object):

    def __init__(self, document, form):
        self.document = document
        self.form = form

    def __call__(self, func):

        @wraps(func)
        def decorated_view():
            form = self.form(request.form)
            if not form.validate():
                return form.errors, 400
            model = self.document()
            try:
                form.load(model)
            except FormLoadException as e:
                return jsonify(ok=False, msg=e.message)
            else:
                model.update_user = current_user.id
                model.create_user = current_user.id
                model.save()
                return jsonify(ok=True, msg='success', id=str(model.id))

        return decorated_view


class base_update(object):

    def __init__(self, document, form):
        self.document = document
        self.form = form

    def __call__(self, func):

        @wraps(func)
        def decorated_view(oid, model=None):
            form = self.form(request.form)
            if not form.validate():
                return form.errors, 400
            if model is None:
                try:
                    model = self.document.objects.get(id=oid)
                except self.document.DoesNotExist:
                    return jsonify(ok=False, msg='not found')

            if model is None or model.is_deleted:
                return jsonify(ok=False, msg='not found')

            if model.is_template:
                return jsonify(ok=False, msg='not found')

            if not model.updatable:
                return jsonify(ok=False, msg='no updatable')
            try:
                old = copy(model)
                form.load(model)
            except FormLoadException as e:
                return jsonify(ok=False, msg=e.message)
            else:
                model.update_num += 1
                model.update_user = current_user.id
                model.updated_at = datetime.now()
                model.save()
                resp = jsonify(ok=True, msg='success')
                return func(new=model, old=old, response=resp)

        return decorated_view


class base_delete(object):

    def __init__(self, document):
        self.document = document

    def __call__(self, func):

        @wraps(func)
        def decorated_view(oid, model=None):
            if model is None:
                try:
                    model = self.document.objects.get(id=oid, is_deleted=False)
                except self.document.DoesNotExist:
                    return jsonify(ok=True, msg='not found')

            if model is None or model.is_deleted:
                return jsonify(ok=True, msg='not found')

            model.is_deleted = True
            model.save()
            resp = jsonify(ok=True, msg='success')
            return func(oid=oid, response=resp)

        return decorated_view


class base_delete_many(object):

    def __init__(self, document):
        self.document = document

    def __call__(self, func):

        @wraps(func)
        def decorated_view():
            form = ObjectIdListForm(request.args)
            ids = form.ids.data
            self.document.objects(id__in=ids).update(set__is_deleted=True)
            return jsonify(ok=True, msg='success')

        return decorated_view


class base_copy_templates(object):
    def __init__(self, document):
        self.document = document

    def __call__(self, func):

        @wraps(func)
        def decorated_view():
            form = ObjectIdListForm(request.form)
            ids = form.ids.data
            templates = self.document.objects(id__in=ids).clone()
            for temp in templates:
                temp.id = None
                temp.is_template = True
                temp.create_user = current_user.id
                temp.update_user = current_user.id
                temp.created_at = datetime.now()
                temp.updated_at = temp.created_at
                temp.update_num = 1
                temp.save()
            return jsonify(ok=True, msg='success')
        return decorated_view


class base_update_templates():
    def __init__(self, document, form):
        self.document = document
        self.form = form

    def __call__(self, func):

        @wraps(func)
        def decorated_view(oid, model=None):
            form = self.form(request.form)
            if model is None:
                try:
                    model = self.document.objects.get(id=oid)
                except self.document.DoesNotExist:
                    return jsonify(ok=False, msg='not found')

            if model is None or model.is_deleted:
                return jsonify(ok=False, msg='not found')

            if not model.is_template:
                return jsonify(ok=False, msg='not a template')

            if not model.updatable:
                return jsonify(ok=False, msg='no updatable')
            try:
                old = copy(model)
                form.load(model)
            except FormLoadException as e:
                return jsonify(ok=False, msg=e.message)
            else:
                model.update_num += 1
                model.update_user = current_user.id
                model.updated_at = datetime.now()
                model.save()
                resp = jsonify(ok=True, msg='success')
                return func(new=model, old=old, response=resp)

        return decorated_view


class base_get_templates(object):
    def __init__(self, document):
        self.document = document

    def __call__(self, func):

        @wraps(func)
        def decorated_view():
            form = SimpleSearchForm(request.args)
            query = self.document.objects(is_deleted=False, is_template=True)

            if form.verified.data:
                query = query.filter(_verify_user__exists=True)

            if form.searchKey.data:
                search_key = form.searchKey.data
                query = query.filter(Q(name__contains=search_key) | Q(note__contains=search_key))
            return build_order_by(query, form.orderBy.data)
        return decorated_view


class base_verify_templates(object):
    def __init__(self, document):
        self.document = document

    def __call__(self, func):

        @wraps(func)
        def decorated_view():
            form = ObjectIdListForm(request.form)
            ids = form.ids.data
            self.document.objects(id__in=ids, is_template=True).update(set___verify_user=current_user.id)
            return jsonify(ok=True, msg='success')
        return decorated_view


class base_get_recycles(object):
    def __init__(self, document):
        self.document = document

    def __call__(self, func):

        @wraps(func)
        def decorated_view():
            form = SimpleSearchForm(request.args)
            query = self.document.objects(is_deleted=True, is_template=False)
            if current_user.author_type == 0:
                query = query.filter(Q(create_user=current_user.id))
            search_key = form.searchKey.data
            if search_key:
                query = query.filter(Q(name__contains=search_key) | Q(note__contains=search_key))
            return build_order_by(query, form.orderBy.data)

        return decorated_view


class base_delete_recycles(object):
    def __init__(self, document):
        self.document = document

    def __call__(self, func):

        @wraps(func)
        def decorate_view():
            form = ObjectIdListForm(request.args)
            ids = form.ids.data
            self.document.objects(id__in=ids, is_deleted=True).delete()
            return jsonify(ok=True, msg='success')
        return decorate_view


class base_recover_recycles(object):
    def __init__(self, document):
        self.document = document

    def __call__(self, func):

        @wraps(func)
        def decorate_view():
            form = ObjectIdListForm(request.form)
            ids = form.ids.data
            return func(ids=ids)
        return decorate_view


class get_templates_recycles(object):
    def __init__(self, document):
        self.document = document

    def __call__(self, func):

        @wraps(func)
        def decorated_view():
            form = SimpleSearchForm(request.args)
            query = self.document.objects(is_deleted=True, is_template=True)
            if current_user.author_type == 0:
                query = query.filter(Q(create_user=current_user.id))
            search_key = form.searchKey.data
            if search_key:
                query = query.filter(Q(name__contains=search_key) | Q(note__contains=search_key))
            return build_order_by(query, form.orderBy.data)

        return decorated_view
