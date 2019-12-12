# -*- coding: utf-8 -*-
from apps.kbl.tools import *
from apps.kbl.kbl_translate import translate
import asyncio
from apps.send_error_msg import dingding_alter
import traceback
from common.libs.log import LogMgr

logger = LogMgr.get('kbl_basketball_pbp_box_live')


class PbpBoxLive(object):
    def __init__(self):
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.match_id_dict = get_match_id_start()
        self.player_id_list = get_player_id()

    async def kbl_playbyplay(self, game_id, match_id, first_id_dict):
        try:
            url = 'https://sports.news.naver.com/ajax/game/relayData.nhn?gameId=%s' % str(game_id)
            period_list = {
                'Q1': 1,
                'Q2': 2,
                'Q3': 3,
                'Q4': 4,
                'X1': 5,
                'X2': 6,
                'X3': 7,
                'X4': 8,
            }
            res = requests.get(url, headers=self.headers).json()
            away_team_code = res['away_team']
            home_team_code = res['home_team']
            player_list = []
            team_list = []
            if res['line_up']['status'] == 0:
                logger.info('未开赛......%s' % game_id)
                match_data_boxscore = {'match': {'id': int(match_id),
                                                 'basketball_items': {
                                                     'player_stat': {
                                                         'items': ''},
                                                     'team_stat': {'items': ''}
                                                 }}}
                match_data_playbyplay = {'match': {'id': int(match_id),
                                                   'basketball_items': {
                                                       'incident': {
                                                           'period': '',
                                                           'items': ''}
                                                   }}}
                return match_data_boxscore, match_data_playbyplay

            else:
                line_up_id = []
                for index_name in res['line_up']:
                    if 'status' not in index_name:
                        for first_player_id in res['line_up'][index_name]:
                            line_up_id.append(res['line_up'][index_name][first_player_id])
                team_code_list = list(res['player_avg_record']['game'])
                team_code_list.remove('format')
                for player_rec in team_code_list:
                    player_box = res['player_avg_record']['game'][player_rec]
                    for player_id in player_box:
                        player_boxer = {}
                        first_id_list = first_id_dict[game_id]
                        if player_id in first_id_list:
                            player_boxer['first_publish'] = 1
                        else:
                            player_boxer['first_publish'] = 0
                        if player_id in line_up_id:
                            player_boxer['on_ground'] = 0
                        else:
                            player_boxer['on_ground'] = 1
                        box_list = player_box[player_id].split(',')
                        if int(away_team_code) == int(box_list[2]):
                            player_boxer['belong'] = 2
                        elif int(home_team_code) == int(box_list[2]):
                            player_boxer['belong'] = 1
                        else:
                            player_boxer['belong'] = 0
                        player_boxer['player_name'] = box_list[0]
                        if int(box_list[5]) >= 30 and int(box_list[4]) >= 1:
                            player_boxer['minutes'] = int(box_list[4]) + 1
                        elif int(box_list[5]) >= 1 and int(box_list[4]) == 0:
                            player_boxer['minutes'] = 1
                        else:
                            player_boxer['minutes'] = int(box_list[4])

                        player_boxer['enter_ground'] = 1
                        if player_id in self.player_id_list:
                            player_boxer['player_id'] = int(player_id)
                        else:
                            player_boxer['player_id'] = upsert_player_id(player_id, box_list[0], box_list[2],
                                                                         box_list[3],
                                                                         box_list[1])
                        player_boxer['two_points_goals'] = int(box_list[6])
                        player_boxer['two_points_total'] = int(box_list[7])
                        player_boxer['free_throw_goals'] = int(box_list[8])
                        player_boxer['free_throw_field'] = int(box_list[9])
                        player_boxer['three_point_goals'] = int(box_list[10])
                        player_boxer['three_point_field'] = int(box_list[11])
                        player_boxer['goals'] = player_boxer['two_points_goals'] + player_boxer['three_point_goals']
                        player_boxer['field'] = player_boxer['two_points_total'] + player_boxer['three_point_field']
                        player_boxer['offensive_rebounds'] = int(box_list[14])
                        player_boxer['defensive_rebounds'] = int(box_list[15])
                        player_boxer['rebounds'] = player_boxer['offensive_rebounds'] + player_boxer[
                            'defensive_rebounds']
                        player_boxer['assists'] = int(box_list[16])
                        player_boxer['steals'] = int(box_list[17])
                        player_boxer['blocks'] = int(box_list[18])
                        player_boxer['point'] = int(box_list[22])
                        player_boxer['shirt_number'] = int(box_list[3])
                        player_list.append(player_boxer)
                    for team_code in res['team_game_rec']:
                        team_boxer = {}
                        if team_code == away_team_code:
                            team_boxer['belong'] = 2
                        else:
                            team_boxer['belong'] = 1
                        team_boxer['team_id'] = int(team_code)
                        team_boxer['team_name'] = translater_team_name[int(team_code)]
                        team_boxer['two_points_goals'] = int(res['team_game_rec'][team_code]['fg'])
                        team_boxer['two_points_total'] = int(res['team_game_rec'][team_code]['fg_a'])
                        team_boxer['three_point_goals'] = int(res['team_game_rec'][team_code]['threep'])
                        team_boxer['three_point_field'] = int(res['team_game_rec'][team_code]['threep_a'])
                        team_boxer['free_throw_goals'] = int(res['team_game_rec'][team_code]['ft'])
                        team_boxer['free_throw_field'] = int(res['team_game_rec'][team_code]['ft_a'])
                        team_boxer['offensive_rebounds'] = int(res['team_game_rec'][team_code]['o_r'])
                        team_boxer['defensive_rebounds'] = int(res['team_game_rec'][team_code]['d_r'])
                        team_boxer['rebounds'] = int(res['team_game_rec'][team_code]['rebound'])
                        team_boxer['goals'] = team_boxer['two_points_goals'] + team_boxer['three_point_goals']
                        team_boxer['field'] = team_boxer['two_points_total'] + team_boxer['three_point_field']
                        team_boxer['assists'] = int(res['team_game_rec'][team_code]['a_s'])
                        team_boxer['steals'] = int(res['team_game_rec'][team_code]['s_t'])
                        team_boxer['blocks'] = int(res['team_game_rec'][team_code]['b_s'])
                        team_boxer['personal_fouls'] = int(res['team_game_rec'][team_code]['foul_tot'])
                        team_boxer['point'] = int(res['quarter_score'][team_code]['total_score'])
                        team_list.append(team_boxer)
                match_data_boxscore = {'match': {'id': int(match_id),
                                                 'basketball_items': {
                                                     'player_stat': {
                                                         'items': player_list},
                                                     'team_stat': {'items': team_list}
                                                 }}}
                playbyplay_list = []
                period_total = len(res['quarter_score'][home_team_code].keys()) - 1
                home_score = 0
                away_score = 0
                for stage in list(res['live_text']):
                    if 'Q' in stage or 'X' in stage:
                        period = period_list[stage]
                        for minutes_second in res['live_text'][stage]:
                            minute = minutes_second.split(':')[0]
                            second = minutes_second.split(':')[1]
                            match_minute = 9 - int(minute)
                            match_second = 60 - int(second)
                            if match_second == 60:
                                game_minute = match_minute + 1
                                game_second = '00'
                            else:
                                game_minute = match_minute
                                game_second = match_second
                            if len(str(game_second)) == 1:
                                period_time = '0' + str(game_minute) + ':0' + str(game_second)
                            else:
                                period_time = '0' + str(game_minute) + ':' + str(game_second)
                            for playbyplay_info in res['live_text'][stage][minutes_second]:
                                playbyplay_dict = {}
                                team_code = playbyplay_info.split(',')[0]
                                if team_code == home_team_code:
                                    belong = 1
                                else:
                                    belong = 2
                                player = ' '.join(playbyplay_info.split(',')[-1].split(' ')[:-1])
                                player_name_zh = translate(player)
                                text_en = player + ' ' + playbyplay_info.split(',')[-1].split(' ')[-1]
                                if '2점슛성공' in playbyplay_info or '덩크슛성공' in playbyplay_info:
                                    if int(playbyplay_info.split(',')[0]) == int(home_team_code):
                                        home_score += 2
                                        away_score += 0
                                    else:
                                        home_score += 0
                                        away_score += 2
                                elif '자유투성공' in playbyplay_info:
                                    if int(playbyplay_info.split(',')[0]) == int(home_team_code):
                                        home_score += 1
                                        away_score += 0
                                    else:
                                        home_score += 0
                                        away_score += 1
                                elif '3점슛성공' in playbyplay_info:
                                    if int(playbyplay_info.split(',')[0]) == int(home_team_code):
                                        home_score += 3
                                        away_score += 0
                                    else:
                                        home_score += 0
                                        away_score += 3
                                else:
                                    home_score += 0
                                    away_score += 0
                                text_no_name = playbyplay_info.split(',')[-1].split(' ')[-1]
                                if res['live_text']['quarter'] == 'end':
                                    text = '比赛结束'
                                else:
                                    text = player_name_zh + ' ' + translate(text_no_name)
                                type = 0
                                playbyplay_dict['id'] = int(match_id)
                                playbyplay_dict['type'] = type
                                playbyplay_dict['home_score'] = int(home_score)
                                playbyplay_dict['away_score'] = int(away_score)
                                playbyplay_dict['belong'] = int(belong)
                                playbyplay_dict['period'] = int(period)
                                playbyplay_dict['period_time'] = period_time
                                playbyplay_dict['text'] = text
                                playbyplay_dict['text_en'] = text_en
                                playbyplay_list.append(playbyplay_dict)
                match_data_playbyplay = {'match': {'id': int(match_id),
                                                   'basketball_items': {
                                                       'incident': {
                                                           'period': int(period_total),
                                                           'items': playbyplay_list}
                                                   }}}
                logger.info('数据返回成功。。。')
                return match_data_boxscore, match_data_playbyplay
        except:
            dingding_alter(traceback.format_exc())

    async def get_first_id_list(self, game_id_list):
        first_id_dict = {}
        for game_id in game_id_list:
            url = 'https://sports.news.naver.com/ajax/game/relayData.nhn?gameId=%s' % str(game_id)
            res = requests.get(url, headers=self.headers).json()
            away_team_code = res['away_team']
            home_team_code = res['home_team']
            if res['line_up']['status'] == 0:
                logger.info('未开赛......%s' % game_id)
            else:
                first_id_list = []
                for team_id in [away_team_code, home_team_code]:
                    for value in res['line_up'][team_id].values():
                        first_id_list.append(value)
                    first_id_dict[game_id] = first_id_list
        return first_id_dict
