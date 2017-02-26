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
    life = db.relationship('LifeTable',backref=db.backref('now'),
                           uselist=False)

    def __init__(self,session_id,location,text,
                 temperature,temperatureUnit,code):
        self.session_id = session_id
        self.loctation = location
        self.text = text
        self.temperature = temperature
        self.temperatureUnit = temperatureUnit
        # self.dt = dt
        self.code = code

    def __repr__(self):
        return '<NowTable %r>' % self.location

class LifeTable(db.Model):
    __tablename__ = 'lifeTables'
    id = db.Column(db.Integer, primary_key = True)
    now_id = db.Column(db.Integer,db.ForeignKey('nowTables.id'))

    location = db.Column(db.String(64)) #unique = True
    car_washing = db.Column(db.String(64))
    dressing = db.Column(db.String(64))
    flu = db.Column(db.String(64))
    sport = db.Column(db.String(64))
    travel = db.Column(db.String(64))
    uv = db.Column(db.String(64))
    lastTime = db.Column(db.DateTime,index=True, default=datetime.utcnow)

    def __init__(self,session_id,location,car_washing,dressing,
                 flu,sport,travel,uv,now):
        self.session_id = session_id
        self.location = location
        self.car_washing = car_washing
        self.dressing = dressing
        self.flu = flu
        self.sport = sport
        self.travel = travel
        self.uv = uv
        self.now = now

    def __repr__(self):
        return '<LifeTable %r>' % self.now

class HistoryTable(db.Model):
    __tablename__='historyTable'
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

    def __init__(self,session_id,location,text,code,
                 temperature,temperatureUnit):
        self.session_id = session_id
        self.loctation = location
        self.text = text
        self.temperature = temperature
        self.temperatureUnit = temperatureUnit
        self.code = code
        # self.dt = dt


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

class BaseMode(object):
    def __init__(self,session_id):
        self.now = FDA.NowData()
        self.life = FDA.LifeData()
        self.session_id = session_id

class NowModel(BaseMode):
    def __init__(self,session_id,location,unit='c'):
        super().__init__(session_id)
        self.location = location
        self.unit = unit

    def getBasic(self):
        app.logger.info('Begin now weather：{}'.format(self.location))
        condition = and_(NowTable.session_id == self.session_id,
                         NowTable.location == self.location)
        '''检查数据库中是否有所查信息'''
        basic = NowTable.query.filter(condition).first()
        # basic = NowTable.query.filter_by(session_id == self.session_id).\
        #                        filter_by(location == self.location).first()

        app.logger.debug('Now weather：{}'.format(self.location))
        app.logger.info('Query over')
        return basic

    def getData(self,basic):
        data = self.now.fetchNow(self.location,self.unit) #获取API信息
        if isinstance(data,dict):
            now = self.now.nowData(data)
            self.update(basic,now)

    def save(self):
        basic = self.getBasic()
        print(basic)
        if basic:
            if basic.temperatureUnit != self.unit:
                print(basic)
                getData(basic)
            else:
                if basic.lastTime < datetime.now()-timedalta(minutes=5):
                    getData(basic)
        else:
            dataN = self.now.fetchNow(self.location,self.unit)
            now = self.now.nowData(dataN)
            print(now)
            dataL = self.life.fetchLife(self.location)
            life = self.life.lifeData(dataL)
            print(life)
            self.insert(now,life)

    def insert(self,now,life):
        app.logger.info('Begin to insert now weather:{}'
                        .format(now['location']))
        nowRecode = NowTable(self.session_id,
                        now['location'],
                        now['text'],
                        now['temperature'],
                        now['temperatureUnit'],
                        now['code']
                        )
        print(nowRecode)
        app.logger.debug('now weather:{}'.format(nowRecode))

        lifeRecode = LifeTable(self.session_id,
                         life['location'],
                         life['car_washing'],
                         life['dressing'],
                         life['flu'],
                         life['sport'],
                         life['travel'],
                         life['uv'],
                         nowRecode)
        app.logger.debug('life infomation:{}'.format(lifeRecode))

        db.session.add(nowRecode)
        db.session.add(lifeRecode)
        db.session.commit()

        app.logger.info('End of insert now and life')

        model = HistoryModel(self.session_id)
        model.save(nowRecode)

    def update(self,basic,now):
        app.logger.info('Begin to update now weather:{}'
                        .format(now.location))
        if (basic.amendment is False) or (now.amendment is True
                                        and now.lastTime.date() != date.today()):
            basic.text = now['text']
            basi.amendment = False
        basic.code = now['code']
        basic.temperature = now['temperature']
        basic.temperatureUnit = now['temperatureUnit']
        basic.lastTime = now['lastTime']
        app.logger.debug('Now weather:{}'.format(basic))
        db.seesion.commit()

        life = LifeData.query.filter_by(now_id=now_id).first()
        if life:
            life.car_washing = now['car_washing']
            life.dressing = now['dressing']
            life.flu = now['flu']
            life.sport = now['sport']
            life.travel = now['travel']
            life.uv = now['uv']
            life.lastTime = datetime.now()
            app.logger.debug('Now life infomation:{}'.format(life))
            db.session.commit()
        app.logger.info('Update over')

        model = HistoryModel(self.session_id)
        model.save(basic,life)

    def getLife(self,basic_id):
        life = LifeData.query.filter_by(now_id=now_id).first()
        return life

