import requests
from lxml import etree
import re
import datetime,time
from datetime import date
from orm_connection.orm_session import MysqlSvr
from orm_connection.kbl_basketball import *

def tree_parse(res):
    enconding = requests.utils.get_encodings_from_content(res.text)
    html_doc = res.content.decode(enconding[0])
    tree = etree.HTML(html_doc)
    return tree

def age_timeStamp(birthday):
    time_format = datetime.datetime.strptime(birthday, '%Y-%m-%d')
    timeArray = time.strptime(birthday, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    today = date.today()
    age = today.year - time_format.year - ((today.month, today.day) < (time_format.month, time_format.day))
    return timeStamp,age


def get_school_id(school_key):
    spx_dev_session = MysqlSvr.get('spider_zl')
    school_data = {
        'key':school_key,
        'name_en':school_key,
    }
    _, row = BleagueNblBasketballSchool.upsert(
                        spx_dev_session,
                        'key',
                        school_data
                    )
    return row.id


def get_manager_id(manager_key,team_id,assistant):
    spx_dev_session = MysqlSvr.get('spider_zl')
    manager_data = {
        'key':manager_key,
        'name_en':manager_key,
        'team_id':team_id,
        'assistant':assistant,
        'sport_id':2,
    }
    _, row = BleagueNblBasketballManager.upsert(
                        spx_dev_session,
                        'key',
                        manager_data
                    )
    return row.id


def get_city_id(city_key):
    spx_dev_session = MysqlSvr.get('spider_zl')
    city_data = {
        'key':city_key,
        'name_en':city_key,
    }
    _, row = BleagueNblBasketballCity.upsert(
                        spx_dev_session,
                        'key',
                        city_data
                    )
    return row.id


def change_bjtime(date):
    time_format = datetime.datetime.strptime(date, '%Y%m%d%H:%M')
    timeArray = datetime.datetime.strftime(time_format, '%Y.%m.%d %H:%M')
    timeArray1 = datetime.datetime.strptime(timeArray, '%Y.%m.%d %H:%M')
    bj_time = (timeArray1+datetime.timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M")
    bj_time1 = datetime.datetime.strptime(bj_time, '%Y-%m-%d %H:%M')
    timeStamp = int(time.mktime(bj_time1.timetuple()))
    return timeStamp


def get_team_id(team_name):
    try:
        spx_dev_session = MysqlSvr.get('spider_zl')
        return spx_dev_session.query(BleagueNblBasketballTeam).filter(BleagueNblBasketballTeam.name_en.like('%%'+team_name+'%%')).all()[0].id
    except:
        return 0


import cv2

img = cv2.imread("/Users/zhulang/Downloads/92c24f1024ae6883be76ca14fd1c43ceL1.png")
cropped = img[0:220, 150:450]  # 裁剪坐标为[y0:y1, x0:x1]
cv2.imwrite("92c24f1024ae6883be76ca14fd1c43ceL1.png", cropped)
