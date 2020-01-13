import requests
import json
import traceback
from orm_connection.orm_session import MysqlSvr
from orm_connection.tennis import TennisSinglePlayerStatBySeason,TennisPlayerInfoDoubleRank,TennisPlayerInfoSingleRank
from common.libs.log import LogMgr

logger = LogMgr.get('wta_tennis_player_season_stat')


class GetSinglePlayerStat(object):
    def __init__(self):
        self.session = MysqlSvr.get('spider_zl')
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }



    def get_player_stat(self,player_id,year):
        player_stat = {}
        url = 'https://api.wtatennis.com/tennis/players/%s/year/%s' % (player_id,year)
        logger.info(url)
        res = requests.get(url,headers=self.headers)
        if res.text:
            stat_info = json.loads(res.text)
            if 'stats' in list(stat_info.keys()):
                player_stat['key'] = str(year)+str(player_id)
                player_stat['season_id'] = year
                player_stat['sport_id'] = 3
                player_stat['player_id'] = player_id
                player_stat['aces'] = stat_info['stats']['Aces']
                player_stat['double_faults'] = stat_info['stats']['Double_Faults']
                player_stat['service_points_win'] = stat_info['stats']['service_points_won_percent']
                player_stat['first_serve'] = stat_info['stats']['first_serve_percent']
                player_stat['first_serve_win'] = stat_info['stats']['first_serve_won_percent']
                player_stat['second_serve_win'] = stat_info['stats']['second_serve_won_percent']
                player_stat['break_point_saved'] = stat_info['stats']['breakpoint_saved_percent']
                player_stat['service_games_win'] = stat_info['stats']['service_games_won_percent']
                player_stat['service_games_played'] = stat_info['stats']['Service_Games_Played']
                player_stat['return_points_win'] = stat_info['stats']['return_points_won_percent']
                player_stat['first_return_points_won'] = stat_info['stats']['first_return_percent']
                player_stat['second_return_points_won'] = stat_info['stats']['second_return_percent']
                player_stat['break_point_converted'] = stat_info['stats']['breakpoint_converted_percent']
                player_stat['break_points_lost'] = stat_info['stats']['Break_Points_Lost']
                player_stat['return_games_win'] = stat_info['stats']['return_games_won_percent']
                player_stat['return_games_played'] = stat_info['stats']['Return_Games_Played']
                player_stat['break_points_faced'] = stat_info['stats']['Break_Points_Faced']
                player_stat['match_count'] = stat_info['stats']['MatchCount']
                TennisSinglePlayerStatBySeason.upsert(
                    self.session,
                    'key',
                    player_stat
                )
                logger.info(player_stat)
            else:
                logger.info(stat_info)
        else:
            logger.info('该球员没有该赛季的技术统计。。。%s,%s' % (player_id,year))


    def get_double_player(self):
        session = MysqlSvr.get('spider_zl')
        for row in TennisPlayerInfoDoubleRank.inter(
                session=session,
                key='id',
                per_page=1000
        ):
            for year in range(2010,2020):
                try:
                    self.get_player_stat(row.player_id, year)
                except:
                    logger.error(traceback.format_exc())
                    continue


    def get_single_player(self):
        session = MysqlSvr.get('spider_zl')
        for row in TennisPlayerInfoSingleRank.inter(
                session=session,
                key='id',
                per_page=1000
        ):
            for year in range(2010,2020):
                try:
                    self.get_player_stat(row.player_id,year)
                except:
                    logger.error(traceback.format_exc())
                    continue





