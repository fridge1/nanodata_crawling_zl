import requests
from lxml import etree
import datetime, time
from datetime import date
from orm_connection.orm_session import MysqlSvr
from orm_connection.acb_basketball import BleagueAcbBasketballPlayer,BleagueAcbBasketballVenue,BleagueAcbBasketballTeam,BleagueAcbBasketballMatch


def tree_parse(res):
    enconding = requests.utils.get_encodings_from_content(res.text)
    html_doc = res.content.decode()
    tree = etree.HTML(html_doc)
    return tree


def change_match_bjtime(time_date):
    time_format = datetime.datetime.strptime(time_date, '%d/%m/%Y')
    timeArray = datetime.datetime.strftime(time_format, '%d/%m/%Y')
    timeArray1 = datetime.datetime.strptime(timeArray, '%d/%m/%Y')
    bj_time = (timeArray1 + datetime.timedelta()).strftime("%Y-%m-%d")
    bj_time1 = datetime.datetime.strptime(bj_time, '%Y-%m-%d')
    timeStamp = int(time.mktime(bj_time1.timetuple()))
    today = date.today()
    age = today.year - time_format.year - ((today.month, today.day) < (time_format.month, time_format.day))
    return timeStamp, age


def get_player_id_short():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueAcbBasketballPlayer).all()
    data_dict = {row.short_name_en.lower(): row.id for row in rows}
    return data_dict

def get_player_id():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueAcbBasketballPlayer).all()
    data_dict = {row.name_en.lower(): row.id for row in rows}
    return data_dict



def change_bjtime(date):
    time_format = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M')
    timeArray = datetime.datetime.strftime(time_format, '%d/%m/%Y %H:%M')
    timeArray1 = datetime.datetime.strptime(timeArray, '%d/%m/%Y %H:%M')
    bj_time = (timeArray1 + datetime.timedelta(hours=7)).strftime("%d/%m/%Y %H:%M")
    bj_time1 = datetime.datetime.strptime(bj_time, '%d/%m/%Y %H:%M')
    timeStamp = int(time.mktime(bj_time1.timetuple()))
    return timeStamp

def get_venue_id():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueAcbBasketballVenue).all()
    data_dict = {row.name_en: row.id for row in rows}
    return data_dict

def get_team_id():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueAcbBasketballTeam).all()
    data_dict = {row.short_name_en.lower().strip(): row.id for row in rows}
    return data_dict


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

def get_player_id_upsert(player_upsert):
    spx_dev_session = MysqlSvr.get('spider_zl')
    _, row = BleagueAcbBasketballPlayer.upsert(
        spx_dev_session,
        'name_en',
        player_upsert
    )
    return row.id

def get_acb_player_name_short():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueAcbBasketballPlayer).all()
    data_dict = {row.short_name_en: row.name_zh for row in rows}
    return data_dict

def get_acb_player_name_en():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueAcbBasketballPlayer).all()
    data_dict = {row.name_en: row.name_zh for row in rows}
    return data_dict

def get_player_id_position_update():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueAcbBasketballPlayer).all()
    data_dict = {row.short_name_en.lower(): (row.id, row.position) for row in rows}
    return data_dict


def get_match_id_start():
    spx_dev_session = MysqlSvr.get('spider_zl')
    b = time.strftime("%Y-%m-%d 23:59:59", time.localtime())
    bj_time2 = datetime.datetime.strptime(b, '%Y-%m-%d %H:%M:%S')
    timeStamp1 = int(time.mktime(bj_time2.timetuple()))
    rows = spx_dev_session.query(BleagueAcbBasketballMatch).filter(BleagueAcbBasketballMatch.status_id == 1,
                                                                   BleagueAcbBasketballMatch.match_time <= timeStamp1).all()
    data_dict = {row.open_id: row.id for row in rows}
    return data_dict