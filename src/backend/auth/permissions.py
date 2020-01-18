from functools import wraps
from flask import current_app, jsonify
from flask_login import current_user


def admin_required(func):
    """限制只能管理员才能调用"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif current_user.author_type == 0:
            return jsonify(ok=False, msg="你不是管理员，权限不足"), 403
        return func(*args, **kwargs)

    return decorated_view


class admin_or_owner_required(object):
    """限制只有管理员或者拥有者才能调用"""
    def __init__(self, document):
        self.document = document

    def __call__(self, func):

        @wraps(func)
        def decorated_view(oid):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()

            try:
                model = self.document.objects.get(id=oid)
            except self.document.DoesNotExist:
                return func(oid=oid)

            if current_user.author_type > 0:
                return func(oid=oid, model=model)
            elif model.create_user.id == current_user.id:
                return func(oid=oid, model=model)
            return jsonify(ok=False, msg="你不是管理员或拥有者，权限不足"), 403

        return decorated_view