class HistoryModel(BaseMode):
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
        history = HistoryTable(now.session_id,
                               now.location,
                               now.text,
                               now.temperature,
                               now.temperatureUnit,
                               now.code)
        app.logger.debug('history :{}'.format(history))

        db.session.add(history)
        db.session.commit()
        app.logger.info('End of insert history')

    def get(self):
        app.logger.info('Begin to query history of user:{}'
                        .format(self.session_id))
        history_record = HistoryTable.query.filter_by(
                  session_id=self.session_id).all()
        # history = self.processHistory(history_record)
        app.logger.debug('history:{}'.format(history))
        app.logger.info('End of query history')
        return history

    # def processHistory(self,history):
    #     historyList = []
    #     if history:
    #         for r in history:


# def insertNowTable(unit,userInput):
#     r = wAPIT.fetchWeatherThink(unit,userInput).nowDict()
#     # location=r['location']
#     # unit_list = getUnit()
#     nowInfo = NowTable.query.filter_by(location = userInput).filter_by(unit = unit).first()
#     nowInfo = NowTable(location=r['location'],
#                         text=r['text'],
#                         temperature=r['temperature'],#+ unit_list[1],
#                         code=r['code'],
#                         unit=unit
#                         )
#     db.session.add(nowInfo)
#     db.session.commit()
#
# def insertLifeTable(unit,userInput):
#     r = wAPIT.fetchWeatherThink(unit,userInput).lifeDict()
#     lifeInfo = LifeTable.query.filter_by(location = userInput).first() #
#
#     if lifeInfo is None:
#         lifeInfo = LifeTable(location=r['location'],
#                              car_washing = r['car_washing'],
#                              dressing = r['dressing'],
#                              flu = r['flu'],
#                              sport = r['sport'],
#                              travel = r['travel'],
#                              uv = r['uv']
#                              )
#     db.session.add(lifeInfo)
#     db.session.commit()
#
# def updataNowTable(location,Info):
#     nowInfoC = NowTable.query.filter_by(location = location).filter_by(unit = 'c').first()
#     nowInfoF = NowTable.query.filter_by(location = location).filter_by(unit = 'f').first()
#     if nowInfoC is not None:
#         nowInfoC.text = (Info)
#         db.session.add(nowInfoC)
#     if nowInfoF is not None:
#         nowInfoF.text = (Info)
#         db.session.add(nowInfoF)
#     db.session.commit()
#
# def updataNowTableT(location,Info):
#     nowInfoC = NowTable.query.filter_by(location = location).filter_by(unit = 'c').first()
#     nowInfoF = NowTable.query.filter_by(location = location).filter_by(unit = 'f').first()
#     if nowInfoC is not None:
#         nowInfoC.temperature = (Info)
#         db.session.add(nowInfoC)
#     if nowInfoF is not None:
#         nowInfoF.temperature = (Info)
#         db.session.add(nowInfoF)
#     db.session.commit()
#
# def updataNowTableC(location,Info):
#     nowInfoC = NowTable.query.filter_by(location = location).filter_by(unit = 'c').first()
#     nowInfoF = NowTable.query.filter_by(location = location).filter_by(unit = 'f').first()
#     if nowInfoC is not None:
#         nowInfoC.code = (Info)
#         db.session.add(nowInfoC)
#     if nowInfoF is not None:
#         nowInfoF.code = (Info)
#         db.session.add(nowInfoF)
#     db.session.commit()
#
#
# class CityTable(db.Model):
#     __tablename__ = 'citytables'
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(64))
#     # ip = db.Column(db.String(64), unique = True)
#     # cities = db.relationship('NowTable',backref='city')
#
#     def __repr__(self):
#         return '<CityTable %r>' % self.name
#
# def insertCityTable(userInput):
#     city = CityTable.query.filter_by(name = userInput).first()
#     if city is None:
#         city = CityTable(name=userInput)
#     db.session.add(city)
#     db.session.commit()

