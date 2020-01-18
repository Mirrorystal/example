from flask import Blueprint
from flask_login import login_required
from flask_restful import fields
from models.user import User
from models.cable import Cable
from models.device import Device
from models.interface import Interface
from models.equipment import Equipment
from auth.permissions import admin_or_owner_required, admin_required
from .forms.cable import CreateOrUpdateForm, SearchForm
from .helper.base_views import *
from .helper.pagination import pagination_marshal_with, build_order_by
from .helper.response_fields import cable_base_fields, equipment_base_fields, interface_base_fields, \
    device_base_fields, cable_template_fields

bp = Blueprint('cable', __name__, url_prefix='/appliance')

cable_list_fields = {
    **cable_base_fields,
    # 'startEquipmentName': fields.String(attribute='start_equipment.name'),
    # 'endEquipmentName': fields.String(attribute='end_equipment.name'),
    # 'startDeviceName': fields.String(attribute='start_device.name'),
    # 'endDeviceName': fields.String(attribute='end_device.name'),
    'startInterfaceName': fields.String(attribute='start_interface.name'),
    'endInterfaceName': fields.String(attribute='end_interface.name')

}

cable_fields = {
    **cable_base_fields,
    'startEquipment': fields.Nested(equipment_base_fields, attribute='start_equipment'),
    'endEquipment': fields.Nested(equipment_base_fields, attribute='end_equipment'),
    'startDevice': fields.Nested(device_base_fields, attribute='start_device'),
    'endDevice': fields.Nested(device_base_fields, attribute='end_device'),
    'startInterface': fields.Nested(interface_base_fields, attribute='start_interface'),
    'endInterface': fields.Nested(interface_base_fields, attribute='end_interface'),
}


@bp.route('/cable/<oid:oid>', methods=['GET'])
@login_required
@base_view(Cable, cable_fields)
def get_cable():
    pass


@bp.route('/cable', methods=['POST'])
@login_required
@base_create(Cable, CreateOrUpdateForm)
def create_cable():
    pass


@bp.route('/cable/<oid:oid>', methods=['PUT'])
@admin_or_owner_required(Cable)
@base_update(Cable, CreateOrUpdateForm)
def update_cable(new, old, response):
    return response


@bp.route('/cable/<oid:oid>', methods=['DELETE'])
@admin_or_owner_required(Cable)
@base_delete(Cable)
def delete_cable():
    pass


@bp.route('/cables', methods=['DELETE'])
@admin_required
@base_delete_many(Cable)
def delete_cables():
    pass


@bp.route('/cables/meta', methods=['GET'])
@login_required
def get_users_meta():
    data = Cable.objects(is_deleted=False).fields(id=1, name=1, _start_interface=1, _end_interface=1).all()
    meta = [{
        'id': str(item.id),
        'name': item.name,
        'startInterface': str(item._start_interface.id) if item._start_interface else None,
        'endInterface': str(item._end_interface.id) if item._end_interface else None,
    } for item in data]
    return jsonify(ok=True, data=meta)


@bp.route('/cables', methods=['GET'])
@login_required
@pagination_marshal_with(cable_list_fields)
def search_cable():
    form = SearchForm(request.args)
    query = Cable.objects(is_deleted=False, is_template=False)

    # 简单搜索
    if form.searchKey.data:
        search_key = form.searchKey.data
        query = query.filter(Q(name__contains=search_key) | Q(note__contains=search_key))
        return build_order_by(query, form.orderBy.data), 200

    # 高级搜索
    if form.name.data:
        query = query.filter(name__contains=form.name.data)
    if form.note.data:
        query = query.filter(note__contains=form.note.data)
    if form.signalType.data:
        query = query.filter(signal_type=form.signalType.data)
    if form.shieldType.data:
        query = query.filter(shield_type=form.shieldType.data)
    if form.isCustom.data:
        query = query.filter(is_custom=True)
    if form.startEquipmentId.data:
        query = query.filter(_start_equipment=form.startEquipmentId.data)
    if form.endEquipmentId.data:
        query = query.filter(_end_equipment=form.endEquipmentId.data)
    if form.startDeviceId.data:
        query = query.filter(_start_device=form.startDeviceId.data)
    if form.endDeviceId.data:
        query = query.filter(_end_device=form.endDeviceId.data)
    if form.startInterfaceId.data:
        query = query.filter(_start_interface=form.startInterfaceId.data)
    if form.endInterfaceId.data:
        query = query.filter(_end_interface=form.endInterfaceId.data)
    if form.createUserId.data:
        query = query.filter(_create_user=form.createUserId.data)
    if form.createdAtStart.data:
        query = query.filter(created_at__gte=form.createdAt.data)
    if form.createdAtEnd.data:
        query = query.filter(created_at__lt=form.createdAtEnd.data)
    current_user.update(inc__search_num=1)
    return build_order_by(query, form.orderBy.data)


# 复刻模板
@bp.route('/cable/templates', methods=['POST'])
@login_required
@base_copy_templates(Cable)
def create_cable_template():
    pass


# 审核模板
@bp.route('/cable/templates', methods=['PUT'])
@admin_required
@base_verify_templates(Cable)
def verify_cable_template():
    pass


# 获取模板
@bp.route('/cable/templates', methods=['GET'])
@login_required
@pagination_marshal_with(cable_template_fields)
@base_get_templates(Cable)
def get_cable_templates():
    pass


# 移除模板
@bp.route('/cable/templates', methods=['DELETE'])
@admin_required
@base_delete_many(Cable)
def delete_cable_templates():
    pass


# 更新模板
@bp.route('/cable/template/<oid:oid>', methods=['PUT'])
@admin_or_owner_required(Cable)
@base_update_templates(Cable, CreateOrUpdateForm)
def update_cable_template(new, old, response):
    return response


# 获取已删除
@bp.route('/cables/recycles', methods=['GET'])
@login_required
@pagination_marshal_with(cable_base_fields)
@base_get_recycles(Cable)
def get_cables_recycles():
    pass


# 彻底删除
@bp.route('/cables/recycles', methods=['DELETE'])
@login_required
@base_delete_recycles(Cable)
def delete_cables_recycles():
    pass


# 撤销删除
@bp.route('/cables/recycles', methods=['PUT'])
@login_required
@base_recover_recycles(Cable)
def recover_cables_recycles(ids):
    cables = Cable.objects(Q(id__in=ids) & Q(is_template=False))
    cables.update(is_deleted=False)  # 恢复线缆自身

    interfaces = [interface.id for interface in cables.values_list('_start_interface', '_end_interface')[0]]
    devices = [device.id for device in cables.values_list('_start_device', '_end_interface')[0]]
    equipments = [equipment.id for equipment in cables.values_list('_start_equipment', '_end_interface')[0]]

    Interface.objects(id__in=interfaces).update(is_deleted=False)
    Device.objects(id__in=devices).update(is_deleted=False)
    Equipment.objects(id__in=equipments).update(is_deleted=False)

    return jsonify(ok=True, msg='success')


# 撤销删除模板
@bp.route('/cables/templates/recycles', methods=['PUT'])
@login_required
@base_recover_recycles(Cable)
def recover_cables__templates_recycles(ids):
    Cable.objects(Q(id__in=ids) & Q(is_template=True)).update(is_deleted=False)
    return jsonify(ok=True, msg='success')


# 获取已删除模板
@bp.route('/cables/templates/recycles', methods=['GET'])
@login_required
@pagination_marshal_with(cable_template_fields)
@get_templates_recycles(Cable)
def get_cables_templates_recycles():
    pass