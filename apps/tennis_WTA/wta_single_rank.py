import requests
from orm_connection.orm_session import MysqlSvr
from orm_connection.tennis import TennisPlayerInfoSingleRank
from apps.tennis_WTA.tools import rank_match_bjtime,get_proxy
import json
from apps.tennis_WTA.get_monday_date import GetMondayDate
from common.libs.log import LogMgr

logger = LogMgr.get('wta_tennis_single_rank')



class GetSingleRankInfo(object):
    def __init__(self):
        self.session = MysqlSvr.get('spider_zl')
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.proxy = get_proxy()




    def get_double_rank(self,page,date):
        url = 'https://api.wtatennis.com/tennis/players/ranked?page=%s&pageSize=100&type=rankSingles&sort=asc&name=&metric=SINGLES&at=%s&nationality=' % (page,date)
        print(url)
        response = requests.get(url,headers=self.headers)
        print(response.text)
        if response.text == '':
            logger.info('没有排名数据。。。')
        else:
            rank_info = json.loads(response.text)
            for info in rank_info:
                player_info = {}
                player_info['player_id'] = info['player']['id']
                player_info['key'] = str(date) + str(player_info['player_id'])
                player_info['sport_id'] = 3
                player_info['name_en'] = info['player']['fullName']
                player_info['ranking'] = info['ranking']
                player_info['points'] = info['points']
                player_info['scope_date'] = rank_match_bjtime(date)
                player_info['stat_cycle'] = 7
                player_info['promotion'] = info['movement']
                player_info['season_id'] = 2019
                if player_info['promotion'] > 0:
                    player_info['promotion_type'] = 1
                elif player_info['promotion'] == 0:
                    player_info['promotion_type'] = 0
                else:
                    player_info['promotion_type'] = 2
                TennisPlayerInfoSingleRank.upsert(
                    self.session,
                    'key',
                    player_info
                )
                logger.info(player_info)

    def run(self):
        monday_date_list = GetMondayDate().run(2020)
        for date in monday_date_list:
            for page in range(16):
                self.get_double_rank(page,date)


