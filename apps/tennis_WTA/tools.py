# coding:utf-8
from orm_connection.orm_session import MysqlSvr
from orm_connection.tennis import TennisPlayerInfoSingleRank,TennisPlayerInfoDoubleRank,TennisCity
import requests
from lxml import etree
import unicodedata
import datetime
import time
from datetime import date


def replace_text(text):
    list1 = []
    for i in text.lower():
        if 97 <= ord(i) <= 122 or 65 <= ord(i) <= 90:
            list1.append(i)
        else:
            list1.append('-')
    a = '-'.join((''.join(list1)).split('-'))
    return a

def get_en_name(data):
    return str(unicodedata.normalize('NFKD', data).encode('ascii', 'ignore'), encoding='utf-8')

def get_single_player_id():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(TennisPlayerInfoSingleRank).all()
    single_player_id_name = {}
    for row in rows:
        single_player_id_name[row.player_id] = replace_text(row.name_en)
    return single_player_id_name


def get_double_player_id():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(TennisPlayerInfoDoubleRank).all()
    double_player_id_name = {}
    for row in rows:
        double_player_id_name[row.player_id] = replace_text(row.name_en)
    return double_player_id_name

def tree_parse(res):
    enconding = requests.utils.get_encodings_from_content(res.text)
    html_doc = res.content.decode(enconding[0])
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

def get_player_single_name():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(TennisPlayerInfoSingleRank).all()
    single_player_id_name = {}
    for row in rows:
        single_player_id_name[row.player_id] = row.name_en
    return single_player_id_name


def get_player_double_name():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(TennisPlayerInfoDoubleRank).all()
    double_player_id_name = {}
    for row in rows:
        double_player_id_name[row.player_id] = row.name_en
    return double_player_id_name