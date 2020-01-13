# coding:utf-8
from orm_connection.orm_session import MysqlSvr
from orm_connection.tennis import TennisPlayerInfoSingleRank, TennisPlayerInfoDoubleRank, TennisCity, TennisCountry, \
    TennisPlayer
import requests
from lxml import etree
import unicodedata
import datetime
import time
from datetime import date
import redis
import random


def replace_text(text):
    list1 = []
    for i in text.lower():
        if 97 <= ord(i) <= 122 or 65 <= ord(i) <= 90:
            list1.append(i)
        else:
            list1.append('-')
    a = '-'.join((''.join(list1)).split('-')).replace('--', '-')
    return a


def get_en_name(data):
    return str(unicodedata.normalize('NFKD', data).encode('ascii', 'ignore'), encoding='utf-8')


def tree_parse(res):
    enconding = requests.utils.get_encodings_from_content(res.text)
    html_doc = res.content.decode()
    tree = etree.HTML(html_doc)
    return tree


def time_stamp(time_date):
    if time_date != 'N/A':
        time_format = datetime.datetime.strptime(time_date, '%Y-%m-%d')
        timeArray = datetime.datetime.strftime(time_format, '%Y-%m-%d')
        timeArray1 = datetime.datetime.strptime(timeArray, '%Y-%m-%d')
        bj_time = (timeArray1 + datetime.timedelta()).strftime("%Y-%m-%d")
        bj_time1 = datetime.datetime.strptime(bj_time, '%Y-%m-%d')
        timeStamp = int(time.mktime(bj_time1.timetuple()))
        today = date.today()
        age = today.year - time_format.year - ((today.month, today.day) < (time_format.month, time_format.day))
        return timeStamp, age
    else:
        return 0, 0


def get_city_id():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(TennisCity).all()
    city_id_dict = {}
    for row in rows:
        city_id_dict[row.name_en] = row.id
    return city_id_dict


def competition_time_stamp(time_date):
    time_format = datetime.datetime.strptime(time_date, '%Y-%m-%d')
    timeArray = datetime.datetime.strftime(time_format, '%Y-%m-%d')
    timeArray1 = datetime.datetime.strptime(timeArray, '%Y-%m-%d')
    bj_time = (timeArray1 + datetime.timedelta()).strftime("%Y-%m-%d")
    bj_time1 = datetime.datetime.strptime(bj_time, '%Y-%m-%d')
    timeStamp = int(time.mktime(bj_time1.timetuple()))
    return timeStamp


def get_country_id():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(TennisCountry).all()
    country_id_dict = {}
    for row in rows:
        country_id_dict[row.name_en] = row.id
    return country_id_dict


def upsert_city(city_name):
    session = MysqlSvr.get('spider_zl')
    data = {
        'name_en': city_name
    }
    _, row = TennisCity.upsert(
        session,
        'name_en',
        data
    )
    return row.id


def upsert_country(country_name):
    session = MysqlSvr.get('spider_zl')
    data = {
        'name_en': country_name
    }
    _, row = TennisCountry.upsert(
        session,
        'name_en',
        data
    )
    return row.id


def safe_get(obj, key, default=0):
    keys = key.split('.')

    def _get(_obj, _keys):
        if not _obj or not _keys or not isinstance(_obj, dict):
            return default

        if len(_keys) == 1:
            return _obj.get(_keys[0], default)
        else:
            return _get(_obj.get(_keys[0]), _keys[1:])

    return _get(obj, keys)


def change_match_bjtime(time_date):
    time_format = datetime.datetime.strptime(time_date, '%Y-%m-%d %H:%M:%S')
    timeArray = datetime.datetime.strftime(time_format, '%Y-%m-%d %H:%M:%S')
    timeArray1 = datetime.datetime.strptime(timeArray, '%Y-%m-%d %H:%M:%S')
    bj_time = (timeArray1 + datetime.timedelta()).strftime("%Y-%m-%d %H:%M:%S")
    bj_time1 = datetime.datetime.strptime(bj_time, '%Y-%m-%d %H:%M:%S')
    timeStamp = int(time.mktime(bj_time1.timetuple()))
    return timeStamp


def rank_match_bjtime(time_date):
    time_format = datetime.datetime.strptime(time_date, '%Y-%m-%d')
    timeArray = datetime.datetime.strftime(time_format, '%Y-%m-%d')
    timeArray1 = datetime.datetime.strptime(timeArray, '%Y-%m-%d')
    bj_time = (timeArray1 + datetime.timedelta()).strftime("%Y-%m-%d")
    bj_time1 = datetime.datetime.strptime(bj_time, '%Y-%m-%d')
    timeStamp = int(time.mktime(bj_time1.timetuple()))
    return timeStamp


def get_last_week_date(time_date):
    time_format = datetime.datetime.strptime(time_date, '%Y-%m-%d')
    delta = datetime.timedelta(days=-7)
    n_days = time_format + delta
    return n_days.strftime('%Y-%m-%d')
