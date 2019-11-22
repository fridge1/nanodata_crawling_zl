import time,datetime
from datetime import date
from orm_connection.orm_session import MysqlSvr
from orm_connection.orm_tableStruct_basketball import *
import pymysql
import pandas as pd




def age_timeStamp(birthday):
    time_format = datetime.datetime.strptime(birthday, '%Y-%m-%d')
    timeArray = time.strptime(birthday, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    today = date.today()
    age = today.year - time_format.year - ((today.month, today.day) < (time_format.month, time_format.day))
    return timeStamp,age


def get_player_id(player_en):
    try:
        spx_dev_session = MysqlSvr.get('spider_zl')
        return spx_dev_session.query(BleagueNblBasketballPlayer).filter(BleagueNblBasketballPlayer.name_en==player_en).all()[0].id
    except:
        return 0

def get_team_id(team_name):
    spx_dev_session = MysqlSvr.get('spider_zl')
    team_data = {
        'name_en': team_name,
    }
    _, row = BleagueNblBasketballTeam.upsert(
        spx_dev_session,
        'name_en',
        team_data
    )
    return row.id


def change_bjtime(date):
    time_format = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    timeArray = datetime.datetime.strftime(time_format, '%Y-%m-%d %H:%M:%S')
    timeArray1 = datetime.datetime.strptime(timeArray, '%Y-%m-%d %H:%M:%S')
    bj_time = (timeArray1+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    bj_time1 = datetime.datetime.strptime(bj_time, '%Y-%m-%d %H:%M:%S')
    timeStamp = int(time.mktime(bj_time1.timetuple()))
    return timeStamp


def get_nbl_nana_player_name_zh():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueNblBasketballPlayer).all()
    data_dict = {row.name_en : row.name_zh for row in rows}
    return data_dict

# a = get_nbl_nana_player_name_zh()
# print(a)

def translate_text():
    data_tran = pd.read_excel('/Users/zhulang/Desktop/nbl_league_basketball_game_text(1)(1).xlsx')
    dup_data_tran = data_tran.drop_duplicates('words_text')
    translate_dict = {}
    key_list = list(dup_data_tran['words_text'])
    value_list = list(dup_data_tran['words_text_zh'])
    for index in range(len(key_list)):
        translate_dict[key_list[index]] = value_list[index]
    return translate_dict


