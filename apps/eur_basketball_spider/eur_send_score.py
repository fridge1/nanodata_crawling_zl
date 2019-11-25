import requests
from apps.eur_basketball_spider.tools import tree_parse,change_bjtime,get_team_id,seasons,stage_id
import re
import json
from orm_connection.orm_session import MysqlSvr
from orm_connection.eur_basketball import *
import time
import threading
import traceback
from common.libs.log import LogMgr
logger = LogMgr.get('eur_basketball_match_live')



def match_end(gamecode):
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
    spx_dev_session = MysqlSvr.get('spider_zl')
    season_id = 2019
    sport_id = 2
    match_id = seasons[str(season_id)+'-'+str(season_id+1)]
    while True:
        time.sleep(10)
        match = {}
        box_url = 'https://www.euroleague.net/main/results/showgame?gamecode=%s&seasoncode=E%s' % (gamecode, season_id)
        box_url_res = requests.get(box_url, headers=headers)
        if box_url_res.status_code == 200:
            box_url_tree = tree_parse(box_url_res)
            date = box_url_tree.xpath('//div[@class="date cet"]/text()')[0]
            match_time = change_bjtime(date)
            box_api_url = 'https://live.euroleague.net/api/Boxscore?gamecode=%s&seasoncode=E%s&disp=' % (
            gamecode, season_id)
            home_team_url = box_url_tree.xpath('//div[@class="team local "]/a/@href|//div[@class="team local winner"]/a/@href')[0]
            away_team_url = box_url_tree.xpath('//div[@class="team road "]/a/@href|//div[@class="team road winner"]/a/@href')[0]
            home_team_key = re.findall(r'clubcode=(.*?)&',home_team_url)[0]
            away_team_key = re.findall(r'clubcode=(.*?)&',away_team_url)[0]
            home_team_id = get_team_id(home_team_key)
            away_team_id = get_team_id(away_team_key)
            box_api_res = requests.get(box_api_url, headers=headers)
            if box_api_res.text == '':
                logger.info(box_api_url)
                logger.info('比赛未开始...')
            else:
                box_api_dict = json.loads(box_api_res.text)
                key_list = list(box_api_dict['ByQuarter'][0].keys())[1:]
                home_scores = []
                away_scores = []
                for key in key_list:
                    home_scores.append(box_api_dict['ByQuarter'][0][key])
                    away_scores.append(box_api_dict['ByQuarter'][1][key])
                home_score = box_api_dict['EndOfQuarter'][0][key_list[-1]]
                away_score = box_api_dict['EndOfQuarter'][1][key_list[-1]]
                if box_api_dict['Live'] == False:
                    status_id = 10
                    match['sport_id'] = sport_id
                    match['season_id'] = season_id
                    match['home_team_id'] = home_team_id
                    match['away_team_id'] = away_team_id
                    match['match_time'] = match_time
                    match['home_score'] = home_score
                    match['away_score'] = away_score
                    match['home_scores'] = str(home_scores).replace(']','') + ', ' + str(home_score) + ']'
                    match['away_scores'] = str(away_scores).replace(']','') + ', ' + str(away_score) + ']'
                    match['status_id'] = status_id
                    match['match_id'] = int(str(match_id) + '0000') + int(gamecode)
                    BleaguejpBasketballMatch.upsert(
                        spx_dev_session,
                        'id',
                        match
                    )
                    logger.info(match)
    spx_dev_session.close()

data = {
    'sport_id': 2,
    'site': 'bt',
    'matches': {
        match_id: {
            'score': {
                'tmr': {'ticking': 0, 'coundown': 1, 'addtime': 0, 'second': match_time},
                'status_id': status_id,
                'home_scores': home_scores,
                'away_scores': away_scores,
            }
        }
    }
}

def run():
    while True:
        match_end()
        time.sleep(7200)






