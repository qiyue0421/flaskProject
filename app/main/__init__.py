# 创建蓝本，在蓝本中定义的路由和错误处理程序处于休眠状态，直到蓝本注册到应用上之后，它们才真正成为应用的一部分
from flask import Blueprint

main = Blueprint('main', __name__)  # 第一个参数为蓝本所在的包或模块，第二个参数为蓝本名称，一般为__name__变量即可

from . import views, errors  # 在末尾导入——避免循环导入依赖，因为在views.py和errors.py脚本中还要导入main蓝本