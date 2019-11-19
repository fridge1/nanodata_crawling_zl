import requests
import json
from orm_connection.orm_session import MysqlSvr
from orm_connection.orm_tableStruct_basketball import *
from apps.NBL.tools import *
import time
import queue



def pbp_box_live(match_id):
    headers = {
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            }
    url = 'https://www.fibalivestats.com/data/%s/data.json' % (match_id)
    pbp_res = requests.get(url,headers=headers)
    pbp_dict = json.loads(pbp_res.text)
    player_stats_list = []
    team_stats_list = []
    playbyplay_list = []
    period_total = pbp_dict['period']
    actionNumber_shot_dict = {}
    keys = pbp_dict['tm'].keys()
    for key in keys:
        BkMatchTeamStats = {}
        BkMatchTeamStats['belong'] = key
        BkMatchTeamStats['team_id'] = get_team_id(pbp_dict['tm'][key]['name'])
        BkMatchTeamStats['team_name'] = pbp_dict['tm'][key]['name']
        BkMatchTeamStats['goals'] = pbp_dict['tm'][key]['tot_sFieldGoalsMade']
        BkMatchTeamStats['field'] = pbp_dict['tm'][key]['tot_sFieldGoalsAttempted']
        BkMatchTeamStats['two_points_goals'] = pbp_dict['tm'][key]['tot_sTwoPointersMade']
        BkMatchTeamStats['two_points_total'] = pbp_dict['tm'][key]['tot_sTwoPointersAttempted']
        BkMatchTeamStats['three_point_goals'] = pbp_dict['tm'][key]['tot_sThreePointersMade']
        BkMatchTeamStats['three_point_field'] = pbp_dict['tm'][key]['tot_sThreePointersAttempted']
        BkMatchTeamStats['free_throw_goals'] = pbp_dict['tm'][key]['tot_sFreeThrowsMade']
        BkMatchTeamStats['free_throw_field'] = pbp_dict['tm'][key]['tot_sFreeThrowsAttempted']
        BkMatchTeamStats['offensive_rebounds'] = pbp_dict['tm'][key]['tot_sReboundsOffensive']
        BkMatchTeamStats['defensive_rebounds'] = pbp_dict['tm'][key]['tot_sReboundsDefensive']
        BkMatchTeamStats['rebounds'] = pbp_dict['tm'][key]['tot_sReboundsTotal']
        BkMatchTeamStats['assists'] = pbp_dict['tm'][key]['tot_sAssists']
        BkMatchTeamStats['steals'] = pbp_dict['tm'][key]['tot_sSteals']
        BkMatchTeamStats['blocks'] = pbp_dict['tm'][key]['tot_sBlocks']
        BkMatchTeamStats['turnovers'] = pbp_dict['tm'][key]['tot_sTurnovers']
        BkMatchTeamStats['personal_fouls'] = pbp_dict['tm'][key]['tot_sFoulsPersonal']
        BkMatchTeamStats['point'] = pbp_dict['tm'][key]['tot_sPoints']
        BkMatchTeamStats[''] = pbp_dict['tm'][key]['tot_sTwoPointersMade']
        team_stats_list.append(BkMatchTeamStats)
        player_keys = pbp_dict['tm'][key]['pl'].keys()
        for player_key in player_keys:
            player = {}
            player['belong'] = key
            player_name = pbp_dict['tm'][key]['pl'][player_key]['firstName'] + ' ' + pbp_dict['tm'][key]['pl'][player_key]['familyName']
            player['player_id'] = get_player_id(player_name)
            player['player_name'] = player_name
            player['minutes'] = pbp_dict['tm'][key]['pl'][player_key]['sMinutes']
            player['goals'] = pbp_dict['tm'][key]['pl'][player_key]['sFieldGoalsMade']
            player['field'] = pbp_dict['tm'][key]['pl'][player_key]['sFieldGoalsAttempted']
            player['two_points_goals'] = pbp_dict['tm'][key]['pl'][player_key]['sTwoPointersMade']
            player['two_points_total'] = pbp_dict['tm'][key]['pl'][player_key]['sTwoPointersAttempted']
            player['three_point_goals'] = pbp_dict['tm'][key]['pl'][player_key]['sThreePointersMade']
            player['three_point_field'] = pbp_dict['tm'][key]['pl'][player_key]['sThreePointersAttempted']
            player['free_throw_goals'] = pbp_dict['tm'][key]['pl'][player_key]['sFreeThrowsMade']
            player['free_throw_field'] = pbp_dict['tm'][key]['pl'][player_key]['sFreeThrowsAttempted']
            player['offensive_rebounds'] = pbp_dict['tm'][key]['pl'][player_key]['sReboundsOffensive']
            player['defensive_rebounds'] = pbp_dict['tm'][key]['pl'][player_key]['sReboundsDefensive']
            player['rebounds'] = pbp_dict['tm'][key]['pl'][player_key]['sReboundsTotal']
            player['assists'] = pbp_dict['tm'][key]['pl'][player_key]['sAssists']
            player['steals'] = pbp_dict['tm'][key]['pl'][player_key]['sSteals']
            player['blocks'] = pbp_dict['tm'][key]['pl'][player_key]['sBlocks']
            player['turnovers'] = pbp_dict['tm'][key]['pl'][player_key]['sTurnovers']
            player['personal_fouls'] = pbp_dict['tm'][key]['pl'][player_key]['sFoulsPersonal']
            player['point'] = pbp_dict['tm'][key]['pl'][player_key]['sPoints']
            player['first_publish'] = pbp_dict['tm'][key]['pl'][player_key]['starter']
            if pbp_dict['tm'][key]['pl'][player_key]['sMinutes'] == '0:00':
                player['enter_ground'] = 0
            elif pbp_dict['tm'][key]['pl'][player_key]['sMinutes'] != '0:00':
                player['enter_ground'] = 1
            else:
                player['enter_ground'] = 0
            player['on_ground'] = pbp_dict['tm'][key]['pl'][player_key]['active']
            player['shirt_number'] = pbp_dict['tm'][key]['pl'][player_key]['shirtNumber']
            player_stats_list.append(player)
        for pbp_shot in pbp_dict['tm'][key]['shot']:
            if 'jumpshot' in pbp_shot['subType']:
                shot_location = (pbp_shot['y'],pbp_shot['x'])
                actionNumber_shot_dict[pbp_shot['actionNumber']] = shot_location
    for pbp_info in pbp_dict['pbp']:
        period = pbp_info['period']
        type = 0
        home_score = pbp_info['s1']
        away_score = pbp_info['s2']
        belong = pbp_info['tno']
        try:
            actionNumber = pbp_info['actionNumber']
            location_x = round(actionNumber_shot_dict[actionNumber][0]) * 0.01 * 49 / 2
            location_y = round(actionNumber_shot_dict[actionNumber][1]) * 0.01 * 32
        except:
            location_x = -1
            location_y = -1
        try:
            player_name = pbp_info['familyName'] + ' ' + pbp_info['firstName']
        except:
            player_name = ''
        if player_name:
            player_ids = get_player_id(player_name)
        else:
            player_ids = ''
        period_time = pbp_info['gt']
        if player_name:
            if 'jumpball' in pbp_info['actionType']:
                shooting_play = 0
                score_value = 0
                scoring_play = 0
                word_text = pbp_info['shirtNumber'] + ',' + pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                            pbp_info['actionType'] + ' - ' + pbp_info['subType']
            else:
                if pbp_info['scoring'] == 0:
                    shooting_play = pbp_info['scoring']
                    score_value = 0
                    scoring_play = 0
                    word_text = pbp_info['shirtNumber'] + ',' + pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                pbp_info['actionType'] + ' ' + pbp_info['subType']
                elif pbp_info['scoring'] == 1:
                    if pbp_info['success'] == 0:
                        shooting_play = pbp_info['scoring']
                        score_value = 0
                        scoring_play = 0
                        word_text = pbp_info['shirtNumber'] + ',' + pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                    pbp_info['actionType'] + ' ' + pbp_info['subType'] + ' ' + 'missed'
                    elif pbp_info['success'] == 1:
                        shooting_play = pbp_info['scoring']
                        score_value = pbp_info['actionType'][0]
                        scoring_play = 1
                        if pbp_info['lead'] > 0 and pbp_info['tno'] == 1:
                            word_text = pbp_info['shirtNumber'] + ',' + pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                        pbp_info['actionType'] + ' ' + pbp_info['subType'] + ' ' + pbp_dict['tm'][str(pbp_info['tno'])]['name'] + ' - lead by ' + str(pbp_info['lead'])
                        elif pbp_info['lead'] > 0 and pbp_info['tno'] == 2:
                            word_text = pbp_info['shirtNumber'] + ',' + pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                            pbp_info['actionType'] + ' ' + pbp_info['subType'] + ' ' + pbp_dict['tm'][str(pbp_info['tno'])]['name'] + ' - trail by ' + str(pbp_info['lead'])
                        elif pbp_info['lead'] < 0 and pbp_info['tno'] == 1:
                            word_text = pbp_info['shirtNumber'] + ',' + pbp_info['firstName'] + ' ' + pbp_info[
                                'familyName'] + ',' + pbp_info['actionType'] + ' ' + pbp_info['subType'] + ' ' + pbp_dict['tm'][str(pbp_info['tno'])]['name'] + ' - trail by ' + str(abs(int(pbp_info['lead'])))
                        elif pbp_info['lead'] < 0 and pbp_info['tno'] == 2:
                            word_text = pbp_info['shirtNumber'] + ',' + pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                        pbp_info['actionType'] + ' ' + pbp_info['subType'] + ' ' + pbp_dict['tm'][str(pbp_info['tno'])]['name'] + ' - lead by ' + str(abs(int(pbp_info['lead'])))
                        else:
                            word_text = pbp_info['shirtNumber'] + ',' + pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                        pbp_info['actionType'] + ' ' + pbp_info['subType'] + ' ' + pbp_dict['tm'][str(pbp_info['tno'])]['name'] + ' - tie'
                    else:
                        shooting_play = 0
                        score_value = 0
                        scoring_play = 0
                        word_text = ''
                else:
                    shooting_play = 0
                    score_value = 0
                    scoring_play = 0
                    word_text = ''
        else:
            shooting_play = 0
            score_value = 0
            scoring_play = 0
            word_text = pbp_info['actionType'] + ' ' + pbp_info['subType']
        data = {
            'id' : match_id,
            'text':word_text,
            'period':period,
            'type':type,
            'home_score':home_score,
            'away_score':away_score,
            'belong':belong,
            'player_name':player_name,
            'player_ids':[player_ids],
            'period_time':period_time,
            'shooting_play':shooting_play,
            'score_value':score_value,
            'scoring_play':scoring_play,
            'text_en':word_text,
            'location_x' : location_x,
            'location_y' : location_y,
        }
        playbyplay_list.append(data)
    match_data_boxscore = {'match': {'id': match_id,
                                     'basketball_items': {
                                         'player_stat': {
                                             'items': player_stats_list},
                                         'team_stat': {'items': team_stats_list}
                                     }}}
    match_data_playbyplay = {'match': {'id': match_id,
                                       'basketball_items': {
                                           'incident': {
                                               'period': period_total,
                                               'items': playbyplay_list}
                                           }}}
    print(json.dumps(match_data_boxscore))
