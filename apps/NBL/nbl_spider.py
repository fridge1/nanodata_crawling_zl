import requests
from apps.NBL.tools import age_timeStamp
import traceback
import json, time
from orm_connection.orm_session import MysqlSvr
from orm_connection.orm_tableStruct_basketball import *
from apps.NBL.tools import get_player_id_update
from apps.send_error_msg import dingding_alter
from common.libs.log import LogMgr

logger = LogMgr.get('nbl_basketball_player_team_info_live')


def player_info():
    headers = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    }
    player_ids = get_player_id_update()
    url = 'https://api.nbl.com.au/_/custom/api/genius?route[0]=competitions/24346/teams/3682/persons&route[1]=competitions/24346/teams/3709/persons&route[2]=competitions/24346/teams/3713/persons&route[3]=competitions/24346/teams/3716/persons&route[4]=competitions/24346/teams/7694/persons&route[5]=competitions/24346/teams/3684/persons&route[6]=competitions/24346/teams/3692/persons&route[7]=competitions/24346/teams/113805/persons&route[8]=competitions/24346/teams/3694/persons&filter[owner]=nbl'
    player_res = requests.get(url, headers=headers)
    player_dict = json.loads(player_res.text)
    datas = player_dict['data']
    player_ids_update = []
    for data in datas:
        id = data['personId']
        player_ids_update.append(id)
        sport_id = 2
        team_id = data['primaryTeamId']
        name_en = data['firstName'] + ' ' + data['familyName']
        try:
            logo = data['images']['photo']['L1']['url']
        except:
            logo = ''
        try:
            birthday, age = age_timeStamp(data['dob'])
        except:
            birthday, age = 0, 0
        weight = data['weight']
        height = data['height']
        short_name_en = data['nickName']
        shirt_number = data['defaultShirtNumber']
        nationality = data['nationality']
        position = data['defaultPlayingPosition']
        data = {
            'id': id,
            'sport_id': sport_id,
            'team_id': team_id,
            'name_en': name_en,
            'logo': logo,
            'birthday': birthday,
            'age': age,
            'weight': weight,
            'height': height,
            'short_name_en': short_name_en,
            'shirt_number': shirt_number,
            'nationality': nationality,
            'position': position,
        }
        print('player_info %s' % data)
        spx_dev_session = MysqlSvr.get('spider_zl')
        BleagueNblBasketballPlayer.upsert(
            spx_dev_session,
            'id',
            data
        )
        logger.info('data:', data)
    for player_id in player_ids:
        if player_id not in player_ids_update:
            update_data = {
                'id': player_id,
                'deleted': 1
            }
            spx_dev_session = MysqlSvr.get('spider_zl')
            BleagueNblBasketballPlayer.upsert(
                spx_dev_session,
                'id',
                update_data
            )
            logger.info('update_data:', update_data)


def team_info():
    headers = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    }
    url = 'https://api.nbl.com.au/_/custom/api/genius?route=competitions/24346/teams&filter[owner]=nbl'
    team_res = requests.get(url, headers=headers)
    team_dict = json.loads(team_res.text)
    datas = team_dict['data']
    for data in datas:
        id = data['teamId']
        sport_id = 2
        name_en = data['teamName']
        try:
            logo = data['images']['logo']['S1']['url']
        except:
            logo = ''
        short_name_en = data['teamNickname']
        data = {
            'id': id,
            'sport_id': sport_id,
            'name_en': name_en,
            'logo': logo,
            'short_name_en': short_name_en,
        }
        logger.info(data)
        spx_dev_session = MysqlSvr.get('spider_zl')
        BleagueNblBasketballTeam.upsert(
            spx_dev_session,
            'id',
            data
        )


def run():
    try:
        while True:
            player_info()
            team_info()
            time.sleep(3600)
    except:
        dingding_alter(traceback.format_exc())
        logger.error(traceback.format_exc())
