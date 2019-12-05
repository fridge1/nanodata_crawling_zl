# -*- coding: utf-8 -*-
from apps.kbl.tools import *
from apps.kbl.kbl_translate import translate
import json


period_list = {
    'Q1':1,
    'Q2':2,
    'Q3':3,
    'Q4':4,
    'X1':5,
    'X2':6,
    'X3':7
}
headers = {
            'user_agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }

url = 'https://sports.news.naver.com/ajax/game/relayData.nhn?gameId=201912041665350189'
res = requests.get(url,headers=headers).json()
away_team_code = res['away_team']
home_team_code = res['home_team']
if res['line_up']['status'] == 0:
    print('未开赛......')
else:
    playbyplay_list = []
    for stage in list(res['live_text'])[:-4]:
        print(stage)
        period = period_list[stage]
        print(period)
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
            playbyplay_dict = {}
            for playbyplay_info in res['live_text'][stage][minutes_second]:
                team_code = playbyplay_info.split(',')[0]
                if team_code == home_team_code:
                    belong = 1
                else:
                    belong = 2
                player = ' '.join(playbyplay_info.split(',')[-1].split(' ')[:-1])
                player_name_zh = translate(player)
                text_en = player + ' ' + playbyplay_info.split(',')[-1].split(' ')[-1]
                text = translate(text_en)
                print(text)
                home_score = res['quarter_score'][home_team_code]['total_score']
                away_scort = res['quarter_score'][away_team_code]['total_score']
                type = 0
    # match_id = 1
    # first_id = []
    # for index_name in res['line_up']:
    #     if 'status' not in index_name:
    #         for first_player_id in res['line_up'][index_name]:
    #             first_id.append(res['line_up'][index_name][first_player_id])
    # player_list = []
    # for player_rec in res['player_avg_record']['game']:
    #     player_box = res['player_avg_record']['game'][player_rec]
    #     if 'format' not in player_rec:
    #         player_boxer = {}
    #         for player_id in player_box:
    #             player_boxer['player_id'] = player_id
    #             if player_id in first_id:
    #                 player_boxer['first_publish'] = 1
    #             else:
    #                 player_boxer['first_publish'] = 0
    #             box_list = player_box[player_id].split(',')
    #             if away_team_code in box_list[2]:
    #                 player_boxer['belong'] = 0
    #             else:
    #                 player_boxer['belong'] = 1
    #             player_boxer['player_name'] = box_list[0]
    #             if int(box_list[5]) >= 30 and int(box_list[4]) >= 1:
    #                 player_boxer['minutes'] = int(box_list[4]) + 1
    #             elif int(box_list[5]) >= 1 and int(box_list[4]) == 0:
    #                 player_boxer['minutes'] = 1
    #             else:
    #                 player_boxer['minutes'] = int(box_list[4])
    #             if player_boxer['minutes'] == 0:
    #                 player_boxer['enter_ground'] = 0
    #             else:
    #                 player_boxer['enter_ground'] = 1
    #             player_boxer['two_points_goals'] = int(box_list[6])
    #             player_boxer['two_points_total'] = int(box_list[7])
    #             player_boxer['free_throw_goals'] = int(box_list[8])
    #             player_boxer['free_throw_field'] = int(box_list[9])
    #             player_boxer['three_point_goals'] = int(box_list[10])
    #             player_boxer['three_point_field'] = int(box_list[11])
    #             player_boxer['goals'] = player_boxer['two_points_goals'] + player_boxer['three_point_goals']
    #             player_boxer['field'] =  player_boxer['two_points_total'] + player_boxer['three_point_field']
    #             player_boxer['offensive_rebounds'] = int(box_list[14])
    #             player_boxer['defensive_rebounds'] = int(box_list[15])
    #             player_boxer['rebounds'] = player_boxer['offensive_rebounds'] + player_boxer['defensive_rebounds']
    #             player_boxer['assists'] = box_list[16]
    #             player_boxer['steals'] = box_list[17]
    #             player_boxer['blocks'] = box_list[18]
    #             player_boxer['point'] = box_list[22]
    #             player_boxer['shirt_number'] = box_list[3]
    #             player_list.append(player_boxer)
    # team_list = []
    # for team_code in res['team_game_rec']:
    #     team_boxer = {}
    #     if team_code == away_team_code:
    #         team_boxer['belong'] = 2
    #     else:
    #         team_boxer['belong'] = 1
    #     team_boxer['team_id'] = team_code
    #     team_boxer['team_name'] = translater_team_name[int(team_code)]
    #     team_boxer['two_points_goals'] = int(res['team_game_rec'][team_code]['fg'])
    #     team_boxer['two_points_total'] = int(res['team_game_rec'][team_code]['fg_a'])
    #     team_boxer['three_point_goals'] = int(res['team_game_rec'][team_code]['threep'])
    #     team_boxer['three_point_field'] = int(res['team_game_rec'][team_code]['threep_a'])
    #     team_boxer['free_throw_goals'] = int(res['team_game_rec'][team_code]['ft'])
    #     team_boxer['free_throw_field'] = int(res['team_game_rec'][team_code]['ft_a'])
    #     team_boxer['offensive_rebounds'] = int(res['team_game_rec'][team_code]['o_r'])
    #     team_boxer['defensive_rebounds'] = int(res['team_game_rec'][team_code]['d_r'])
    #     team_boxer['rebounds'] = int(res['team_game_rec'][team_code]['rebound'])
    #     team_boxer['goals'] = team_boxer['two_points_goals'] + team_boxer['three_point_goals']
    #     team_boxer['field'] = team_boxer['two_points_total'] + team_boxer['three_point_field']
    #     team_boxer['assists'] = res['team_game_rec'][team_code]['a_s']
    #     team_boxer['steals'] = res['team_game_rec'][team_code]['s_t']
    #     team_boxer['blocks'] = res['team_game_rec'][team_code]['b_s']
    #     team_boxer['personal_fouls'] = res['team_game_rec'][team_code]['foul_tot']
    #     team_boxer['point'] = res['quarter_score'][team_code]['total_score']
    #     team_list.append(team_boxer)
    # match_data_boxscore = {'match': {'id': int(match_id),
    #                                  'basketball_items': {
    #                                      'player_stat': {
    #                                          'items': player_list},
    #                                      'team_stat': {'items': team_list}
    #                                  }}}
    # print(match_data_boxscore)


