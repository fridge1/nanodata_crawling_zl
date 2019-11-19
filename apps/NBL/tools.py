import time,datetime
from datetime import date
from orm_connection.orm_session import MysqlSvr
from orm_connection.orm_tableStruct_basketball import *

def age_timeStamp(birthday):
    time_format = datetime.datetime.strptime(birthday, '%Y-%m-%d')
    timeArray = time.strptime(birthday, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    today = date.today()
    age = today.year - time_format.year - ((today.month, today.day) < (time_format.month, time_format.day))
    return timeStamp,age


def get_player_id(player_en):
    spx_dev_session = MysqlSvr.get('spider_zl')
    player_data = {
        'name_en':player_en,
    }
    _, row = BleagueNblBasketballPlayer.upsert(
                        spx_dev_session,
                        'name_en',
                        player_data
                    )
    return row.id

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

