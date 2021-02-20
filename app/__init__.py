from flask import Flask

from flask_bootstrap import Bootstrap

# flask mail 扩展
from flask_mail import Mail

# 在浏览器中渲染日期和时间
from flask_moment import Moment

# 关系型数据库框架
from flask_sqlalchemy import SQLAlchemy

from app.config import config
from app import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    db.create_all()

    # 添加路由和自定义的错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)  # 注册主蓝本

    return app

