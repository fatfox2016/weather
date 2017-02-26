from sqlalchemy import and_
from datetime import datetime,date,timedelta
# from flask import Flask, render_template, session, redirect, url_for, request,flash
from flask_sqlalchemy import SQLAlchemy
from main import db,app
import main.fetchdata as FDA

class NowTable(db.Model):
    __tablename__  = 'nowTables'
    id = db.Column(db.Integer, primary_key = True)
    session_id = db.Column(db.String(255)) #,nullable=False
    location = db.Column(db.String(64)) #unique = True
    text = db.Column(db.String(64))
    temperature = db.Column(db.Integer)
    temperatureUnit = db.Column(db.String(16))
    code = db.Column(db.Integer)
    # dt = db.Column(db.DateTime,nullable=False)
    amendment = db.Column(db.Boolean,default=False)
    lastTime = db.Column(db.DateTime,index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<NowTable %r>' % self.location

class LifeTable(db.Model):
    __tablename__ = 'lifeTables'
    id = db.Column(db.Integer, primary_key = True)
    # now_id = db.Column(db.Integer,db.ForeignKey('nowTables.id'))

    location = db.Column(db.String(64)) #unique = True
    car_washing = db.Column(db.String(64))
    dressing = db.Column(db.String(64))
    flu = db.Column(db.String(64))
    sport = db.Column(db.String(64))
    travel = db.Column(db.String(64))
    uv = db.Column(db.String(64))
    lastTime = db.Column(db.DateTime,index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<LifeTable %r>' % self.location

class DailyTable(db.Model):
    __tablename__ = 'dailyTables'
    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String(64)) #unique = True
    text_day = db.Column(db.String(64))
    code_day = db.Column(db.Integer)
    text_night = db.Column(db.String(64))
    code_night = db.Column(db.Integer)
    high = db.Column(db.Integer)
    low = db.Column(db.Integer)
    wind_direction = db.Column(db.String(64))
    wind_direction_degree = db.Column(db.Integer) #风向角度，范围0~360
    wind_speed = db.Column(db.Integer)   #风速，单位km/h（当unit=c时）、mph（当unit=f时）
    wind_scale = db.Column(db.Integer)  #风力等级
    temperatureUnit = db.Column(db.String(16))
    windUnit = db.Column(db.String(16))
    day = db.Column(db.Integer)
    amendment = db.Column(db.Boolean,default=False)
    lastTime = db.Column(db.DateTime,index=True, default=date.today()) #default=date.today())

    def __repr__(self):
        return '<DailyTable %r' % self.location

class HistoryTable(db.Model):
    __tablename__='historyTables'
    id = db.Column(db.Integer,primary_key=True)
    session_id = db.Column(db.String(255))
    location = db.Column(db.String(64)) #unique = True
    text = db.Column(db.String(64))
    temperature = db.Column(db.Integer)
    temperatureUnit = db.Column(db.String(16))
    code = db.Column(db.Integer)
    # dt = db.Column(db.DateTime,nullable=False)
    amendment = db.Column(db.Boolean,default=False)
    lastTime = db.Column(db.DateTime,index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<HistoryTable %r>' % self.location

# class Description(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     desc_id = db.Column(db.Integer,nullable=False)
#     group = db.Column(db.String(20),nullable=False)
#     description = db.Column(db.String(50),nullable=False)
#
#     def __init__(self,desc_id,group,descrption):
#         self.desc_id = desc_id
#         sefl.group = group
#         self.description = desciption
#
#     def __repr__(self):
#         return '<APP description %r>' %self.description

class BaseModel(object):
    def __init__(self,session_id):
        self.now = FDA.NowData()
        self.life = FDA.LifeData()
        self.session_id = session_id

    def processLife(self,life):
        L={}
        L['洗车指数：'] = life.car_washing
        L['穿衣指数：'] = life.dressing
        L['感冒指数：'] = life.flu
        L['运动指数：'] = life.sport
        L['旅游指数：'] = life.travel
        L['紫外线指数：'] = life.uv

        return L

class NowModel(BaseModel):
    def __init__(self,session_id,location,unit='c'):
        super().__init__(session_id)
        self.location = location
        self.unit = unit

    def getBasic(self):
        app.logger.info('Begin now weather：{}'.format(self.location))
        condition = and_(NowTable.session_id == self.session_id,
                         NowTable.temperatureUnit == self.unit,
                         NowTable.location == self.location)
        '''检查数据库中是否有所查信息'''
        basic = NowTable.query.filter(condition).first()
        # basic = NowTable.query.filter_by(session_id == self.session_id).\
        #                        filter_by(location == self.location).first()

        app.logger.debug('Now weather：{}'.format(self.location))
        app.logger.info('Query over')
        return basic


    def save(self):
        basic = self.getBasic()
        if basic:
            if basic.lastTime.date() != date.today():
                dataN = self.now.fetchNow(self.location,self.unit)
                now = self.now.nowData(dataN)
                self.insertNow(now)
                dataL = self.life.fetchLife(self.location)
                life = self.life.lifeData(dataL)
                self.insertLife(life)

            else:
                if basic.temperatureUnit != self.unit:
                    data = self.now.fetchNow(self.location,self.unit)
                    now = self.now.nowData(data)
                    self.insertNow(now)

                else:
                    if basic.lastTime < datetime.now()-timedelta(minutes=5):
                        # print('now5')
                        dataN = self.now.fetchNow(self.location,self.unit)
                        now = self.now.nowData(dataN)
                        self.update(basic,now)
                    # else:
                    #     print('now6')
        else:
            dataN = self.now.fetchNow(self.location,self.unit)
            now = self.now.nowData(dataN)
            self.insertNow(now)
            dataL = self.life.fetchLife(self.location)
            life = self.life.lifeData(dataL)
            self.insertLife(life)

    def insertNow(self,now):
        app.logger.info('Begin to insert now weather:{}'
                        .format(now['location']))
        nowRecode = NowTable(session_id=self.session_id,
                        location=now['location'],
                        text=now['text'],
                        temperature=now['temperature'],
                        temperatureUnit=now['temperatureUnit'],
                        code=now['code'])

        app.logger.debug('now weather:{}'.format(nowRecode))

        db.session.add(nowRecode)
        db.session.commit()

        app.logger.info('End of insert now ')

        model = HistoryModel(self.session_id)
        model.save(nowRecode)

    def insertLife(self,life):
        app.logger.info('Begin to insert life:{}'
                        .format(life['location']))
        lifeRecode = LifeTable(location=life['location'],
                            car_washing=life['car_washing'],
                            dressing=life['dressing'],
                            flu=life['flu'],
                            sport=life['sport'],
                            travel=life['travel'],
                            uv=life['uv'])

        app.logger.debug('life infomation:{}'.format(lifeRecode))

        db.session.add(lifeRecode)
        db.session.commit()

        app.logger.info('End of insert  life ')

    def update(self,basic,now):
        app.logger.info('Begin to update now weather:{}'
                        .format(basic.location))
        basic.text = now['text']
        basic.amendment = False
        basic.code = now['code']
        basic.temperature = now['temperature']
        basic.temperatureUnit = now['temperatureUnit']
        basic.lastTime = datetime.now()
        app.logger.debug('Now weather:{}'.format(basic))
        db.session.add(basic)
        db.session.commit()

        app.logger.info('End of update ')

    def getLife(self,userInput):
        life = LifeTable.query.filter_by(location=userInput).first()
        return life

    def modify(self,line,info):
        nowInfo = self.getBasic()
        nowInfo.line = (info)
        db.session.add(nowInfo)
        db.session.commit()

class DailyModel(object):
    def __init__(self,location,unit='c'):
        self.daily = FDA.DailyData()
        self.location = location
        self.unit = unit

    def save(self):
        condition = and_(DailyTable.location == self.location,
                         DailyTable.temperatureUnit == self.unit)
        dailyData = DailyTable.query.filter(condition).all()
        if not dailyData:
            daily = self.daily.fetchDaily(self.location,self.unit)
            dailylist = self.daily.dailyData(daily)
            self.insert(dailylist)
        else:
            if dailyData[0].lastTime.date() != date.today():
                self.delete(dailyData)
                daily = self.daily.fetchDaily(self.location,self.unit)
                dailylist = self.daily.dailyData(daily)
                self.insert(dailylist)

    def get(self):
        app.logger.info('Begin to query dailyData of user:{}'
                        .format(self.location))
        condition = and_(DailyTable.location == self.location,
                         DailyTable.temperatureUnit == self.unit)
        dailyData = DailyTable.query.filter(condition).all()
        app.logger.debug('dailyData:{}'.format(dailyData))
        app.logger.info('End of query dailyData')
        return dailyData

    def insert(self,daily):
        for i in daily:
            app.logger.info('Begin to insert daily:{}'.format(i['location']))
            dailyRecord = DailyTable(location = i['location'],
                                    text_day = i['text_day'],
                                    code_day = i['code_day'],
                                    text_night = i['text_night'],
                                    code_night = i['code_night'],
                                    high = i['high'],
                                    low = i['low'],
                                    wind_direction = i['wind_direction'],
                                    wind_direction_degree = i['wind_direction_degree'],
                                    wind_speed = i['wind_speed'],
                                    wind_scale = i['wind_scale'],
                                    temperatureUnit = i['temperatureUnit'],
                                    windUnit = i['windUnit'],
                                    day = i['day'])

            app.logger.debug('history :{}'.format(dailyRecord))

            db.session.add(dailyRecord)
            db.session.commit()

            app.logger.info('End of insert history')

    def delete(self,dailyData):
        app.logger.info('Begin to update now weather:{}'
                            .format(dailyData[0].location))
        for r in dailyData:
            db.session.delete(r)
            db.session.commit()

        app.logger.info('End of update ')

    # def update(self,dailyData,daily):
    #     for r,i in dailyData,daily:
    #         app.logger.info('Begin to update now weather:{}'
    #                         .format(r.location))
    #         r.location = i['location']
    #         r.text_day = i['text_day']
    #         r.code_day = i['code_day']
    #         r.text_night = i['text_night']
    #         r.code_night = i['code_night']
    #         r.high = i['high']
    #         r.low = i['low']
    #         r.wind_direction = i['wind_direction']
    #         r.wind_direction_degree = i['wind_direction_degree']
    #         r.wind_speed = i['wind_speed']
    #         r.wind_scale = i['wind_scale']
    #         r.temperatureUnit = i['temperatureUnit']
    #         r.windUnit = i['windUnit']
    #         r.day = i['day']
    #         r.lastTime = date.today()
    #
    #         db.session.add(r)
    #         db.session.commit()
    #
    #         app.logger.info('End of update ')


class HistoryModel(BaseModel):
    def __init__(self,session_id):
        super().__init__(session_id)

    def save(self,now):
        # history = HistoryTable.query.filter_by(session_id == now.session_id).\
        #                              filter_by(location == now.location).\
        #                              filter_by(temperatureUnit == now.temperatureUnit).\
        #                              filter_by(lastTime == now.lastTime).first()
        condition = and_(HistoryTable.session_id == now.session_id,
                         HistoryTable.location == now.location,
                         HistoryTable.temperatureUnit == now.temperatureUnit,
                         HistoryTable.lastTime == now.lastTime)
        history = HistoryTable.query.filter(condition).first()
        if not history:
            self.insert(now)

    def insert(self,now):
        app.logger.info('Begin to insert history:{}'.format(now.location))
        history = HistoryTable(session_id=now.session_id,
                               location=now.location,
                               text=now.text,
                               temperature=now.temperature,
                               temperatureUnit=now.temperatureUnit,
                               code=now.code)
        app.logger.debug('history :{}'.format(history))

        db.session.add(history)
        db.session.commit()
        app.logger.info('End of insert history')

    def get(self):
        app.logger.info('Begin to query history of user:{}'
                        .format(self.session_id))
        history_record = HistoryTable.query.filter_by(
                  session_id=self.session_id).all()
        app.logger.debug('history:{}'.format(history_record))
        app.logger.info('End of query history')
        return history_record

    def processHistory(self,history):
        historyList = []
        if history:
            for r in history:
                historyList.append(r)
        return historyList

# class Modify(object):
#     def __init__(self,session_id,location,unit):
#         self.session_id = session_id
#         self.location = location
#         self.unit = unit
#
#     def getData(self):
#         condition = and_(NowTable.session_id == now.session_id,
#                          NowTable.location == now.location,
#                          NowTable.temperatureUnit == unit)
#         data = NowTable.query.filter(condition).first()
#         return data




# class CityTable(db.Model):
#     __tablename__ = 'citytables'
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(64))
#     # ip = db.Column(db.String(64), unique = True)
#     # cities = db.relationship('NowTable',backref='city')
#
#     def __repr__(self):
#         return '<CityTable %r>' % self.name

