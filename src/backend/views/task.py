import os
from flask_restful import marshal
from flask_restful import fields
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models.task import Task

task_status_storage = {}
bp = Blueprint('task', __name__, url_prefix='/task')


task_fields = {
    'name': fields.String(),
    'status': fields.String(),
    'params': fields.Raw(),
    'result': fields.Raw(),
    'createdAt': fields.DateTime(attribute='created_at', dt_format='iso8601'),
}


@bp.route('/result/<oid:task_id>', methods=['GET'])
@login_required
def get_task_result(task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return jsonify(ok=False, msg='任务不存在'), 404
    if task.create_user.id != current_user.id:
        return jsonify(ok=False, msg='不是任务创建者，拒绝访问'), 403
    result = task_status_storage.get(str(task_id))
    return result if result is not None else task.result


@bp.route('/<oid:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return jsonify(ok=False, msg='任务不存在'), 404
    if task.create_user.id != current_user.id:
        return jsonify(ok=False, msg='不是任务创建者，拒绝访问'), 403
    return marshal(task, task_fields)


@bp.route('/<oid:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return jsonify(ok=True, msg='任务不存在')
    else:
        if task.create_user.id != current_user.id:
            return jsonify(ok=False, msg='不是任务创建者，无法删除任务'), 403
        if task.status == task.STATUS_RUNNING:
            return jsonify(ok=False, msg='任务正在运行，无法删除')
        path = task.file.path
        if path and os.path.exists(path):
            os.remove(path)
        task.delete()
        return jsonify(ok=True, msg='任务删除成功')
