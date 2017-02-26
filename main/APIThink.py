
class APIT(object):
    nowAPI = 'https://api.thinkpage.cn/v3/weather/now.json'
    lifeAPI = 'https://api.thinkpage.cn/v3/life/suggestion.json'
    dailyAPI = 'https://api.thinkpage.cn/v3/weather/daily.json'
    KEY = 'cp3kmxnoxvklla8q'
    Language = 'zh-Hans'
    METRIC = 'c'
    BRITISH = 'f'
    TIMEOUT = 20

class IPC(object):
    ipAPI = 'http://pv.sohu.com/cityjson?ie = utf-8'
    cityAPI = 'http://ip.taobao.com/service/getIpInfo.php?ip='


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

{
  "results": [{
    "location": {
      "id": "WX4FBXXFKE4F",
      "name": "北京",
      "country": "CN",
      "path": "北京,北京,中国",
      "timezone": "Asia/Shanghai",
      "timezone_offset": "+08:00"
    },
    "daily": [{                         //返回指定days天数的结果
      "date": "2015-09-20",             //日期
      "text_day": "多云",               //白天天气现象文字
      "code_day": "4",                  //白天天气现象代码
      "text_night": "晴",               //晚间天气现象文字
      "code_night": "0",                //晚间天气现象代码
      "high": "26",                     //当天最高温度
      "low": "17",                      //当天最低温度
      "precip": "0",                    //降水概率，范围0~100，单位百分比
      "wind_direction": "",             //风向文字
      "wind_direction_degree": "255",   //风向角度，范围0~360
      "wind_speed": "9.66",             //风速，单位km/h（当unit=c时）、mph（当unit=f时）
      "wind_scale": ""                  //风力等级
    }, {
      "date": "2015-09-21",
      "text_day": "晴",
      "code_day": "0",
      "text_night": "晴",
      "code_night": "0",
      "high": "27",
      "low": "17",
      "precip": "0",
      "wind_direction": "",
      "wind_direction_degree": "157",
      "wind_speed": "17.7",
      "wind_scale": "3"
    }, {
      ...                               //更多返回结果
    }],
    "last_update": "2015-09-20T18:00:00+08:00" //数据更新时间（该城市的本地时间）
  }]
}
'''