import os
import requests
import re
import socket
from datetime import datetime,date
from flask import Flask, render_template, session, redirect, url_for, request
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, TextField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import weatherAPIThink as wAPIT


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


def make_shell_context():
    return dict(app=app, db=db, NowTable=NowTable, LifeTable=LifeTable, User = User)

manager.add_command("shell", Shell(make_context=make_shell_context))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    ip = db.Column(db.String(64), unique = True)
    users = db.relationship('NowTable',backref='user')

class NowTable(db.Model):
    __tablename__  = 'nowTables'
    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String(64)) #unique = True
    text = db.Column(db.String(64))
    code = db.Column(db.Integer)
    temperature = db.Column(db.String(16))
    unit = db.Column(db.String(16))
    queryTime = db.Column(db.DateTime,index=True, default=datetime.utcnow)
    user_name = db.Column(db.String(64),db.ForeignKey('users.name'))

    def __repr__(self):
        return '<NowTable %r>' % self.location

def insertNowTable(unit,userInput):
    userList = ipCity()
    ip = userList[1]
    name = userList[0]
    user_name = User.query.filter_by(name=name).first()
    if user_name is None:
         user_name = User(name=name,ip=ip)

    API = 'https://api.thinkpage.cn/v3/weather/now.json'
    result = wAPIT.fetchWeatherThink(unit,userInput).fetchAPIResult(API)
    r = result.json()['results'][0]
    location=r['location']['name']
    unit_list = getUnit()
    nowInfo = NowTable.query.filter_by(location = location).filter_by(unit = unit).first()
    if nowInfo is None:
        nowInfo = NowTable(location=r['location']['name'],
                           text=r['now']['text'],
                           temperature=r['now']['temperature'] + unit_list[1],
                           code=r['now']['code'],
                           unit=unit,
                           user=user_name
                           )
    else:
        pass
    db.session.add(user_name)
    db.session.add(nowInfo)
    db.session.commit()
    return r['location']['name']

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
    else:
        pass
    db.session.add(lifeInfo)
    db.session.commit()


class NameForm(FlaskForm):
    name = StringField(
            '请输入城市中文名称，选择公／英制后，点击查询。',
            validators=[Required()])
    unit = RadioField('unit',
                      choices=[('℃','公制:℃ 摄氏度'),('℉','英制:℉ 华氏度')],
                      default = '℃')
    submit = SubmitField('查 询')

def getUnit():
    form = NameForm()
    if form.unit.data == '℉':
        unit_list = ['f','℉','mph']
    else:
        unit_list = ['c','℃','km/h']
    return unit_list

def ipCity():
    ip = socket.gethostbyname(socket.getfqdn())
    cityUrl = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + ip
    cityResult = requests.get(cityUrl)
    city = cityResult.json()['data']
    cityList = [city['region'] + city['city'],ip]
    return cityList

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['ipText']  =  ipCity()
        userInput = form.name.data.strip()
        unit_list = getUnit()
        insertNowTable(unit_list[0],userInput)
        insertLifeTable(unit_list[0],userInput)

        now = NowTable.query.filter_by(location=userInput).\
            filter_by(unit=unit_list[0]).\
            order_by(db.desc(NowTable.queryTime)).\
            first()

        life = LifeTable.query.\
            filter_by(location=userInput).\
            first()

        session['name'] = now.location

        session['nowText'] = \
            (" {}  温度:  {}  ".format(now.text,now.temperature))

        session['lifeText'] = \
            ("洗车: {};     穿衣: {};     感冒: {};      运动: {};     旅行: {};     紫外线: {}" .\
                format(life.car_washing,life.dressing,life.flu,life.sport,life.travel,life.uv))

        session['nowImg'] = now.code

        form.name.data = ''
        return render_template('index.html', form=form,
                               ipText = session.get('ipText'),
                               name = session.get('name'),
                               nowText = session.get('nowText'),
                               lifeText = session.get('lifeText'),
                               nowImg = session.get('nowImg')
                               )

    return render_template('index.html', form=form)


@app.route('/text.html')
def help():
    session['Text'] = wAPIT.getText("/app/app/README.md")
    return render_template('text.html',Text = session.get('Text'))

@app.route('/history.html')
def history():
    _your_list=[]
    userList = ipCity()
    name = userList[0]
    your = NowTable.query.filter_by(user_name=name).all()
    for r in your:
        yourText = ("{}天气： {}  温度:  {}<br/>".\
                format(r.location,r.text,r.temperature))
    session['youtText'] = ' '.join(_your_list)

    _history_List=[]
    now = NowTable.query.all()
    for r in now:
        text = ("{}天气： {}  温度:  {}  天气代码：{} {}<br/>".\
                format(r.location,r.text,r.temperature,r.code,r.user_name))
        _history_List.append(text)

    session['historyText'] = ' '.join(_history_List)


    return render_template('history.html',
                           historyText = session.get('historyText')
                           ) #yourText = session.get('yourtText'),

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    manager.run()
