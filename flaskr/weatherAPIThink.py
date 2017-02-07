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
    cityText = '您在' + city['region'] + city['city']
    return cityText

class fetchWeatherThink(object):
    
    def __init__(self,UNIT,inputLocation):
        self._query_result = {'status':'404', 'message':'无法连接服务器'}
        self.KEY = 'cp3kmxnoxvklla8q'
        self.UNIT = UNIT
        self.inputLocation = inputLocation
#         self.nowDict()
#         self.dailyDict()
    
    def fetchAPIResult(self,API): 

        _query_params = {
                'key': self.KEY,
                'location': self.inputLocation,
                'language': 'zh-Hans',
                'unit': self.UNIT
                }
        result = requests.get(API, params = _query_params) #timeout = 1?

        return result
    
    def nowDict(self):
        '''Real_time weather forecast'''
        API = 'https://api.thinkpage.cn/v3/weather/now.json'
        result = self.fetchAPIResult(API)
        if result.status_code == 200:
            r = result.json()['results'][0]
            self._query_result['status'] = '200'
            self._query_result['message'] = 'yes'
            self._query_result['location'] = r['location']['name']
            self._query_result['text'] = r['now']['text']
            self._query_result['code'] = r['now']['code']
            self._query_result['temperature'] = r['now']['temperature']
            self._query_result['lastUpdate'] = r['last_update']
        else:
            self._query_result = {'status':'502', 'message':'查询不到此城市信息'}

        return self._query_result
    
    def dailyDict(self):
        '''The weather daily'''
        API = 'https://api.thinkpage.cn/v3/weather/daily.json'
        result = self.fetchAPIResult(API)
        if result.status_code == 200:
            r = result.json()['results'][0]
            self._query_result['status'] = '200'
            self._query_result['message'] = 'yes'
            self._query_result['location'] = r['location']['name']
            self._query_result['lastUpdate'] = r['last_update']
            #today
            self._query_result['date_day_d0'] = r['daily'][0]['date']
            self._query_result['text_day_d0'] = r['daily'][0]['text_day']
            self._query_result['text_night_d0'] = r['daily'][0]['text_night']
            self._query_result['code_day_d0'] = r['daily'][0]['code_day']
            self._query_result['code_night_d0'] = r['daily'][0]['code_night']
            self._query_result['low_d0'] = r['daily'][0]['low']
            self._query_result['high_d0'] = r['daily'][0]['high']
            self._query_result['wind_direction_d0'] = r['daily'][0]['wind_direction']
            self._query_result['wind_scale_d0'] = r['daily'][0]['wind_scale']
            #tomorrow
            self._query_result['date_day_d1'] = r['daily'][1]['date']
            self._query_result['text_day_d1'] = r['daily'][1]['text_day']
            self._query_result['text_night_d1'] = r['daily'][1]['text_night']
            self._query_result['code_day_d1'] = r['daily'][1]['code_day']
            self._query_result['code_night_d1'] = r['daily'][1]['code_night']
            self._query_result['low_d1'] = r['daily'][1]['low']
            self._query_result['high_d1'] = r['daily'][1]['high']
            self._query_result['wind_direction_d1'] = r['daily'][1]['wind_direction']
            self._query_result['wind_scale_d1'] = r['daily'][1]['wind_scale']
            #after tomorrow
            self._query_result['date_day_d2'] = r['daily'][2]['date']
            self._query_result['text_day_d2'] = r['daily'][2]['text_day']
            self._query_result['text_night_d2'] = r['daily'][2]['text_night']
            self._query_result['code_day_d2'] = r['daily'][2]['code_day']
            self._query_result['code_night_d2'] = r['daily'][2]['code_night']
            self._query_result['low_d2'] = r['daily'][2]['low']
            self._query_result['high_d2'] = r['daily'][2]['high']
            self._query_result['wind_direction_d2'] = r['daily'][2]['wind_direction']
            self._query_result['wind_scale_d2'] = r['daily'][2]['wind_scale']
        else:
            self._query_result = {'status':'502', 'message':'查询不到此城市信息'}

        return self._query_result
        
    def lifeDict(self):
        '''Fetch life message'''
        API = 'https://api.thinkpage.cn/v3/life/suggestion.json'
        result = self.fetchAPIResult(API)
        if result.status_code == 200:
            r = result.json()['results'][0]
            self._query_result['status'] = '200'
            self._query_result['message'] = 'yes'
            self._query_result['location'] = r['location']['name']
            self._query_result['car_washing'] = r['suggestion']['car_washing']['brief'] # 洗车
            self._query_result['dressing'] = r['suggestion']['dressing']['brief'] #穿衣
            self._query_result['flu'] = r['suggestion']['flu']['brief'] #感冒
            self._query_result['sport'] = r['suggestion']['sport']['brief'] #运动
            self._query_result['travel'] = r['suggestion']['travel']['brief'] #旅行
            self._query_result['uv'] = r['suggestion']['uv']['brief'] #紫外线
            self._query_result['lastUpdate'] = r['last_update']
        else:
            self._query_result = {'status':'502', 'message':'查询不到此城市信息'}

        return self._query_result




















