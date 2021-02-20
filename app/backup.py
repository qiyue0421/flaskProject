from flask import Flask, render_template, session, redirect, url_for

from flask_bootstrap import Bootstrap

# 在浏览器中渲染日期和时间
from flask_moment import Moment
from datetime import datetime

from app.main.form import NameForm

import os
# 关系型数据库框架
from flask_sqlalchemy import SQLAlchemy

# 数据库迁移框架
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# flask mail 扩展
from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))

# 应用实例，Flask类的对象，WSGI负责接收来自客户端的所有请求并转交给这个对象进行处理
app = Flask(__name__)
# Flask-WTF扩展无须在应用层初始化，但是要求应用配置一个密钥——一个由随机字符构成的唯一字符串，通过加密或签名以不同的方式提升应用的安全性，防止跨站请求伪造攻击（CSRF）
app.config['SECRET_KEY'] = 'qiyue0421'

# 数据库URL存放在 SQLALCHEMY_DATABASE_URI 键中
# 注意：sqlite默认建立的对象只能让建立该对象的线程使用，而sqlalchemy是多线程的所以需要指定 check_same_thread=False 来让建立的对象任意线程都可使用，否则就会报错
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../data.sqlite', '?check_same_thread=False')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 降低内存消耗

# 邮件配置
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'  # 邮件主题前缀
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'  # 发件人地址
# set MAIL_USERNAME=<Gmail username>
# set MAIL_PASSWORD=<Gmail password>

# SQLAlchemy类的实例，表示应用使用的数据库
db = SQLAlchemy(app)

# 初始化Flask-Bootstrap，在应用中集成Bootstrap开源框架
bootstrap = Bootstrap(app)

# 初始化Flask-Monment，该扩展可在浏览器中渲染日期和时间
moment = Moment(app)

# 初始化Flask-Migrate
manager = Manager(app)
migrate = Migrate(app, db)

mail = Mail(app)


# 定义数据库模型
class Role(db.Model):
    __tablename__ = 'roles'  # 表名
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 对于一个Role类的实例，其users属性返回与角色相关联的用户组成的列表，第一个参数表明这个关系的另一端是哪个模型
    # backref参数向User模型中添加一个role属性（用于获取对应的Role模型对象），从而定义反向关系；
    # lazy参数禁止自动执行查询（便于添加过滤器，而默认查询是隐藏query对象的，无法指定更精确的查询过滤器）
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):  # __repr__方法返回一个具有可读性的字符串表示模型
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)  # index为True则创建索引，提升查询效率
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 外键

    def __repr__(self):
        return '<User %r>' % self.username


""" 数据库操作
1、创建表
# 创建数据库
from app import db
db.create_all()  # 遍寻所有db.Model子类，然后在数据库中创建对应的表


2、插入行
# 模型的构造函数接受的参数是使用关键字参数指定的模型属性初始值（下面操作对象都只在python中还未写入数据库）
from app import Role, User
admin_role = Role(name='Admin')
mod_role = Role(name='Moderator')
user_role = Role(name='User')
user_john = User(username='john', role=admin_role)
user_susan = User(username='susan', role=user_role)
user_david = User(username='david', role=user_role)

# 对数据库的改动通过数据库会话管理
db.session.add(admin_role)
db.session.add(mod_role)
db.session.add(user_role)
db.session.add(user_john)
db.session.add(user_susan)
db.session.add(user_david)
# 或者简写为：
db.session.add_all([admin_role, mod_role, user_role, user_john, user_susan, user_david])

# 提交会话
db.session.commit()

print(admin_role.id)
print(mod_role.id)
print(user_role.id)


3、修改行
admin_role.name = 'Administrator'
db.session.add(admin_role)
db.session.commit()


4、删除行
db.session.delete(mod_role)
db.session.commit()


5、查询行
# 每个模型都有query对象，使用all()方法取回对应表中的所有记录
Role.query.all()
User.query.all()

# 使用过滤器进行更精确的数据库查询
User.query.filter_by(role=user_role).all()

# 查看SQLAlchemy为查询生成的原生SQL查询语句，将query对象转换为字符串
str(User.query.filter_by(role=user_role))

# first()方法只返回第一个结果
user_role = Role.query.filter_by(name='User').first()
"""


# 定义路由使用 app.route 装饰器
@app.route('/', methods=['GET', 'POST'])  # 如果没有指定methods参数，则只把视图函数注册为GET请求的处理程序
def index():
    form = NameForm()  # 初始化一个表单
    if form.validate_on_submit():  # 如果提交的表单数据能够被所有验证函数接受，返回True
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data  # 将数据存储在用户会话中，可以在多次请求之间记住输入的值
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())


# 设置动态路由，放在尖括号里的内容就是动态部分
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# 客户端请求未知页面或路由时显示
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 应用有未处理的异常时显示
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# shell上下文处理器
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)  # 返回一个字典，包含数据库实例和模型


manager.add_command('shell', Shell(make_context=make_shell_context))
# 添加db命令
manager.add_command('db', MigrateCommand)
"""
1、做好数据库迁移的第一步，初始化相关准备工作(只做一次) 生成migrations文件夹
python flasky.py db init

2、根据模型类生成数据库迁移文件（每次修改了模型类，都要做）
python flasky.py db migrate -m ‘添加User模型类’

3、执行迁移文件，真正修改数据库
python flasky.py db upgrade
"""


# 发送电子邮件
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


if __name__ == '__main__':
    # app.run()
    manager.run()
    # 运行调试模式，开启重载器和调试器
    # 启动重载器后，Flask会监视项目中的所有源代码文件，发现变动时自动重启服务器
    # 调试器是一个基于Web的工具，当应用抛出未处理的异常时，它会出现在浏览器中，此时Web浏览器变成一个交互式栈跟踪
    # app.run(debug=True)
