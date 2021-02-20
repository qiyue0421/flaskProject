from . import db


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