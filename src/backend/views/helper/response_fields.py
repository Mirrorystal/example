from flask_restful import fields


base_fields = {
    'id': fields.String,
    'name': fields.String,
    'note': fields.String,
}


appliance_fields = {
    **base_fields,
    'type': fields.String,
    'location': fields.String,
}

operation_fields = {
    'createdAt': fields.DateTime(attribute='created_at', dt_format='iso8601'),
    'updatedAt': fields.DateTime(attribute='updated_at', dt_format='iso8601'),
    'createUserName': fields.String(attribute='create_user.username'),
    'updateUserName': fields.String(attribute='update_user.username'),
    'updateNum': fields.Integer(attribute='update_num')
}

equipment_base_fields = {
    **appliance_fields,
    'sn': fields.String,
    'manufacturer': fields.String,
    **operation_fields
}
equipment_template_fields = {
    **equipment_base_fields,
    'verifyUserName': fields.String(attribute='verify_user.username')
}

device_base_fields = {
    **appliance_fields,
    'sn': fields.String,
    'manufacturer': fields.String,
    'system': fields.String,
    **operation_fields
}

device_template_fields = {
    **device_base_fields,
    'parentEquipmentName': fields.String(attribute='parent_equipment.name'),
    'verifyUserName': fields.String(attribute='verify_user.username')
}

interface_base_fields = {
    **appliance_fields,
    'protocol': fields.String,
    'pcl': fields.String,
    **operation_fields
}

interface_template_fields = {
    **interface_base_fields,
    'parentDeviceName': fields.String(attribute='parent_device.name'),
    'parentEquipmentName': fields.String(attribute='parent_equipment.name'),
    'verifyUserName': fields.String(attribute='verify_user.username')
}

cable_base_fields = {
    **base_fields,
    'signalType': fields.String(attribute='signal_type'),
    'shieldType': fields.String(attribute='shield_type'),
    'isCustom': fields.Boolean(attribute='is_custom'),
    'parameterList': fields.String(attribute='parameter_list'),
    **operation_fields
}

cable_template_fields = {
    **cable_base_fields,
    # 'startEquipmentName': fields.String(attribute='start_equipment.name'),
    # 'endEquipmentName': fields.String(attribute='end_equipment.name'),
    # 'startDeviceName': fields.String(attribute='start_device.name'),
    # 'endDeviceName': fields.String(attribute='end_device.name'),
    'startInterfaceName': fields.String(attribute='start_interface.name'),
    'endInterfaceName': fields.String(attribute='end_interface.name'),
    'verifyUserName': fields.String(attribute='verify_user.username')
}