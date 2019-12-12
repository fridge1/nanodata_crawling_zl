# -*- encoding=utf-8 -*-
import requests
import json


def dingding_alter(text):  # 程序报警
    url = 'https://oapi.dingtalk.com/robot/send?access_token=adef51bdf91a51103717ba9178986d69eaeff094998671b0bfb819f11d9b9c3d'
    data = {
        'msgtype': 'text',
        'text': {'content': text + '错误'}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(data), headers=headers)
