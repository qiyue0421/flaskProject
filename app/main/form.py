# 表单扩展
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# 定义表单类，包含一个文本字段和一个提交按钮
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])  # 第一个参数为HTML的label，DataRequired()为验证函数，确保输入文本不为空
    submit = SubmitField('Submit')
