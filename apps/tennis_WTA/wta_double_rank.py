import aiohttp
import asyncio
import requests
import threading
from aiohttp import ClientSession
from orm_connection.orm_session import MysqlSvr
from orm_connection.tennis import TennisPlayerInfoDoubleRank
import json
from common.libs.log import LogMgr

logger = LogMgr.get('wta_tennis_double_rank')



class GetRankInfo(object):
    def __init__(self):
        self.session = MysqlSvr.get('spider_zl')
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }




    def get_double_rank(self,page):
        url = 'https://api.wtatennis.com/tennis/players/ranked?page=%s&pageSize=100&type=rankDoubles&sort=asc&name=&metric=DOUBLES&at=2019-12-30&nationality=' % page
        response = requests.get(url,headers=self.headers)
        if response.text == '':
            logger.info('没有排名数据。。。')
        else:
            rank_info = json.loads(response.text)
            for info in rank_info:
                player_info = {}
                player_info['player_id'] = info['player']['id']
                player_info['sport_id'] = 3
                player_info['name_en'] = info['player']['fullName']
                player_info['ranking'] = info['ranking']
                player_info['points'] = info['points']
                player_info['scope_date'] = 1577635200
                player_info['stat_cycle'] = 7
                player_info['promotion'] = info['movement']
                player_info['season_id'] = 2019
                if player_info['promotion'] > 0:
                    player_info['promotion_type'] = 1
                elif player_info['promotion'] == 0:
                    player_info['promotion_type'] = 0
                else:
                    player_info['promotion_type'] = 2
                TennisPlayerInfoDoubleRank.upsert(
                    self.session,
                    'player_id',
                    player_info
                )
                logger.info(player_info)

    def run(self):
        for page in range(14):
            self.get_double_rank(page)

