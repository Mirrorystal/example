from flask import Blueprint, jsonify
from flask_restful import fields

from models.keyword import Keyword

bp = Blueprint('key', __name__, '/key')

key_fields = {
    'keyword': fields.String(attribute='word'),
    'frequency': fields.Integer,
    'user.id': fields.String,
    'create_at': fields.DateTime,
    'update_at': fields.DateTime
}

@bp.route('/total', methods=['GET'])
def get_all_keywords():
    try:
        totalKeyWords = Keyword.objects()
        return totalKeyWords, 200
    except Keyword.DoesNotExist:
        return jsonify(msg='not found'), 404