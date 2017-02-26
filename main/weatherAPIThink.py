'''
import json
import sys
import requests
from utils.const_value import API, KEY, UNIT, LANGUAGE
from utils.helper import getLocation


def fetchWeather(location):
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT
    }, timeout=1)
    return result.text

if __name__ == '__main__':
    location = getLocation()
    result = fetchWeather(location)
    print(result)


{
  "results": [{
  "location": {
      "id": "C23NB62W20TF",
      "name": "西雅图",
      "country": "US",
      "timezone": "America/Los_Angeles",
      "timezone_osffset": "-07:00"
  },
  "now": {
      "text": "多云", //天气现象文字
      "code": "4", //天气现象代码
      "temperature": "14", //温度，单位为c摄氏度或f华氏度
      "feels_like": "14", //体感温度，单位为c摄氏度或f华氏度
      "pressure": "1018", //气压，单位为mb百帕或in英寸
      "humidity": "76", //相对湿度，0~100，单位为百分比
      "visibility": "16.09", //能见度，单位为km公里或mi英里
      "wind_direction": "西北", //风向文字
      "wind_direction_degree": "340", //风向角度，范围0~360，0为正北，90为正东，180为正南，270为正西
      "wind_speed": "8.05", //风速，单位为km/h公里每小时或mph英里每小时
      "wind_scale": "2", //风力等级，请参考：http://baike.baidu.com/view/465076.htm
      "clouds": "90", //云量，范围0~100，天空被云覆盖的百分比 #目前不支持中国城市#
      "dew_point": "-12" //露点温度，请参考：http://baike.baidu.com/view/118348.htm #目前不支持中国城市#
  },
  "last_update": "2015-09-25T22:45:00-07:00" //数据更新时间（该城市的本地时间）
  }]
}
'''

# -*- coding: utf-8 -*-
import requests
import re

def getText(fileName):
    '''获取文档内容'''
    with open(fileName,'r',encoding = "utf8") as file:
      text = file.read()   #输出文档
    return text

def ipCity():
    ipUrl = 'http://pv.sohu.com/cityjson?ie = utf-8'
    ipResult = requests.get(ipUrl)
    ip = re.search(r'\d+\.\d+\.\d+\.\d+', ipResult.text).group(0)
    cityUrl = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + ip
    cityResult = requests.get(cityUrl)
    city = cityResult.json()['data']
    cityText = city['region'] + city['city'] + 'ip:' + ip
    return cityText

class fetchWeatherThink(object):

    def __init__(self,UNIT,inputLocation):
        self._query_result = {'status':'404'}
        self.KEY = 'cp3kmxnoxvklla8q'
        self.UNIT = UNIT
        self.inputLocation = inputLocation

    def fetchAPIResult(self,API):
        _query_params = {
                'key': self.KEY,
                'location': self.inputLocation,
                'language': 'zh-Hans',
                'unit': self.UNIT
                }
        result = requests.get(API, params = _query_params)
        return result

    def nowDict(self):
        '''Real_time weather forecast'''
        API = 'https://api.thinkpage.cn/v3/weather/now.json'
        result = self.fetchAPIResult(API)
        if result.status_code == 200:
            r = result.json()['results'][0]
            self._query_result['status'] = '200'
            self._query_result['location'] = r['location']['name']
            self._query_result['lastUpdate'] = r['last_update']
            now = r['now']
            for k,v in now.items():
                self._query_result[k] = v
        else:
            self._query_result = {'status':'502'}

        return self._query_result

    def dailyDict(self):
        '''The weather daily'''
        API = 'https://api.thinkpage.cn/v3/weather/daily.json'
        result = self.fetchAPIResult(API)
        if result.status_code == 200:
            r = result.json()['results'][0]
            self._query_result['status'] = '200'
            self._query_result['location'] = r['location']['name']
            self._query_result['lastUpdate'] = r['last_update']
            for i in range(3):
                daily = r['daily'][i]
                for k,v in daily.items():
                    k = k + str(i)
                    self._query_result[k] = v
        else:
            self._query_result = {'status':'502'}
        return self._query_result

    def lifeDict(self):
        '''Fetch life message'''
        API = 'https://api.thinkpage.cn/v3/life/suggestion.json'
        result = self.fetchAPIResult(API)
        if result.status_code == 200:
            r = result.json()['results'][0]
            self._query_result['status'] = '200'
            self._query_result['location'] = r['location']['name']
            self._query_result['lastUpdate'] = r['last_update']
            suggestion = r['suggestion']
            for k,v in suggestion.items():
                self._query_result[k] = v['brief']
        else:
            self._query_result = {'status':'502'}
        return self._query_result