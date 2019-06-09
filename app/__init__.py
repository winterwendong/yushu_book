# -*- coding:utf-8 -*-
from flask import Flask
from app.models.base import db
from app.libs.email import mail
from app.libs.limiter import Limiter

__author__ = 'wendong'

from flask_login import LoginManager
from app.libs.email import mail
from flask_cache import Cache
from app.libs.limiter import Limiter


login_manager = LoginManager()
cache = Cache(config={'CACHE_TYPE': 'simple'})
limiter = Limiter()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_web_blueprint(app)

    # 注册SQLAlchemy
    db.init_app(app)


    # 注册email模块
    mail.init_app(app)

    # 注册login模块
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    # 注册flask-cache模块
    # cache.init_app(app)

    with app.app_context():
        db.create_all()

    return app

def register_web_blueprint(app):
    from app.web import web
    app.register_blueprint(web)

