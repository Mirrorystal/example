import os
from models.task import Task
from datetime import datetime
from tempfile import NamedTemporaryFile
from flask import Blueprint, request, jsonify, current_app, send_file
from flask_login import login_required, current_user
from models.image import Image
from urllib.parse import quote
from .forms.resource import ImageUploadForm

bp = Blueprint('resource', __name__, url_prefix='/resource')


def generate_upload_path(created_at):
    upload_path = current_app.config['UPLOAD_RESOURCE_PATH'] or '/tmp'
    date_path = datetime.strftime(created_at, '%Y/%m')
    return os.path.join(upload_path, date_path)


@bp.route('/image', methods=['POST'])
@login_required
def upload_image():
    form = ImageUploadForm(request.files)
    if not form.validate():
        return form.errors, 400

    image = Image()
    file = form.file.data
    image.name = file.filename
    image.type = file.mimetype
    image.owner = current_user.id

    try:
        image.save()
    except:
        return jsonify(msg='保存图片记录到数据库失败'), 500

    upload_path = generate_upload_path(image.created_at)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    try:
        file.save(os.path.join(upload_path, image.real_name))
    except:
        return jsonify(msg='保存图片记录到磁盘失败'), 500

    return jsonify(id=str(image.id), name=image.name, url=image.url)


@bp.route('/task/<oid:task_id>', methods=['GET'])
@login_required
def download_task_file(task_id):

    task = Task.objects(id=task_id).first()
    if task is None:
        return jsonify(msg='file not found'), 404
    elif task.create_user.id != current_user.id:
        return jsonify(msg='access denial'), 403

    file = task.file
    filename = quote(file.name)
    response = send_file(file.path, mimetype=file.mimetype, as_attachment=True, attachment_filename=filename)
    response.headers['Content-Disposition'] += "; filename*=utf-8''{}".format(filename)
    return response


@bp.route('/task/user-template', methods=['GET'])
def import_user_template():
    from openpyxl import Workbook

    work_book = Workbook()
    sheet = work_book.active
    sheet.append(['姓名', '邮箱', '职位', '部门', '电话号码'])
    temp_file = NamedTemporaryFile()
    work_book.save(temp_file.name)
    return send_file(temp_file,
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True,
                     attachment_filename='import_user_template.xlsx')
