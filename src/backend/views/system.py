from flask import Blueprint, jsonify, request
from flask_restful import fields, marshal_with
from flask_login import login_required, current_user
from .forms.system import UpdateSettingForm
from auth.permissions import admin_required
from models.setting import Setting
from models.user import User
from models.interface import Interface
from models.cable import Cable

bp = Blueprint('system', __name__, url_prefix='/system')

setting_fields = {
    'departments': fields.List(fields.String()),
    'positions': fields.List(fields.String()),
    'shieldTypes': fields.List(fields.String(), attribute='shield_types'),
    'spliceTypes': fields.List(fields.String(), attribute='splice_types'),
    'interfaceProtocol': fields.List(fields.String(), attribute='interface_protocol'),
}


@bp.route('/settings', methods=['GET'])
@login_required
@marshal_with(setting_fields)
def get_settings():
    setting = Setting.objects().first()
    if setting is None:
        setting = Setting()
        setting.update_user = current_user.id
        setting.save()
    return setting


@bp.route('/settings', methods=['PUT'])
@admin_required
def update_settings():
    form = UpdateSettingForm(request.form)
    if not form.validate():
        return form.errors, 400
    setting = Setting.objects().first()
    if setting is None:
        return jsonify(ok=False, msg="system setting is uninitialized")

    attribute = ["departments", "positions", "shield_types", "splice_types", "interface_protocol"]
    index = form.nameString.index(form.name.data)
    if form.value.data in setting.__getattribute__(attribute[index]):
        return form.errors
    setting.__getattribute__(attribute[index]).append(form.value.data)
    setting.update_user = current_user.id

    setting.save()
    return jsonify(ok=True, msg="success")


@bp.route('/settings', methods=['DELETE'])
@admin_required
def delete_settings():
    form = UpdateSettingForm(request.args)
    if not form.validate():
        return form.errors, 400
    setting = Setting.objects().first()
    if setting is None:
        return jsonify(ok=False, msg="system setting is uninitialized")

    attribute = ["departments", "positions", "shield_types", "splice_types", "interface_protocol"]
    index = form.nameString.index(form.name.data)

    if form.value.data in setting.__getattribute__(attribute[index]):
        field = ["department", "position", "shield_type", "type", "protocol"]
        documents = [User, User, Cable, Interface, Interface]

        count = len(documents[index].objects(**{field[index]: form.value.data}))
        if count:
            return jsonify(ok=False, msg=count)
        setting.__getattribute__(attribute[index]).remove(form.value.data)
        setting.update_user = current_user.id
        setting.save()
        return jsonify(ok=True, msg="success")
    return jsonify(ok=False, msg="not found"), 404
