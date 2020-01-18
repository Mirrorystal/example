from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from auth import auth
from models import db
import views
from .config import Config
from .converter import ObjectIdConverter


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.url_map.converters['oid'] = ObjectIdConverter
    db.init_app(app)
    auth.init_app(app)
    views.init_app(app)
    metrics = PrometheusMetrics(app)
    metrics.info('backend_info', 'Backend Information', version='1.0.0')

    @app.route('/ping')
    @metrics.do_not_track()
    def ping():
        return 'pong'

    return app
