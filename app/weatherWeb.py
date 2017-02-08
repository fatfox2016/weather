from flask import Flask, render_template, session, redirect, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, TextField
from wtforms.validators import Required
import weatherAPIThink as wAPIT

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string with fatfox2016'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('请输入城市中文名称或者拼音,选择公／英制后，点击查询', validators=[Required()])
    unit = RadioField('Label', choices=[('value','公制:℃ 摄氏度'),('value_two','英制:℉华氏度')])
    submit = SubmitField('查 询')

# class TextForm(FlaskForm):
#     text = TextAreaField()

def getUnit():
    form = NameForm()
    if form.unit.data == 'value_two':
        unit_list = ['f','℉ 华氏度','mph']
    else:
        unit_list = ['c','℃ 摄氏度','km/h']
    return unit_list

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # ipCity = wAPIT.ipCity()
        session['ipText']  =  wAPIT.ipCity() #'您所在地:' + ipCity['region'] + ipCity['city']

        userInput = form.name.data
        unit_list = getUnit()
        _query_weather_now = wAPIT.fetchWeatherThink(unit_list[0],userInput).nowDict()
        _query_weather_life = wAPIT.fetchWeatherThink(unit_list[0],userInput).lifeDict()
        _query_weather_daily = wAPIT.fetchWeatherThink(unit_list[0],userInput).dailyDict()
        session['name'] = _query_weather_now['location']

        _history_List.append(_query_weather_now['location']
                             + '实时天气:' + _query_weather_now['text']
                             + ' 温度:' + _query_weather_now['temperature']
                             + unit_list[1] + '<br/>')
        if _query_weather_now['status'] == '200' and _query_weather_daily['status'] == '200' :
            session['nowText'] = ('实时天气:' + _query_weather_now['text']
                                + ' 温度:' + _query_weather_now['temperature'] + unit_list[1])
            session['lifeText'] = ('生活指数:<br/>' + ' 洗车:' + _query_weather_life['car_washing']
                                + ';  穿衣:' + _query_weather_life['dressing']
                                + ';  感冒:' + _query_weather_life['flu']
                                + ';  运动:' + _query_weather_life['sport']
                                + ';  旅行:' + _query_weather_life['travel']
                                + ';  紫外线:' + _query_weather_life['uv'])
            #today
            session['daily0Text'] =  ('今日温度:' + _query_weather_daily['low_d0'] + ' ~ '
							+ _query_weather_daily['high_d0'] + unit_list[1]
							+ ' 风向:' + _query_weather_daily['wind_direction_d0']
							+ ' 风速:' + _query_weather_daily['wind_scale_d0']
						  	+ unit_list[2])
            session['nowImg'] = '<img src= "/static/' + _query_weather_now['code'] + '.png" />'
            #tommrow
            session['daily1Text'] =  ('明日温度:' + _query_weather_daily['low_d1'] + ' ~ '
							+ _query_weather_daily['high_d1'] + unit_list[1]
							+ ' 风向:' + _query_weather_daily['wind_direction_d1']
							+ ' 风速:' + _query_weather_daily['wind_scale_d1']
						  	+ unit_list[2])
            session['dailyImg1'] = '<img src= "/static/' + _query_weather_daily['code_day_d1'] + '.png" />'
			#after tommrow
            session['daily2Text'] =  ('后日温度:' + _query_weather_daily['low_d2'] + ' ~ '
							+ _query_weather_daily['high_d2'] + unit_list[2]
							+ ' 风向:' + _query_weather_daily['wind_direction_d2']
							+ ' 风速:' + _query_weather_daily['wind_scale_d2']
						  	+ unit_list[2])
            session['dailyImg2'] = '<img src= "/static/' + _query_weather_daily['code_day_d2'] + '.png" />'
        else:
            session['text'] = '信息获取有误，请重新输入查询！'
        form.name.data = ''
        return render_template('index.html', form=form,
                               ipText = session.get('ipText'),
                               name = session.get('name'),
                               nowText = session.get('nowText'),
                               lifeText = session.get('lifeText'),
                               daily0Text = session.get('daily0Text'),
                               nowImg = session.get('nowImg'),
                               daily1Text = session.get('daily1Text'),
                               dailyImg1 = session.get('dailyImg1'),
                               daily2Text = session.get('daily2Text'),
                               dailyImg2 = session.get('dailyImg2')
                               )

    return render_template('index.html', form=form)



@app.route('/text.html')
def help():
    session['Text'] = wAPIT.getText('README.md')
    return render_template('text.html',Text = session.get('Text'))


@app.route('/history.html')
def history():
    session['historyText'] = ' '.join(_history_List)
    return render_template('history.html', historyText = session.get('historyText'))

if __name__ == '__main__':
    _query_weather_now = {}
    _query_weather_life = {}
    _query_weather_daily = {}
    _history_List = []
    manager.run(host='0.0.0.0')
