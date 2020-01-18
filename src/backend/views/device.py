from flask import Blueprint
from flask_login import login_required
from flask_restful import fields
from models.user import User
from models.cable import Cable
from models.device import Device
from models.interface import Interface
from models.equipment import Equipment
from auth.permissions import admin_or_owner_required, admin_required
from .forms.device import CreateOrUpdateForm, SearchForm
from .helper.base_views import *
from .helper.pagination import pagination_marshal_with, build_order_by
from .helper.response_fields import device_base_fields, equipment_base_fields, device_template_fields

bp = Blueprint('device', __name__, url_prefix='/appliance')

device_list_fields = {
    **device_base_fields,
    'parentEquipmentName': fields.String(attribute='parent_equipment.name'),
}

device_fields = {
    **device_base_fields,
    'parentEquipment': fields.Nested(equipment_base_fields, attribute='parent_equipment'),
}


@bp.route('/device/<oid:oid>', methods=['GET'])
@login_required
@base_view(Device, device_fields)
def get_device():
    pass


@bp.route('/device', methods=['POST'])
@login_required
@base_create(Device, CreateOrUpdateForm)
def create_device():
    pass


@bp.route('/device/<oid:oid>', methods=['PUT'])
@admin_or_owner_required(Device)
@base_update(Device, CreateOrUpdateForm)
def update_device(new, old, response):
    if new.parent_equipment.id != old.parent_equipment.id:
        Interface.objects(_parent_device=new).update(_parent_equipment=new.parent_equipment)
        Cable.objects(_start_device=new).update(_start_equipment=new.parent_equipment)
        Cable.objects(_end_device=new).update(_end_equipment=new.parent_equipment)
    return response


@bp.route('/device/<oid:oid>', methods=['DELETE'])
@admin_or_owner_required(Device)
@base_delete(Device)
def delete_device(oid, response):
    Interface.objects(_parent_device=oid).update(is_deleted=True)
    Cable.objects(Q(_start_device=oid) | Q(_end_device=oid)).update(is_deleted=True)

    return response


@bp.route('/device/child/<oid:oid>', methods=['GET'])
@login_required
def get_child(oid):
    device = Device.objects(id=oid).count()
    if not device:
        return jsonify(ok=True, msg='not found'), 404
    child_interface = Interface.objects(_parent_device=oid).count()
    child_cable = Cable.objects(Q(_start_device=oid) | Q(_end_device=oid)).count()
    return jsonify(ok=True, msg={'interface': child_interface, 'cable': child_cable})


@bp.route('/devices', methods=['DELETE'])
@admin_required
@base_delete_many(Device)
def delete_devices():
    pass


@bp.route('/devices/child', methods=['GET'])
@login_required
def get_devices_child():
    form = ObjectIdListForm(request.args)
    ids = form.ids.data
    device = Device.objects(id__in=ids).count()
    if not device:
        return jsonify(ok=True, msg='not found'), 404
    child_interface = Interface.objects(_parent_device__in=ids).count()
    child_cable = Cable.objects(Q(_start_device__in=ids) | Q(_end_device__in=ids)).count()
    return jsonify(ok=True, msg={'interface': child_interface, 'cable': child_cable})


@bp.route('/devices/meta', methods=['GET'])
@login_required
def get_users_meta():
    data = Device.objects(is_deleted=False, is_template=False).fields(id=1, name=1, _parent_equipment=1).all()
    meta = [{
        'id': str(item.id),
        'name': item.name,
        'parentEquipmentId': str(item._parent_equipment.id) if item._parent_equipment else None
    } for item in data]
    return jsonify(ok=True, data=meta)


# 查询
@bp.route('/devices', methods=['GET'])
@login_required
@pagination_marshal_with(device_list_fields)
def get_devices():
    form = SearchForm(request.args)
    query = Device.objects(is_deleted=False, is_template=False)

    if form.searchKey.data:
        search_key = form.searchKey.data
        query = query.filter(Q(name__contains=search_key) | Q(note__contains=search_key))
        return build_order_by(query, form.orderBy.data), 200

    if form.name.data:
        query = query.filter(name__contains=form.name.data)
    if form.note.data:
        query = query.filter(note__contains=form.note.data)
    if form.type.data:
        query = query.filter(type=form.type.data)
    if form.location.data:
        query = query.filter(location=form.location.data)
    if form.sn.data:
        query = query.filter(sn=form.sn.data)
    if form.manufacturer.data:
        query = query.filter(manufacturer=form.manufacturer.data)
    if form.system.data:
        query = query.filter(system=form.system.data)
    if form.createUserId.data:
        query = query.filter(_create_user=form.createUserId.data)
    if form.parentEquipmentId.data:
        query = query.filter(_parent_equipment=form.parentEquipmentId.data)
    if form.createdAtStart.data:
        query = query.filter(created_at__gte=form.createdAt.data)
    if form.createdAtEnd.data:
        query = query.filter(created_at__lte=form.createdAtEnd.data)

    current_user.update(inc__search_num=1)
    return build_order_by(query, form.orderBy.data)

# 复刻模板
@bp.route('/device/templates', methods=['POST'])
@login_required
@base_copy_templates(Device)
def create_device_template():
    pass


# 审核模板
@bp.route('/device/templates', methods=['PUT'])
@admin_required
@base_verify_templates(Device)
def verify_equipment_template():
    pass


# 获取模板
@bp.route('/device/templates', methods=['GET'])
@login_required
@pagination_marshal_with(device_template_fields)
@base_get_templates(Device)
def get_device_templates():
    pass


# 移除模板
@bp.route('/device/templates', methods=['DELETE'])
@admin_required
@base_delete_many(Device)
def delete_device_templates():
    pass


# 更新模板
@bp.route('/device/template/<oid:oid>', methods=['PUT'])
@admin_or_owner_required(Device)
@base_update_templates(Device, CreateOrUpdateForm)
def update_device_template(new, old, response):
    return response


# 获取已删除
@bp.route('/devices/recycles', methods=['GET'])
@login_required
@pagination_marshal_with(device_base_fields)
@base_get_recycles(Device)
def get_devices_recycles():
    pass


# 彻底删除
@bp.route('/devices/recycles', methods=['DELETE'])
@login_required
@base_delete_recycles(Device)
def delete_devices_recycles():
    pass


# 撤销删除设备
@bp.route('/devices/recycles', methods=['PUT'])
@login_required
@base_recover_recycles(Device)
def recover_devices_recycles(ids):
    devices = Device.objects(Q(id__in=ids) & Q(is_template=False))
    devices.update(is_deleted=False)

    equipments = [equipment.id for equipment in devices.values_list('_parent_equipment')]
    Equipment.objects(id__in=equipments).update(is_deleted=False)

    return jsonify(ok=True, msg='success')


# 撤销删除模板
@bp.route('/devices/templates/recycles', methods=['PUT'])
@login_required
@base_recover_recycles(Device)
def recover_devices_templates_recycles(ids):
    Device.objects(Q(id__in=ids) & Q(is_template=True)).update(is_deleted=False)
    return jsonify(ok=True, msg='success')


# 获取已删除模板
@bp.route('/devices/templates/recycles', methods=['GET'])
@login_required
@pagination_marshal_with(device_template_fields)
@get_templates_recycles(Device)
def get_devices_templates_recycles():
    pass
