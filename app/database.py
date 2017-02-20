import os
import requests
import re
import socket
from datetime import datetime,date
from flask import Flask, render_template, session, redirect, url_for, request,flash
# from flask_script import Manager,Shell
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import weatherAPIThink as wAPIT


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
# app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# moment = Moment(app)
db = SQLAlchemy(app)


class CityTable(db.Model):
    __tablename__ = 'citytables'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    # ip = db.Column(db.String(64), unique = True)
    # cities = db.relationship('NowTable',backref='city')

    def __repr__(self):
        return '<CityTable %r>' % self.name

class NowTable(db.Model):
    __tablename__  = 'nowTables'
    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String(64)) #unique = True
    text = db.Column(db.String(64))
    code = db.Column(db.Integer)
    temperature = db.Column(db.String(16))
    unit = db.Column(db.String(16))
    queryTime = db.Column(db.DateTime,index=True, default=datetime.utcnow)
    # city_name = db.Column(db.String(64),db.ForeignKey('cities.id'))

    def __repr__(self):
        return '<NowTable %r>' % self.location

class LifeTable(db.Model):
    __tablename__ = 'lifeTables'
    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String(64)) #unique = True
    car_washing = db.Column(db.String(64))
    dressing = db.Column(db.String(64))
    flu = db.Column(db.String(64))
    sport = db.Column(db.String(64))
    travel = db.Column(db.String(64))
    uv = db.Column(db.String(64))
    queryTime = db.Column(db.DateTime,index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<LifeTable %r>' % self.location



def insertCityTable(userInput):
    city = CityTable.query.filter_by(name = userInput).first()
    if city is None:
        city = CityTable(name=userInput)
    db.session.add(city)
    db.session.commit()


def insertNowTable(unit,userInput):
    r = wAPIT.fetchWeatherThink(unit,userInput).nowDict()
    # location=r['location']
    # unit_list = getUnit()
    nowInfo = NowTable.query.filter_by(location = userInput).filter_by(unit = unit).first()
    nowInfo = NowTable(location=r['location'],
                        text=r['text'],
                        temperature=r['temperature'],#+ unit_list[1],
                        code=r['code'],
                        unit=unit
                        )
    db.session.add(nowInfo)
    db.session.commit()

def insertLifeTable(unit,userInput):
    r = wAPIT.fetchWeatherThink(unit,userInput).lifeDict()
    lifeInfo = LifeTable.query.filter_by(location = userInput).first() #

    if lifeInfo is None:
        lifeInfo = LifeTable(location=r['location'],
                             car_washing = r['car_washing'],
                             dressing = r['dressing'],
                             flu = r['flu'],
                             sport = r['sport'],
                             travel = r['travel'],
                             uv = r['uv']
                             )
    db.session.add(lifeInfo)
    db.session.commit()

def updataNowTable(location,Info):
    nowInfoC = NowTable.query.filter_by(location = location).filter_by(unit = 'c').first()
    nowInfoF = NowTable.query.filter_by(location = location).filter_by(unit = 'f').first()
    if nowInfoC is not None:
        nowInfoC.text = (Info)
        db.session.add(nowInfoC)
    if nowInfoF is not None:
        nowInfoF.text = (Info)
        db.session.add(nowInfoF)
    db.session.commit()

if __name__ == '__main__':

    db.drop_all()
    db.create_all()