from flask import Flask
from flask import request
from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from .config import config_by_name

from ..main.service.mail_service import get_email_by_id
from ..main.util.cache import Cache

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)

    @app.route('/email')
    def get_html():
        return get_email_by_id(request.args.get('id'))

    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app
