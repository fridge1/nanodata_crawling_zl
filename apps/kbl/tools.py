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