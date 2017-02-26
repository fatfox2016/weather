# -*- coding: utf-8 -*-
import requests
import re
from main.APIThink import APIT
# nowAPI,lifeAPI,dailyAPI,ipAPI,cityAPI,KEY,Language,TIMEOUT,METRIC,BRITISH


def ipCity():
    ipResult = requests.get(APIT.ipAPI)
    ip = re.search(r'\d+\.\d+\.\d+\.\d+', ipResult.text).group(0)
    cityUrl = APIT.cityAPI + ip
    cityResult = requests.get(cityUrl)
    city = cityResult.json()['data']
    cityText = city['region'] + city['city'] + 'ip:' + ip
    return cityText

class ThinkAPI(object):
    def __init__(self,api):
        self.api = api
        self.KEY = APIT.KEY
        self.language = APIT.Language
        self.timeout = APIT.TIMEOUT

    def fetchAPIResult(self,params):
        error = None
        try:
            r = requests.get(self.api, params = params,timeout=self.timeout)
            if r.status_code == 200:
                data = r.json()['results'][0]
                return data

        except(requests.Timeout,requests.ConnectionError):
            error = 'API loser!'
            return error

    def chooseUnit(self,unit):
        _unit_Dict = {}
        if unit == APIT.BRITISH:
            temperatureUnit = 'f'
            windUnit = 'mph'
        else:
            temperatureUnit = 'c'
            windUnit = 'km/h'
        _unit_Dict['temperatureUnit'] = temperatureUnit
        _unit_Dict['windUnit'] = windUnit
        return _unit_Dict

class NowData(ThinkAPI):

    def __init__(self):
        super().__init__(APIT.nowAPI)

    def fetchNow(self,location,unit):
        params = {'key': self.KEY,
                'location': location,
                'language': self.language,
                'unit': unit}
        data = self.fetchAPIResult(params)
        if isinstance(data, dict):  #判断data的类型是不是字典
            if location == data['location']['name']:
                data['unit'] = params['unit']
                return data
        else:
            error = '找不到{}的信息'.format(location)
            return error

    def nowData(self,data):
        '''Real_time weather forecast'''
        N = {}
        if isinstance(data, dict):
            units = self.chooseUnit(data['unit'])
            N['location'] = data['location']['name']
            N['lastUpdate'] = data['last_update']
            N['text'] = data['now']['text']
            N['temperature'] = data['now']['temperature']
            N['temperatureUnit'] = units['temperatureUnit']
            N['code'] = data['now']['code']
        return N

class LifeData(ThinkAPI):
    def __init__(self):
        super().__init__(APIT.lifeAPI)

    def fetchLife(self,location):
        params = {'key': self.KEY,
                'location': location,
                'language': self.language}
        data = self.fetchAPIResult(params)
        if isinstance(data, dict):
            if location == data['location']['name']:
                return data
        else:
            error = '找不到{}的信息'.format(location)
            return error

    def lifeData(self,data):
        '''Fetch life message'''
        L = {}
        L['location'] = data['location']['name']
        suggestion = data['suggestion']
        for k,v in suggestion.items():
            L[k] = v['brief']
        return L

class DailyData(ThinkAPI):
    def __init__(self):
        super().__init__(APIT.dailyAPI)

    def fetchDaily(self,location,unit):
        params = {'key': self.KEY,
                'location': location,
                'language': self.language,
                'unit': unit}
        data = self.fetchAPIResult(params)
        if isinstance(data, dict):
            if location == data['location']['name']:
                data['unit'] = params['unit']
                return data
        else:
            error = '找不到{}的信息'.format(location)
            return error

    def dailyData(self,data):
        '''The weather daily'''
        D = []
        units = self.chooseUnit(data['unit'])
        for i in range(3):
            daily = data['daily'][i]
            daily['location'] = data['location']['name']
            daily['temperatureUnit'] = units['temperatureUnit']
            daily['windUnit'] = units['windUnit']
            daily['day'] = str(i)
            D.append(daily)
            # for k,v in daily.items():
            #     k = k + str(i)
            #     D[k] = v

        return D

# if __name__ == '__main__':
#
#     data = DailyData().fetchDaily('阜阳','c')
#     a = DailyData().dailyData(data)
#     print(a)