from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .form import NameForm
from .. import db
from ..model import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
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
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())
