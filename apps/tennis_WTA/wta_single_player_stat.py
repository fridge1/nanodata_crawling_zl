import requests
import json
from orm_connection.orm_session import MysqlSvr
from orm_connection.tennis import TennisSinglePlayerStatBySeason
from apps.tennis_WTA.tools import get_player_double_name,get_player_single_name


class GetSinglePlayerStat(object):
    def __init__(self):
        self.session = MysqlSvr.get('spider_zl')
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.single_name_dict = get_player_single_name()
        self.double_name_dict = get_player_double_name()



    def get_player_stat(self,player_id,year):
        player_stat = {}
        url = 'https://api.wtatennis.com/tennis/players/%s/year/%s' % (player_id,year)
        print(url)
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
                print(player_stat)
            else:
                print(stat_info)
        else:
            print('该球员没有该赛季的技术统计。。。')


    def run(self):
        player_id_list = list(set(list(self.single_name_dict.keys()) + list(self.double_name_dict.keys())))
        for player_id in player_id_list:
            for year in range(2010,2020):
                self.get_player_stat(player_id,year)





