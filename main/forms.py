# import re
# from flask import Flask, render_template, session, redirect, url_for, request,flash
# from flask_script import Manager,Shell
# from flask_bootstrap import Bootstrap
# from flask_moment import Moment

from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField,IntegerField,\
                    validators,ValidationError
from wtforms.validators import Required,AnyOf,NumberRange,Optional,Regexp
# from sqlalchemy import disinct
from main import db
# from database import Description

class NameForm(FlaskForm):
    name = StringField(
            '请输入城市中文名称，选择公／英制后，点击查询。',
            validators=[Required()])
    unit = RadioField('unit',
                      choices=[('c','公制:℃ 摄氏度'),('f','英制:℉ 华氏度')],
                      default = 'c')
    nowSubmit = SubmitField('实时天气')
    dailySubmit = SubmitField('多日天气')


class ModifyForm(FlaskForm):
    location = StringField(
            '请输入城市中文名称：',
            validators=[Required()])
    text = StringField(
            '请输入天气情况：(例如：\'晴\'、\'多云\'、\'阴\'、\'小雨\'、\'大雪\'等)',
            validators=[AnyOf(values=['晴','多云','阴','小雨','大雨',
                                      '中雨','大雪','小雪','中雪','雾'
                                      ], message='输入错误，请按提示输入'),Optional()])
    temperature = StringField(
            '请输入温度：',validators=[Optional()])
    unit = RadioField('unit',
                      choices=[('c','公制:℃ 摄氏度'),('f','英制:℉ 华氏度')],
                      default = 'c')

    code = IntegerField('请输入气象代码：(范围0-38的整数)',
                       validators=[NumberRange(
                               min=0,max=38,message = '输入错误，请按提示输入'),
                       Optional()]
                       ) #NumberRange(min=0,max=38),

    submit = SubmitField('提交更改')