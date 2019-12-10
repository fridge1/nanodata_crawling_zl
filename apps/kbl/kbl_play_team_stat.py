# -*- coding: utf-8 -*-
from apps.kbl.tools import *
import asyncio
from aiohttp import ClientSession
import aiohttp
from apps.send_error_msg import dingding_alter
import traceback
import json
from orm_connection.kbl_basketball import BleagueNblBasketballPlayerStats,BleagueNblBasketballTeamStats
from common.libs.log import LogMgr
logger = LogMgr.get('kbl_basketball_player_team_stat')





class PlayerTeamStats(object):
    def __init__(self):
        self.match_id_dict = get_match_id()



    async def get_player_stat(self):
        for key,value in self.match_id_dict.items():
            url = 'https://sports.news.naver.com/ajax/game/relayData.nhn?gameId=%s' % str(key)
            conn = aiohttp.TCPConnector(verify_ssl=False)
            async with ClientSession(connector=conn) as session:
                async with session.get(url) as response:
                    response = await response.text()
                    player_stat = json.loads(response)
                    yield player_stat,value

    async def jiexi_player_stat(self):
       try:
           spx_dev_session = MysqlSvr.get('spider_zl')
           async for player_stat,match_id in  self.get_player_stat():
               home_team_id = player_stat['home_team']
               away_team_id = player_stat['away_team']
               team_id_list = [home_team_id,away_team_id]
               first_id = []
               for index_name in player_stat['line_up']:
                   if 'status' not in index_name:
                       for first_player_id in player_stat['line_up'][index_name]:
                           first_id.append(player_stat['line_up'][index_name][first_player_id])
               for team_id in team_id_list:
                   player_stat_info = player_stat['player_avg_record']['game'][team_id]
                   for key,value in player_stat_info.items():
                       player_stat_dict = {}
                       if key in first_id:
                           player_stat_dict['first'] = 1
                       else:
                           player_stat_dict['first'] = 0
                       info_list = value.split(',')
                       if int(info_list[5]) >= 30 and int(info_list[4]) >= 1:
                           player_stat_dict['minutes_played'] = int(info_list[4]) + 1
                       elif int(info_list[5]) >= 1 and int(info_list[4]) == 0:
                           player_stat_dict['minutes_played'] = 1
                       else:
                           player_stat_dict['minutes_played'] = int(info_list[4])
                       player_stat_dict['sport_id'] = 2
                       player_stat_dict['match_id'] = int(match_id)
                       player_stat_dict['team_id'] = int(team_id)
                       player_stat_dict['player_id'] = key
                       player_stat_dict['position'] = str(info_list[1])
                       player_stat_dict['points'] = int(info_list[22])
                       player_stat_dict['free_throws_scored'] = int(info_list[8])
                       player_stat_dict['free_throws_total'] = int(info_list[9])
                       if int(info_list[9]) == 0:
                           player_stat_dict['free_throws_accuracy'] = 0
                       else:
                           player_stat_dict['free_throws_accuracy'] = round(int(info_list[8])/int(info_list[9])*100)
                       player_stat_dict['two_points_scored'] = int(info_list[6])
                       player_stat_dict['two_points_total'] = int(info_list[7])
                       if int(info_list[7]) == 0:
                           player_stat_dict['two_points_accuracy'] = 0
                       else:
                           player_stat_dict['two_points_accuracy'] = round(int(info_list[6])/int(info_list[7])*100)
                       player_stat_dict['three_points_scored'] = int(info_list[10])
                       player_stat_dict['three_points_total'] = int(info_list[11])
                       if int(info_list[11]) == 0:
                           player_stat_dict['three_points_accuracy'] = 0
                       else:
                           player_stat_dict['three_points_accuracy'] = round(int(info_list[10])/int(info_list[11])*100)
                       player_stat_dict['field_goals_scored'] = int(info_list[6]) + int(info_list[10])
                       player_stat_dict['field_goals_total'] = int(info_list[7]) + int(info_list[11])
                       if player_stat_dict['field_goals_total'] == 0:
                           player_stat_dict['field_goals_accuracy'] = 0
                       else:
                           player_stat_dict['field_goals_accuracy'] = round(player_stat_dict['field_goals_scored']/player_stat_dict['field_goals_total']*100)
                       player_stat_dict['defensive_rebounds'] = int(info_list[14])
                       player_stat_dict['offensive_rebounds'] = int(info_list[15])
                       player_stat_dict['rebounds'] = int(info_list[30])
                       player_stat_dict['assists'] = int(info_list[16])
                       player_stat_dict['steals'] = int(info_list[17])
                       player_stat_dict['blocks'] = int(info_list[18])
                       player_stat_dict['key'] = str(match_id)+str(key)
                       BleagueNblBasketballPlayerStats.upsert(
                           spx_dev_session,
                           'key',
                           player_stat_dict
                       )
                       logger.info('player_stat_dict:',player_stat_dict)
       except:
           logger.error(traceback.format_exc())
           dingding_alter(traceback.format_exc())


    async def jiexi_team_stat(self):
       try:
           spx_dev_session = MysqlSvr.get('spider_zl')
           async for player_stat,match_id in  self.get_player_stat():
               home_team_id = player_stat['home_team']
               away_team_id = player_stat['away_team']
               team_id_list = [home_team_id,away_team_id]
               for team_id in team_id_list:
                   team_stat_dict = {}
                   team_stat_info = player_stat['team_game_rec'][team_id]
                   team_stat_dict['sport_id'] = 2
                   team_stat_dict['match_id'] = int(match_id)
                   team_stat_dict['team_id'] = int(team_id)
                   team_stat_dict['two_pointers_scored'] = int(team_stat_info['fg'])
                   team_stat_dict['two_pointers_total'] = int(team_stat_info['fg_a'])
                   if int(team_stat_info['fg_a']) == 0:
                       team_stat_dict['two_pointers_accuracy'] = 0
                   else:
                       team_stat_dict['two_pointers_accuracy'] = round(int(team_stat_info['fg']) / int(team_stat_info['fg_a']) * 100)
                   team_stat_dict['three_pointers_scored'] = int(team_stat_info['threep'])
                   team_stat_dict['three_pointers_total'] = int(team_stat_info['threep_a'])
                   if int(team_stat_info['threep_a']) == 0:
                       team_stat_dict['three_pointers_accuracy'] = 0
                   else:
                       team_stat_dict['three_pointers_accuracy'] = round(int(team_stat_info['threep']) / int(team_stat_info['threep_a']) * 100)
                   team_stat_dict['field_goals_scored'] = int(team_stat_info['fg']) + int(team_stat_info['threep'])
                   team_stat_dict['field_goals_total'] = int(team_stat_info['fg_a']) + int(team_stat_info['threep_a'])
                   if team_stat_dict['field_goals_total'] == 0:
                       team_stat_dict['field_goals_accuracy'] = 0
                   else:
                       team_stat_dict['field_goals_accuracy'] = round(team_stat_dict['field_goals_scored'] / team_stat_dict['field_goals_total'] * 100)
                   team_stat_dict['free_throws_scored'] = int(team_stat_info['ft'])
                   team_stat_dict['free_throws_total'] = int(team_stat_info['ft_a'])
                   if team_stat_dict['free_throws_total'] == 0:
                       team_stat_dict['free_throws_accuracy'] = 0
                   else:
                       team_stat_dict['free_throws_accuracy'] = round(team_stat_dict['free_throws_scored'] / team_stat_dict['free_throws_total'] * 100)
                   team_stat_dict['total_fouls'] = team_stat_info['foul_tot']
                   team_stat_dict['rebounds'] = team_stat_info['rebound']
                   team_stat_dict['defensive_rebounds'] = team_stat_info['d_r']
                   team_stat_dict['offensive_rebounds'] = team_stat_info['o_r']
                   team_stat_dict['assists'] = team_stat_info['a_s']
                   team_stat_dict['steals'] = team_stat_info['s_t']
                   team_stat_dict['blocks'] = team_stat_info['b_s']
                   team_stat_dict['key'] = str(match_id)+str(team_id)
                   BleagueNblBasketballTeamStats.upsert(
                       spx_dev_session,
                       'key',
                       team_stat_dict
                   )
                   logger.info('team_stat_dict:',team_stat_dict)
       except:
           logger.error(traceback.format_exc())
           dingding_alter(traceback.format_exc())


    async def run(self):
        task1 = asyncio.create_task(self.jiexi_player_stat())
        task2 = asyncio.create_task(self.jiexi_team_stat())
        coro = [task1,task2]
        await asyncio.gather(*coro)




if __name__ == '__main__':
    a = PlayerTeamStats()
    asyncio.run(a.run())





