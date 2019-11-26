import time,datetime
from datetime import date
from orm_connection.orm_session import MysqlSvr
from orm_connection.orm_tableStruct_basketball import *
import pandas as pd
import requests
import io
from PIL import Image




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



def get_team_id():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueNblBasketballTeam).all()
    data_dict = {row.name_en: row.id for row in rows}
    return data_dict



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
    data_dict = {row.name_en.lower(): row.name_zh for row in rows}
    return data_dict



def translate_text():
    data_tran = pd.read_excel('/root/nanodata_crawling/nbl_league_basketball_game_text.xlsx')
    dup_data_tran = data_tran.drop_duplicates('words_text')
    translate_dict = {}
    key_list = list(dup_data_tran['words_text'])
    value_list = list(dup_data_tran['words_text_zh'])
    for index in range(len(key_list)):
        translate_dict[key_list[index]] = value_list[index]
    return translate_dict


def get_nbl_nana_player_name_zh_1():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueNblBasketballPlayer).all()
    data_dict = {row.id: row.logo for row in rows}
    return data_dict



def download_img(img_url,name,content):
    res = requests.get(img_url)
    byte_stream = io.BytesIO(res.content)
    roiImg = Image.open(byte_stream)
    imgByteArr = io.BytesIO()
    roiImg.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    with open('./' + content + '/' + name + ".png", "wb") as f:
        f.write(imgByteArr)

