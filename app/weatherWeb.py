import requests
import re
import socket
from flask import Flask, render_template, session, redirect, url_for, request,flash
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField,IntegerField
from wtforms.validators import Required,AnyOf,NumberRange,Optional,Regexp
import weatherAPIThink as wAPIT
from database import CityTable,NowTable,LifeTable,insertCityTable,insertNowTable,insertLifeTable,updataNowTable,db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


def make_shell_context():
    return dict(app=app, db=db, NowTable=NowTable, LifeTable=LifeTable, User = User)

manager.add_command("shell", Shell(make_context=make_shell_context))


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

def validateInput(unit,userInput):
    '''Validate the input text effectively'''
    nowInfo = NowTable.query.filter_by(location = userInput).filter_by(unit = unit).first()
    if nowInfo is None:
        r = wAPIT.fetchWeatherThink(unit,userInput).nowDict()
        if r['status'] != '200':
            flash('因网络问题，您查询的结果走丢了！')
            return False
        else:
            insertCityTable(userInput)
            insertNowTable(unit,userInput)
            insertLifeTable(unit,userInput)
            return True
    else:
        return True

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['ipText']  =  ipCity()
        userInput = form.name.data.strip()
        if re.match(u'([\u4e00-\u9fff]+)',userInput):
            unit_list = getUnit()
            if validateInput(unit_list[0],userInput) is True:
                now = NowTable.query.filter_by(location=userInput).\
                    filter_by(unit=unit_list[0]).\
                    order_by(db.desc(NowTable.queryTime)).\
                    first()

                life = LifeTable.query.\
                    filter_by(location=userInput).\
                    first()

                session['name'] = now.location

                if now.unit == 'c':
                    tUnit = '℃'
                else:
                    tUnit = '℉'
                session['nowText'] = \
                        (" {}  温度:  {}  {}".format(now.text,now.temperature,tUnit))

                session['lifeText'] = \
                        ("洗车: {};     穿衣: {};     感冒: {};      运动: {};     旅行: {};     紫外线: {}" .\
                            format(life.car_washing,life.dressing,life.flu,life.sport,life.travel,life.uv))

                session['nowImg'] = ("<img src= \"/static/{}.png \" />".format(now.code))

                form.name.data = ''

                return render_template('index.html', form=form,
                                        ipText = session.get('ipText'),
                                        name = session.get('name'),
                                        nowImg = session.get('nowImg'),
                                        nowText = session.get('nowText'),
                                        lifeText = session.get('lifeText'))
            return render_template('index.html', form=form)
        else:
            flash('请输入城市中文名称！')
            return render_template('index.html', form=form)

    return render_template('index.html', form=form)

@app.route('/help.html')
def help():
    session['help'] = wAPIT.getText("\app\app\README.md")
    return render_template('help.html',Text = session.get('help'))

@app.route('/history.html')
def history():
    # _your_list=[]
    # userList = ipCity()
    # name = userList[0]
    # your = NowTable.query.filter_by(user_name=name).all()
    # for r in your:
    #     yourText = ("{}天气： {}  温度:  {}<br/>".\
    #             format(r.location,r.text,r.temperature))
    # session['youtText'] = ' '.join(_your_list)

    _history_List=[]
    now = NowTable.query.all()
    for r in now:
        if r.unit == 'c':
            tUnit = '℃'
        else:
            tUnit = '℉'
        text = ("{}天气： {}  温度:  {}{}  天气代码：{} <br/>".\
                format(r.location,r.text,r.temperature,tUnit,r.code))
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

class InfoForm(FlaskForm):
    location = StringField(
            '请输入城市中文名称：',
            validators=[Required()])
    text = StringField(
            '请输入天气情况，例如：\'晴\'、\'多云\'、\'阴\'、\'小雨\'、\'大雪\'等。',
            validators=[AnyOf(values=['晴','多云','阴','小雨','大雨',
                                      '中雨','大雪','小雪','中雪','雾'
                                      ], message='输入错误，请按提示输入'),Optional()])
    # temperature = StringField(
    #         '请输入温度及单位（℃或℉)',validators=[Optional()])
    #
    # code = IntegerField('请输入气象代码(范围0-38的整数)',
    #                    validators=[NumberRange(
    #                            min=0,max=38,message = '输入错误，请按提示输入'),
    #                    Optional()]
    #                    ) #NumberRange(min=0,max=38),

    submit = SubmitField('提交更正')



@app.route('/text.html', methods=['GET', 'POST'])
def modify():
    form = InfoForm()
    if form.validate_on_submit():
        location = form.location.data.strip()

        nowText = form.text.data
        if nowText != '':
            updataNowTable(location,nowText)
            # nowInfoC = NowTable.query.filter_by(location = location).filter_by(unit = 'c').first()
            # nowInfoF = NowTable.query.filter_by(location = location).filter_by(unit = 'f').first()
            # print(nowInfoF)
            # print(nowInfoC)
            # if nowInfoC is not None:
            #     nowInfoC.text = (nowText)
            #     db.session.add(nowInfoC)
            # if nowInfoF is not None:
            #     nowInfoF.text = (nowText)
            #     db.session.add(nowInfoF)
            # db.session.commit()

        # temperatureText = form.temperature.data
        # if temperatureText != '':
        #     updataNowTable(location,'temperature',temperatureText)
        #
        # codeInt = form.code.data
        # if codeInt != '':
        #     updataNowTable(location,'code',codeInt)

        flash('修改成功，请再次查询')
        C = NowTable.query.filter_by(location = location).filter_by(unit = 'c').first()
        F = NowTable.query.filter_by(location = location).filter_by(unit = 'f').first()
        if C is not None:
            session['textC'] = ("公制数据：{}天气： {}  温度:  {}  天气代码：{} <br/>".\
                    format(C.location,C.text,C.temperature,C.code))
        if F is not None:
            session['textF'] = ("英制数据：{}天气： {}  温度:  {}  天气代码：{} <br/>".\
                    format(F.location,F.text,F.temperature,F.code))
        return render_template('text.html', form=form,
                               textC = session.get('textC'),
                               textF = session.get('textF'))

    return render_template('text.html', form=form)


if __name__ == '__main__':

    db.drop_all()
    db.create_all()
    manager.run()

