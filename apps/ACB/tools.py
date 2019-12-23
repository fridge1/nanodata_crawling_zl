import requests
from lxml import etree
import datetime,time
from datetime import date
from orm_connection.orm_session import MysqlSvr
from orm_connection.acb_basketball import BleagueAcbBasketballPlayer

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
    return timeStamp,age


def get_player_id():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueAcbBasketballPlayer).all()
    data_dict = {row.short_name_en: row.id for row in rows}
    return data_dict

print(get_player_id())
