from flask import Blueprint, jsonify, request
from flask_restful import fields, marshal_with, marshal
from flask_login import current_user, login_required
from auth.permissions import admin_required
from mongoengine.errors import NotUniqueError
from mongoengine.queryset.visitor import Q
from auth import auth
from models.user import User
from views.helper.pagination import pagination_marshal_with, build_order_by
from views.forms.account import LoginForm, DeleteForm, CreateForm, SearchForm, UpdateForm, \
    PasswordUpdateForm, ImportUserForm
from app.config import Config
from views.forms.public_form import ObjectIdListForm, SimpleSearchForm
from views.helper.base_views import base_delete_recycles, base_recover_recycles

bp = Blueprint('account', __name__, url_prefix='/account')

user_fields = {
    'id': fields.String,
    'username': fields.String,
    'email': fields.String,
    'avatar': fields.String(default=Config.DEFAULT_AVATAR_URL),
    'position': fields.String,
    'department': fields.String,
    'phone': fields.String,
    'searchNum': fields.Integer(attribute='search_num'),
    'loginNum': fields.Integer(attribute='login_num'),
    'authorType': fields.Integer(attribute='author_type'),
}


@bp.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if not form.validate():
        return form.errors, 400
    user = User.objects(email=form.username.data, is_deleted=False).first()
    if user is None:
        return jsonify(ok=False, msg='用户名或密码错误')
    elif not user.is_active:
        return jsonify(ok=False, msg='用户已被锁定')
    elif user.check_password(form.password.data):
        expired_time = auth.token_expired_time
        return jsonify(ok=True, token=user.generate_token(expired_time), expired_at=expired_time)
    return jsonify(ok=False, msg='用户名或密码错误')


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    current_user.token = None
    current_user.save()
    return jsonify(ok=True, msg='success')


@bp.route('/user', methods=['GET'])
@login_required
@marshal_with(user_fields)
def get_current_user():
    return current_user


@bp.route('/user', methods=['PUT'])
@login_required
def update_current_user():
    form = UpdateForm(request.form)
    if not form.validate():
        return form.errors, 400
    form.load(current_user)
    current_user.save()
    return jsonify(ok=True, msg='success')


@bp.route('/users/meta', methods=['GET'])
@login_required
def get_users_meta():
    users = User.objects(is_deleted=False).fields(id=1, username=1, email=1).all()
    users_meta = [{
        'id': str(user.id),
        'username': user.username,
        'email': user.email
    } for user in users]
    return jsonify(ok=True, data=users_meta)


@bp.route('/users', methods=['GET'])
@admin_required
@pagination_marshal_with(user_fields)
def get_users():
    form = SearchForm(request.args)
    query = User.objects(is_deleted=False)
    if form.searchKey.data:
        search_key = form.searchKey.data
        query = query.filter(Q(username__contains=search_key) | Q(email__contains=search_key) | Q(phone=search_key))
    if form.position.data:
        query = query.filter(position=form.position.data)
    if form.department.data:
        query = query.filter(department=form.department.data)
    current_user.update(inc__search_num=1)
    return build_order_by(query, form.orderBy.data), 200


