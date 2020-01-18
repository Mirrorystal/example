from flask import Blueprint
from flask_login import login_required
from models.user import User
from models.equipment import Equipment
from models.device import Device
from models.interface import Interface
from models.cable import Cable
from auth.permissions import admin_or_owner_required, admin_required
from .forms.equipment import CreateOrUpdateForm, SearchForm
from .helper.response_fields import equipment_base_fields, equipment_template_fields
from .helper.base_views import *
from .helper.pagination import pagination_marshal_with, build_order_by

bp = Blueprint('equipment', __name__, url_prefix='/appliance')

# 通过id获取
@bp.route('/equipment/<oid:oid>', methods=['GET'])
@login_required
@base_view(Equipment, equipment_base_fields)
def get_equipment():
    pass


@bp.route('/equipment', methods=['POST'])
@login_required
@base_create(Equipment, CreateOrUpdateForm)
def create_equipment():
    pass


@bp.route('/equipment/<oid:oid>', methods=['PUT'])
@admin_or_owner_required(Equipment)
@base_update(Equipment, CreateOrUpdateForm)
def update_equipment(new, old, response):
    return response


@bp.route('/equipment/<oid:oid>', methods=['DELETE'])
@admin_or_owner_required(Equipment)
@base_delete(Equipment)
def delete_equipment(oid, response):
    Device.objects(_parent_equipment=oid).update(is_deleted=True)
    Interface.objects(_parent_equipment=oid).update(is_deleted=True)
    Cable.objects(Q(_start_equipment=oid) | Q(_end_equipment=oid)).update(is_deleted=True)
    return response


@bp.route('/equipment/child/<oid:oid>', methods=['GET'])
@login_required
def get_child(oid):
    equipment = Equipment.objects(id=oid).count()
    if not equipment:
        return jsonify(ok=True, msg='not found'), 404
    child_device = Device.objects(_parent_equipment=oid).count()
    child_interface = Interface.objects(_parent_equipment=oid).count()
    child_cable = Cable.objects(Q(_start_equipment=oid) | Q(_end_equipment=oid)).count()
    return jsonify(ok=True, msg={'device': child_device, 'interface': child_interface,
                                 'cable': child_cable})


@bp.route('/equipments', methods=['DELETE'])
@admin_required
@base_delete_many(Equipment)
def delete_equipments():
    pass


@bp.route('/equipments/child', methods=['GET'])
@login_required
def get_equipments_child():
    form = ObjectIdListForm(request.args)
    ids = form.ids.data
    equipment = Equipment.objects(id__in=ids).count()
    if not equipment:
        return jsonify(ok=True, msg='not found'), 404
    child_device = Device.objects(_parent_equipment__in=ids).count()
    child_interface = Interface.objects(_parent_equipment__in=ids).count()
    child_cable = Cable.objects(Q(_start_equipment__in=ids) | Q(_end_equipment__in=ids)).count()
    return jsonify(ok=True, msg={'device': child_device, 'interface': child_interface,
                                 'cable': child_cable})


@bp.route('/equipments/meta', methods=['GET'])
@login_required
def get_users_meta():
    data = Equipment.objects(is_deleted=False, is_template=False).fields(id=1, name=1).all()
    meta = [{
        'id': str(item.id),
        'name': item.name,
    } for item in data]
    return jsonify(ok=True, data=meta)


@bp.route('/equipments', methods=['GET'])
@login_required
@pagination_marshal_with(equipment_base_fields)
def get_equipments():
    form = SearchForm(request.args)
    query = Equipment.objects(is_deleted=False, is_template=False)

    # 简单搜索
    if form.searchKey.data:
        search_key = form.searchKey.data
        query = query.filter(Q(name__contains=search_key) | Q(note__contains=search_key))
        return build_order_by(query, form.orderBy.data), 200

    # 高级搜索
    if form.name.data:
        query = query.filter(name__contains=form.name.data)
    if form.type.data:
        query = query.filter(type=form.type.data)
    if form.location.data:
        query = query.filter(location=form.location.data)
    if form.sn.data:
        query = query.filter(sn=form.sn.data)
    if form.manufacturer.data:
        query = query.filter(manufacturer=form.manufacturer.data)
    if form.note.data:
        query = query.filter(note__contains=form.note.data)
    if form.createUserId.data:
        query = query.filter(_create_user=form.createUserId.data)
    if form.createdAtStart.data:
        query = query.filter(created_at__gte=form.createdAtStart.data)
    if form.createdAtEnd.data:
        query = query.filter(created_at__lte=form.createdAtEnd.data)

    current_user.update(inc__search_num=1)
    return build_order_by(query, form.orderBy.data)


# 复刻模板
@bp.route('/equipment/templates', methods=['POST'])
@login_required
@base_copy_templates(Equipment)
def create_equipment_template():
    pass


# 审核模板
@bp.route('/equipment/templates', methods=['PUT'])
@admin_required
@base_verify_templates(Equipment)
def verify_equipment_template():
    pass


# 获取模板
@bp.route('/equipment/templates', methods=['GET'])
@login_required
@pagination_marshal_with(equipment_template_fields)
@base_get_templates(Equipment)
def get_equipment_templates():
    pass


# 移除模板
@bp.route('/equipment/templates', methods=['DELETE'])
@admin_required
@base_delete_many(Equipment)
def delete_equipment_templates():
    pass


# 更新模板
@bp.route('/equipment/template/<oid:oid>', methods=['PUT'])
@admin_or_owner_required(Equipment)
@base_update_templates(Equipment, CreateOrUpdateForm)
def update_equipment_template(new, old, response):
    return response


# 获取已删除
@bp.route('/equipments/recycles', methods=['GET'])
@login_required
@pagination_marshal_with(equipment_base_fields)
@base_get_recycles(Equipment)
def get_equipments_recycles():
    pass


# 彻底删除
@bp.route('/equipments/recycles', methods=['DELETE'])
@login_required
@base_delete_recycles(Equipment)
def delete_equipments_recycles():
    pass


# 撤销删除
@bp.route('/equipments/recycles', methods=['PUT'])
@login_required
@base_recover_recycles(Equipment)
def recover_equipments_recycles(ids):
    Equipment.objects(id__in=ids).update(is_deleted=False)
    return jsonify(ok=True, msg='success')


# 获取已删除模板
@bp.route('/equipments/templates/recycles', methods=['GET'])
@login_required
@pagination_marshal_with(equipment_template_fields)
@get_templates_recycles(Equipment)
def get_equipments_templates_recycles():
    pass
