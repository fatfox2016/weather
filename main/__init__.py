import json
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler #该RotatingFileHandler级，位于在logging.handlers 模块，支持磁盘日志文件轮换
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session,SqlAlchemySessionInterface

'''
实例化
'''
app = Flask(__name__)

app.config.from_object('config')
app.secret_key = 'hard to guess string'

db = SQLAlchemy(app)


Session(app)
app.session_interface = SqlAlchemySessionInterface(app,db,'session','')

'''
日志配置
'''
handler = RotatingFileHandler('weather.log',maxBytes = 10000,backupCount = 5)
handler.setLevel(logging.INFO)
handler.setFormatter(Formatter('%(asctime)s %(levelname)s: $(message)s '
                               '[in %(modules)s - %(funcName)s:%(lineno)d]'))
app.logger.addHandler(handler)

from main.weatherWeb import main
# from app.database import Description

app.register_blueprint(main)

#
# def loadDescription():
#     with open('description.json',enconding='utf-8') as file:
#         text = file.readlines()
#         for line in text:
#             data = json.loads(line)
#             record = Description(data['desc_id'],data['group'],
#                                  data['description'])
#             db.session.add(recond)
#             db.session.commit()

#创建数据库

db.create_all()
# loadDescription()