@bp.route('/user/<oid:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        return marshal(user, user_fields)
    except User.DoesNotExist:
        return jsonify(msg='not found'), 404


@bp.route('/user/<oid:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    form = UpdateForm(request.form)
    if not form.validate():
        return form.errors, 400
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return jsonify(ok=False, msg='not found')
    form.load(user)
    user.save()
    return jsonify(ok=True, msg='success')


@bp.route('/user', methods=['POST'])
@admin_required
def create_user():
    form = CreateForm(request.form)
    if not form.validate():
        return form.errors, 400
    try:
        user = User()
        form.load(user)
        user.password = 'Abc123__'
        user.save()
        return jsonify(ok=True, msg='success')
    except NotUniqueError:
        return jsonify(ok=False, msg='email already exists')


@bp.route('/user/<oid:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return jsonify(ok=True, msg='not found')
    if not user.deletable:
        return jsonify(ok=False, msg='用户不可被删除')
    user.is_deleted = True
    user.save()
    return jsonify(ok=True, msg='success')


@bp.route('/users', methods=['DELETE'])
@admin_required
def delete_users():
    form = DeleteForm(request.args)
    userIds = form.userIds.data
    User.objects(id__in=userIds, deletable=True).update(set__is_deleted=True)
    return jsonify(ok=True, msg='success')


# 登录用户修改自己的密码
@bp.route('/password', methods=['PUT'])
@login_required
def update_password():
    form = PasswordUpdateForm(request.form)
    if not form.validate():
        return form.errors, 400
    if not current_user.check_password(form.newPassword.data):
        current_user.password = form.newPassword.data
        current_user.save()
        return jsonify(ok=True, msg='success')
    else:
        return jsonify(ok=False, msg='new password is invalid')


@bp.route('/user/import', methods=['POST'])
@login_required
def import_users():
    form = ImportUserForm(request.files)
    if not form.validate():
        return form.errors, 400

    from models.task import Task, TaskFile
    from tempfile import mktemp
    from os import path

    task = Task()
    task.name = '导入用户数据'
    task.status = Task.STATUS_PENDING
    task.file = TaskFile()
    task.file.name = form.file.data.filename
    task.file.mimetype = form.file.data.mimetype
    ext = path.splitext(form.file.data.filename)[1]
    task.file.path = mktemp(suffix=ext)
    form.file.data.save(task.file.path)
    task.create_user = current_user.id
    task.save()

    from .executor.import_user import execute
    execute(task.id)
    return jsonify(msg='ok', taskId=str(task.id))


@bp.route('/user/export', methods=['GET'])
@login_required
def export_users():
    form = SearchForm(request.args)
    if not form.validate():
        return form.errors, 400

    from models.task import Task

    task = Task()
    task.name = '导出用户数据'
    task.status = Task.STATUS_PENDING
    task.params = {
        'searchKey': form.searchKey.data,
        'department': form.department.data,
        'position': form.position.data,
        'orderBy': form.orderBy.data
    }
    task.create_user = current_user.id
    task.save()

    from .executor.export_user import execute
    execute(task.id)
    return jsonify(msg='ok', taskId=str(task.id))


# 管理员批量重置密码
@bp.route('/users/passwords', methods=['PUT'])
@admin_required
def reset_passwords():
    form = ObjectIdListForm(request.form)
    users = User.objects(id__in=form.ids.data, author_editable=True)
    for user in users:
        user.password = 'Abc123__'
        user.save()
    return jsonify(ok=True, msg='success')


# 管理员批量提权
@bp.route('/users/permission', methods=['PUT'])
@admin_required
def set_admin():
    form = ObjectIdListForm(request.form)
    ids = form.ids.data
    User.objects(id__in=ids, author_editable=True).update(author_type=1)
    return jsonify(ok=True, msg='success')


# 管理员批量降权
@bp.route('/users/permission', methods=['DELETE'])
@admin_required
def unset_admin():
    form = ObjectIdListForm(request.args)
    ids = form.ids.data
    User.objects(id__in=ids, author_editable=True).update(author_type=0)

    return jsonify(ok=True, msg='success')


# 获取已删除用户信息
@bp.route('/users/recycles', methods=['GET'])
@admin_required
@pagination_marshal_with(user_fields)
def get_users_recycles():
    form = SimpleSearchForm(request.args)
    query = User.objects(is_deleted=True)
    search_key = form.searchKey.data
    if search_key:
        query = query.filter(Q(username__contains=search_key) | Q(email__contains=search_key))
    return build_order_by(query, form.orderBy.data), 200


# 彻底删除
@bp.route('/users/recycles', methods=['DELETE'])
@admin_required
@base_delete_recycles(User)
def delete_users_recycles():
    pass


# 撤销删除
@bp.route('/users/recycles', methods=['PUT'])
@admin_required
@base_recover_recycles(User)
def recover_users_recycles(ids):
    User.objects(id__in=ids).update(is_deleted=False)

    return jsonify(ok=True, msg='success')
