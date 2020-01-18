from . import executor
from tempfile import mktemp
from openpyxl import Workbook
from models.task import Task, TaskFile
from models.user import User
from mongoengine.queryset.visitor import Q
from views.task import task_status_storage


def execute(task_id):
    return executor.submit(export_users, task_id)


def export_users(task_id):
    task = Task.objects(id=task_id).first()
    if task is None:
        return

    task.status = Task.STATUS_RUNNING
    task.save()
    query = _build_search_query(task.params)

    """缓存当前导入进度，用于前端调用接口获取"""
    storage_key = str(task_id)
    storage = task_status_storage[storage_key] = {
        'success': 0,
        'failed': 0,
        'total': query.count() + 1
    }

    work_book = Workbook()
    sheet = work_book.active

    sheet.append(['姓名', '邮箱', '角色',  '职位', '部门', '电话号码', '装置数量', '设备数量', '接口数量', '线缆数量', '登陆次数', '搜索次数', '创建时间', '最后更新时间'])
    for user in query:
        sheet.append([
            user.username,
            user.email,
            '普通用户' if user.author_type == 0 else '管理员',
            user.position,
            user.department,
            user.phone,
            user.equipment_num,
            user.device_num,
            user.interface_num,
            user.cable_num,
            user.login_num,
            user.search_num,
            user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            user.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        ])
        storage['success'] += 1

    temp_path = mktemp(suffix='.xls')
    work_book.save(temp_path)

    task.status = Task.STATUS_COMPLETED
    task.result = {
        'success': storage['success'],
        'failed': storage['failed'],
        'total': storage['total'] - 1
    }
    task.file = TaskFile()
    task.file.mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    task.file.path = temp_path
    task.file.name = task.name + task.created_at.strftime('%Y%m%d%H%M%S') + '.xlsx'
    task.save()
    task_status_storage.pop(storage_key)


def _build_search_query(condition):
    query = User.objects()
    if condition['searchKey']:
        search_key = condition['searchKey']
        query = query.filter(Q(username__contains=search_key) | Q(email__contains=search_key) | Q(phone=search_key))
    if condition['position']:
        query = query.filter(position=condition['position'])
    if condition['position']:
        query = query.filter(department=condition['position'])
    if len(condition['orderBy']) > 0:
        key, sort = condition['orderBy'].popitem()
        sort = '-' if sort == 'desc' else ''
        return query.order_by(sort + key)
    else:
        return query.order_by('-created_at')
    return query
