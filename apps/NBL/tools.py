import time, datetime
from datetime import date
from orm_connection.orm_session import MysqlSvr
from orm_connection.orm_tableStruct_basketball import *
import pandas as pd
import requests
import io
from PIL import Image
import pymysql


def age_timeStamp(birthday):
    time_format = datetime.datetime.strptime(birthday, '%Y-%m-%d')
    timeArray = time.strptime(birthday, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    today = date.today()
    age = today.year - time_format.year - ((today.month, today.day) < (time_format.month, time_format.day))
    return timeStamp, age


def get_player_id(player_en):
    try:
        spx_dev_session = MysqlSvr.get('spider_zl')
        return \
        spx_dev_session.query(BleagueNblBasketballPlayer).filter(BleagueNblBasketballPlayer.name_en == player_en).all()[
            0].id
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
    bj_time = (timeArray1 + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    bj_time1 = datetime.datetime.strptime(bj_time, '%Y-%m-%d %H:%M:%S')
    timeStamp = int(time.mktime(bj_time1.timetuple()))
    return timeStamp


def get_nbl_nana_player_name_zh():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueNblBasketballPlayer).all()
    data_dict = {row.name_en.lower(): row.name_zh for row in rows}
    return data_dict


def get_nbl_nana_player_name_zh_1():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueNblBasketballPlayer).all()
    data_dict = {row.id: row.logo for row in rows}
    return data_dict


def download_img(img_url, name, content):
    res = requests.get(img_url)
    byte_stream = io.BytesIO(res.content)
    roiImg = Image.open(byte_stream)
    imgByteArr = io.BytesIO()
    roiImg.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    with open('./' + content + '/' + name + ".png", "wb") as f:
        f.write(imgByteArr)


def get_season_id():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueNblBasketballSeason).all()
    data_list = [row.id for row in rows]
    return data_list


def update_stage_id():
    conn = pymysql.connect(
        host='rm-bp1ov656aj80p2ie8uo.mysql.rds.aliyuncs.com',
        port=3306,
        user='spider_zl',
        password='0EDbIRtu4JPGdiQnu3kvXxiOMDMjejow',
        db='spider_zl',
        charset='utf8mb4'
    )

    cur = conn.cursor()
    select_id = 'select id,season_id from nbl_league_basketball_stage;'
    cur.execute(select_id)
    results = cur.fetchall()
    for result in results:
        update_id = 'update nbl_league_basketball_match set stage_id=%s where season_id=%s;'
        cur.execute(update_id, (result[0], result[1]))
    conn.commit()


def get_player_id_update():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueNblBasketballPlayer).all()
    data_list = [row.id for row in rows]
    return data_list


def get_player_id_position_update():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueNblBasketballPlayer).all()
    data_dict = {row.name_en.lower(): (row.id, row.position) for row in rows}
    return data_dict
