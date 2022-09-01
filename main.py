'''
@Time    : 2022/8/27 7:59
@Author  : Yangtengfei
@FileName: 公众号推送天气.py
@Software: PyCharm
'''
'''
------目前需要改进的最大问题是：修改重复调用函数的问题(函数传参)，及添加多人推送功能------
'''
import json
import requests
import datetime
import random
import re

#和风天气开发平台https://dev.qweather.com/
#和风天气的API官方文档https://dev.qweather.com/docs/api/
#我的和风天气的API的KEY，详见和风天气控制台应用管理https://console.qweather.com/#/apps

mykey='8837beb64f254393b322c7aa376d2fb1'    #此处填写自己申请的和风天气API的KEY
KICT = '南乐'
appID = 'wxe3ed1b0c79453a03'  # 微信测试平台appid
appsecret = "952e8d326e84376d2fc166701ba407dd"   # 微信测试平台appsecret
# User = 'oNcUE6Y-TFW4FuSssf6RPij8IO1M' #微信测试平台用户列表微信号  （猪的）
User = 'oNcUE6fn2XfpoFdF9AKO_LUotkvo' # 我自己的
# User = 'oNcUE6aRBND_V9U4tsbbO8QpIzsM' ##岗的
Message_id = '_EJihrh7WzcCNg_aEs_U5dNOc8zOlFMcItiXbYDVhAw' #微信测试平台模板消息接口ID
mss = '猪猪公主，早上好！'
week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]

#城市ID号详见  https://cdn.heweather.com/china-city-list.txt    编码Unicode（UTF-8）

def CityID():
    with open("./CityId.txt", "r",encoding="gbk") as f:  #本地可以不加解码，本地是utf-8，这里只能是gbk
        a = f.readlines()
        for i in a:
            if KICT in i:
                city1 = re.sub(" ", "", i)
                city2 = city1.replace('|', ',')
                city3 = re.search(',(.*?),.*?', city2)
                cityid = re.sub(',', "", city3.group())
                print(cityid)
                return cityid

## 和风天气官方 城市ID API接口（每天超过次数要钱）
## url1 = f'https://geoapi.qweather.com/v2/city/lookup?location={CityID()}&key='+mykey
#查询实时天气
url2 = 'https://devapi.qweather.com/v7/weather/now?location='+CityID()+'&key=' + mykey
#查询3天预报
url3 = 'https://devapi.qweather.com/v7/weather/3d?location='+CityID()+'&key=' + mykey
## 空气质量查询
url4 = 'https://devapi.qweather.com/v7/air/now?location='+CityID()+'&key=' + mykey
## 穿衣指数，舒适指数，感冒指数
url5 = f'https://devapi.qweather.com/v7/indices/1d?type=3,8,9&location={CityID()}&key={mykey}'
##情话
url6 = 'https://api.uomg.com/api/rand.qinghua'


def Temperature_Now():    #查询实时天气
    f = requests.get(url2)
    jsons = json.loads(f.text)
    result1 = jsons['now']
    return result1


def Temperature_3Day():    #查询3天预报
    f = requests.get(url3)
    jsons = json.loads(f.text)
    result2 = jsons['daily']  #此处为3个字典组成一个列表
    return result2[0]


def AirQuality_Now():    #查询实时空气质量
    f = requests.get(url4)
    #print(f.text)
    jsons = json.loads(f.text)
    result3 = jsons['now']
    return result3


def sHzs():
    dicts = {}
    num = [0,1,2]
    f = requests.get(url5)
    jsons = json.loads(f.text)
    result4 = jsons['daily']
    # print(result4)
    for i,r in zip(num,result4):
        dicts.update({i:r})
    # print(dicts[0]['name']) ## 结果 穿衣指数
    return dicts

## 如果爱不疯狂就不是爱了。
def Qh():
    f = requests.get(url6)
    f.encoding=f.apparent_encoding
    result = f.json()
    return result['content']

def datatime():
    current = datetime.datetime.now().strftime('%Y-%m-%d')
    return current

def randomcolor(): ## 随机颜色
    colorarr =['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorarr[random.randint(0,14)]
    return "#"+color

def message():  ##信息模板
    return {
        "touser": User,
        "template_id": Message_id,
        "topcolor": "#FF0000",
        # json数据对应模板
        "data": {
            "first": {
                "value": mss,
                # 字体颜色
                "color": "#FF0000"
            },
            "word1": { ## 时间+星期几
                "value": str(datatime())+' '+week_list[datetime.datetime.now().weekday()],
                "color": randomcolor()
            },
            "citydata": { ## 城市天气状态
                "value": "南乐"+" "+Temperature_Now()['text'],
                "color": randomcolor()
            },
            "word2": {  ## 目前温度
                "value": Temperature_Now()['temp']+"度",
                "color": randomcolor()
            },
            "word3":{  ## 当天最高温
                "value": Temperature_3Day()['tempMax']+"度",
                "color": "#FF0000"  # 红色
            },
            "word4":{ ## 最低温
                "value": Temperature_3Day()['tempMin']+"度",
                "color": "#87CEFA"  # 浅蓝色
            },
            "word5":{  ## 风向
                "value": Temperature_Now()['windDir'],
                "color": randomcolor()
            },
            "word6":{  ## 风力等级
                "value": Temperature_3Day()['windScaleDay']+"级",
                "color": randomcolor()
            },
            "word7":{  ## 空气质量
                "value": AirQuality_Now()['category'],
                "color": "#173177"
            },
            "word8":{  ## 穿衣建议
                "value": sHzs()[0]['text'],
                "color": randomcolor()
            },
            # "data":{
            #     "value": str(datetime.datetime.now().strftime('%Y-%m-%d'))+' '+week_list[datetime.datetime.now().weekday()],
            #     "color": "#173177"
            # },
            "word9":{  ## 情话
                "value": Qh(),
                "color": randomcolor()
            },
        }
    }

json_data = {"标题":mss,"时间":str(datetime.datetime.now().strftime('%Y-%m-%d'))+' '+week_list[datetime.datetime.now().weekday()],
             "天气":"南乐"+" "+Temperature_Now()['text'],"当前温度" : Temperature_Now()['temp']+"度","最高温":Temperature_3Day()['tempMax']+"度",
             "最低温":Temperature_3Day()['tempMin']+"度","风向":Temperature_Now()['windDir'],"风力等级":Temperature_3Day()['windScaleDay']+"级",
             "空气质量":AirQuality_Now()['category'],"穿衣建议":sHzs()[0]['text'],"情话":Qh()}

def Accesstoken():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appID}&secret={appsecret}"
    resp = requests.get(url)
    result = resp.json()
    if 'access_token' in result:
        return result['access_token']
    else:
        return result

def send_message():
    url=f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={Accesstoken()}"
    data=json.dumps(message())
    resp= requests.post(url,data=data)
    result=resp.json()
    if result["errcode"]==0:
        return("发送成功")
    else:
        return("发送失败")


def main(): ##云函数入口
#     print(json_data)
    return send_message()

if __name__ == '__main__':
    main()
