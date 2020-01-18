from flask import jsonify
from flask_login import LoginManager, current_user
from datetime import datetime, timedelta
from models.user import User


class Auth(object):
    """加载配置"""
    def __init__(self, manager):
        self.manager = manager
        self.token_type = 'Bearer '
        self.token_expired_time = 60 * 60 * 2  # 两小时
        self.token_rest_refresh_time = 60 * 30  # 半小时

    def init_app(self, app):
        if 'TOKEN_HEADER_TYPE' in app.config:
            self.token_type = app.config['TOKEN_HEADER_TYPE']
        if 'TOKEN_EXPIRED_TIME' in app.config:
            self.token_expired_time = app.config['TOKEN_EXPIRED_TIME']
        if 'TOKEN_REST_REFRESH_TIME' in app.config:
            self.token_rest_refresh_time = app.config['TOKEN_REST_REFRESH_TIME']
        self.manager.init_app(app)


login_manager = LoginManager()
auth = Auth(login_manager)


@login_manager.unauthorized_handler
def unauthorized():
    print(current_user)
    if current_user.is_anonymous:
        return jsonify(msg='请先登录'), 401
    else:
        return jsonify(msg='登录失效，请重新登录'), 401


@login_manager.request_loader
def load_user(request):
    header_val = request.headers.get('Authorization')
    token = header_val.replace(auth.token_type, '', 1) if header_val else request.args.get('accessToken')
    if not token:
        return None
    user = User.objects(__raw__={'token.value': token, 'is_deleted': False}).first()
    """最后半小时内有请求进入、刷新token过期时间"""
    if user is not None and user.is_authenticated and need_refresh_token(user):
        user.refresh_token(auth.token_expired_time)
    return user


def need_refresh_token(user):
    return user.token.expired_at - datetime.now() < timedelta(seconds=auth.token_rest_refresh_time)
