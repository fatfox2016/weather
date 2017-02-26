import os
import re
from flask import Flask, render_template, session, redirect, url_for, request,flash,Blueprint
from main.forms import NameForm,ModifyForm
from main.database import NowModel,DailyModel,HistoryModel

textdir = os.path.abspath(os.path.dirname(__file__))
main = Blueprint('main',__name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    session_id = request.cookies.get('session')
    if form.validate_on_submit():
        userInput = form.name.data.strip()
        unit = form.unit.data
        try:
            if re.match(u'([\u4e00-\u9fff]+)',userInput):
                if form.nowSubmit.data:
                    nowModel = NowModel(session_id,userInput,unit) #获取城市实例
                    nowModel.save() #检索数据库信息，根据判断结果更新数据
                    now = nowModel.getBasic()
                    lifeModel = nowModel.getLife(userInput)
                    life = nowModel.processLife(lifeModel)

                    return render_template('index.html', form=form,
                                            now=now,life=life)

                elif form.dailySubmit.data:

                    dailyModel = DailyModel(userInput,unit)
                    dailyModel.save()
                    daily = dailyModel.get()

                    return render_template('index.html', form=form,daily=daily)

            else:
                flash('请输入城市中文名称！')
                return render_template('index.html', form=form)

        except Exception as e:
            flash('您找的{}走丢了！请输入正确城市中文名称！'.format(userInput))
            return render_template('index.html', form=form)

    return render_template('index.html', form=form)

@main.route('/history.html')
def history():
    session_id = request.cookies.get('session')
    historyModel = HistoryModel(session_id)
    historyRecord = historyModel.get()
    history = historyModel.processHistory(historyRecord)
    if history:
        print(history)
        return render_template('history.html',history=history)
    else:
        flash('无记录！')
        return render_template('history.htme')

@main.route('/help.html')
def help():
    fileName = os.path.join(textdir, 'README.md')
    with open(fileName,'r',encoding = "utf8") as file:
        session['help'] = file.read()
    return render_template('help.html',Text = session.get('help'))

@main.route('/modify.html', methods=['GET', 'POST'])
def modify():
    form = ModifyForm()
    session_id = request.cookies.get('session')
    if form.validate_on_submit():
        location = form.location.data.strip()
        unit = form.unit.data
        nowModel = NowModel(session_id,location,unit)
        now = nowModel.getBasic()
        if now:
            nowText = form.text.data
            if nowText != '':
                nowModel.midofy('text',nowText)

            temperatureText = form.temperature.data
            if temperatureText != '':
                nowModel.midofy('temperature',temperatureText)

            codeInt = form.code.data
            if codeInt is not None:
                nowModel.midofy('code',codeInt)

            flash('修改成功，请再次查询')
            return render_template('modify.html',form=form,
                                    now=now,alert = False)
        else:
            flash('您好像没搜过这个城市！请您回到主页先找找看，如果有错误欢迎再来！')
            return render_template('modify.html',form=form,alert = True)
    else:
        return render_template('modify.html',form=form)

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



