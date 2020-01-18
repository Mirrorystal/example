from flask import Blueprint
from flask_login import login_required
from flask_restful import fields
from models.user import User
from models.cable import Cable
from models.device import Device
from models.interface import Interface
from models.equipment import Equipment
from auth.permissions import admin_or_owner_required, admin_required
from .forms.interface import CreateOrUpdateForm, SearchForm
from .helper.base_views import *
from .helper.pagination import pagination_marshal_with, build_order_by
from .helper.response_fields import interface_base_fields, device_base_fields, equipment_base_fields, \
    interface_template_fields

bp = Blueprint('interface', __name__, url_prefix='/appliance')

interface_fields = {
    **interface_base_fields,
    'parentDevice': fields.Nested(device_base_fields, attribute='parent_device'),
    'parentEquipment': fields.Nested(equipment_base_fields, attribute='parent_equipment'),
}

interface_list_fields = {
    **interface_base_fields,
    'parentDeviceName': fields.String(attribute='parent_device.name'),
    'parentEquipmentName': fields.String(attribute='parent_equipment.name'),
}


# 通过id获取接口
@bp.route('/interface/<oid:oid>', methods=['GET'])
@login_required
@base_view(Interface, interface_fields)
def get_interface():
    pass


# 创建接口
@bp.route('/interface', methods=['POST'])
@login_required
@base_create(Interface, CreateOrUpdateForm)
def create_interface():
    pass


# 更新
@bp.route('/interface/<oid:oid>', methods=['PUT'])
@admin_or_owner_required(Interface)
@base_update(Interface, CreateOrUpdateForm)
def update_interface(new, old, response):
    if new.parent_device.id != old.parent_device.id:
        Cable.objects(_start_interface=new).update(_start_device=new.parent_device)
        Cable.objects(_end_interface=new).update(_end_device=new.parent_device)
    return response


# 删除
@bp.route('/interface/<oid:oid>', methods=['DELETE'])
@admin_or_owner_required(Interface)
@base_delete(Interface)
def delete_interface(oid, response):
    Cable.objects(Q(_start_interface=oid) | Q(_end_interface=oid)).update(is_deleted=True)
    return response


@bp.route('/interface/child/<oid:oid>', methods=['GET'])
@login_required
def get_child(oid):
    interface = Interface.objects(id=oid).count()
    if not interface:
        return jsonify(ok=True, msg='not found'), 404
    child_cable = Cable.objects(Q(_start_interface=oid) | Q(_end_interface=oid)).count()
    return jsonify(ok=True, msg={'cable': child_cable})


# 批量删除
@bp.route('/interfaces', methods=['DELETE'])
@admin_required
@base_delete_many(Interface)
def delete_interfaces():
    pass


@bp.route('/interfaces/child', methods=['GET'])
@login_required
def get_interfaces_child():
    form = ObjectIdListForm(request.args)
    ids = form.ids.data
    interface = Interface.objects(id__in=ids).count()
    if not interface:
        return jsonify(ok=True, msg='not found'), 404
    child_cable = Cable.objects(Q(_start_interface__in=ids) | Q(_end_interface__in=ids)).count()
    return jsonify(ok=True, msg={'cable': child_cable})


@bp.route('/interfaces/meta', methods=['GET'])
@login_required
def get_users_meta():
    data = Interface.objects(is_deleted=False, is_template=False).fields(id=1, name=1, _parent_device=1).all()
    meta = [{
        'id': str(item.id),
        'name': item.name,
        'parentDeviceId': str(item._parent_device.id) if item._parent_device else None,
    } for item in data]
    return jsonify(ok=True, data=meta)


# 搜索
@bp.route('/interfaces', methods=['GET'])
@login_required
@pagination_marshal_with(interface_list_fields)
def get_interfaces():
    form = SearchForm(request.args)
    query = Interface.objects(is_deleted=False, is_template=False)

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
    if form.location.data:
        query = query.filter(location=form.location.data)
    if form.type.data:
        query = query.filter(type=form.type.data)
    if form.protocol.data:
        query = query.filter(protocol=form.protocol.data)
    if form.createUserId.data:
        query = query.filter(_create_user=form.createUserId.data)
    if form.parentEquipmentId.data:
        query = query.filter(_parent_equipment=form.parentEquipmentId.data)
    if form.parentDeviceId.data:
        query = query.filter(_parent_device=form.parentDeviceId.data)
    if form.createdAtStart.data:
        query = query.filter(created_at__gte=form.createdAtStart.data)
    if form.createdAtEnd.data:
        query = query.filter(created_at__lt=form.createdAtEnd.data)

    current_user.update(inc__search_num=1)
    return build_order_by(query, form.orderBy.data), 200


# 复刻模板
@bp.route('/interface/templates', methods=['POST'])
@login_required
@base_copy_templates(Interface)
def create_interface_template():
    pass


# 审核模板
@bp.route('/interface/templates', methods=['PUT'])
@admin_required
@base_verify_templates(Interface)
def verify_interface_template():
    pass


# 获取模板
@bp.route('/interface/templates', methods=['GET'])
@login_required
@pagination_marshal_with(interface_template_fields)
@base_get_templates(Interface)
def get_interface_templates():
    pass


# 移除模板
@bp.route('/interface/templates', methods=['DELETE'])
@admin_required
@base_delete_many(Interface)
def delete_interface_templates():
    pass

# 更新模板
@bp.route('/interface/template/<oid:oid>', methods=['PUT'])
@admin_or_owner_required(Interface)
@base_update_templates(Interface, CreateOrUpdateForm)
def update_interface_template(new, old, response):
    return response


# 获取已删除
@bp.route('/interfaces/recycles', methods=['GET'])
@login_required
@pagination_marshal_with(interface_base_fields)
@base_get_recycles(Interface)
def get_interfaces_recycles():
    pass


# 彻底删除
@bp.route('/interfaces/recycles', methods=['DELETE'])
@login_required
@base_delete_recycles(Interface)
def delete_interfaces_recycles():
    pass


# 撤销删除
@bp.route('/interfaces/recycles', methods=['PUT'])
@login_required
@base_recover_recycles(Interface)
def recover_interfaces_recycles(ids):
    interfaces = Interface.objects(Q(id__in=ids) & Q(is_template=False))
    interfaces.update(is_deleted=False)  # 恢复接口自身

    devices = [device.id for device in interfaces.values_list('_parent_device')]
    equipments = [equipment.id for equipment in interfaces.values_list('_parent_equipment')]

    Device.objects(id__in=devices).update(is_deleted=False)
    Equipment.objects(id__in=equipments).update(is_deleted=False)
    return jsonify(ok=True, msg='success')


# 撤销删除模板
@bp.route('/interfaces/templates/recycles', methods=['PUT'])
@login_required
@base_recover_recycles(Interface)
def recover_interfaces__templates_recycles(ids):
    Interface.objects(Q(id__in=ids) & Q(is_template=True)).update(is_deleted=False)
    return jsonify(ok=True, msg='success')


# 获取已删除模板
@bp.route('/interfaces/templates/recycles', methods=['GET'])
@login_required
@pagination_marshal_with(interface_template_fields)
@get_templates_recycles(Interface)
def get_interfaces_templates_recycles():
    pass
