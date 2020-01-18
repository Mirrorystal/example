from wtforms import Form, StringField, validators, BooleanField, DateTimeField
from views.helper.exceptions import FormLoadException
from models.device import Device
from models.interface import Interface
from models.equipment import Equipment
from . import ObjectIdField
from . import JsonField


class CreateOrUpdateForm(Form):
    name = StringField(validators=[validators.Length(max=125), validators.DataRequired()])  # 线缆名称
    signalType = StringField(validators=[validators.Length(max=125), validators.DataRequired()])  # 信号类型
    shieldType = StringField(validators=[validators.Length(max=125), validators.DataRequired()])  # 屏蔽类型
    note = StringField(validators=[validators.Length(max=125), validators.DataRequired()])  # 备注
    isCustom = BooleanField(default=False)  # 是否为定制
    parameterList = StringField(validators=[validators.Length(max=125)])  # 如果是定制线缆,参数表的ID
    startInterfaceId = ObjectIdField(validators=[validators.DataRequired()])  # 起始接口ID
    endInterfaceId = ObjectIdField(validators=[validators.DataRequired()])  # 结束接口ID

    def load(self, cable):
        cable.name = self.name.data
        cable.signal_type = self.signalType.data
        cable.shield_type = self.shieldType.data
        cable.note = self.note.data
        cable.is_custom = self.isCustom.data
        cable.parameter_list = self.parameterList.data

        try:
            start_interface = Interface.objects().get(id=self.startInterfaceId.data)
            start_device = start_interface.parent_device
            start_equipment = start_interface.parent_equipment

        except Interface.DoesNotExist:
            raise FormLoadException('起始接口不存在，id: ' + str(self.startInterfaceId.data))
        except Device.DoesNotExist:
            raise FormLoadException('起始接口所属的设备不存在，接口id: ' + str(self.startInterfaceId.data))
        except Equipment.DoesNotExist:
            raise FormLoadException('起始接口所属设备的装置不存在，接口id: ' + str(self.startInterfaceId.data))
        else:
            cable.start_interface = start_interface.id
            cable.start_device = start_device.id
            cable.start_equipment = start_equipment.id

        try:
            end_interface = Interface.objects().get(id=self.endInterfaceId.data)
            end_device = end_interface.parent_device
            end_equipment = end_interface.parent_equipment

        except Interface.DoesNotExist:
            raise FormLoadException('结束接口不存在，id: ' + str(self.endInterfaceId.data))
        except Device.DoesNotExist:
            raise FormLoadException('结束接口所属的设备不存在，接口id: ' + str(self.endInterfaceId.data))
        except Equipment.DoesNotExist:
            raise FormLoadException('结束接口所属设备的装置不存在，接口id: ' + str(self.endInterfaceId.data))
        else:
            cable.end_interface = end_interface.id
            cable.end_device = end_device.id
            cable.end_equipment = end_equipment.id


class SearchForm(Form):
    searchKey = StringField()
    name = StringField()
    signalType = StringField()
    shieldType = StringField()
    isCustom = BooleanField()
    note = StringField()
    orderBy = JsonField()

    startEquipmentId = ObjectIdField()
    startDeviceId = ObjectIdField()
    startInterfaceId = ObjectIdField()

    endEquipmentId = ObjectIdField()
    endDeviceId = ObjectIdField()
    endInterfaceId = ObjectIdField()

    createUserId = ObjectIdField()
    createdAtStart = DateTimeField()
    createdAtEnd = DateTimeField()
