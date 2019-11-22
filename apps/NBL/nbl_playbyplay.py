import requests
import json
import traceback

from apps.NBL.nbl_tools import translate
from apps.NBL.tools import *
import time
import queue


def pbp_box_live(data_queue):
    while True:
        headers = {
                    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
                }
        match_id = 1307436
        match_time = change_bjtime('2019-11-07 06:30:00')
        url = 'https://www.fibalivestats.com/data/1307436/data.json'
        pbp_res = requests.get(url,headers=headers)
        if int(match_time) >= int(time.time()) and pbp_res.status_code == 200:
            print('比赛未开赛....')
            time.sleep(10)
        else:
            pbp_dict = json.loads(pbp_res.text)
            player_stats_list = []
            team_stats_list = []
            playbyplay_list = []
            period_total = pbp_dict['period']
            actionNumber_shot_dict = {}
            keys = pbp_dict['tm'].keys()
            for key in keys:
                try:
                    BkMatchTeamStats = {}
                    BkMatchTeamStats['belong'] = int(key)
                    BkMatchTeamStats['team_id'] = get_team_id(pbp_dict['tm'][key]['name'])
                    BkMatchTeamStats['team_name'] = pbp_dict['tm'][key]['name']
                    try:
                        BkMatchTeamStats['goals'] = pbp_dict['tm'][key]['tot_sFieldGoalsMade']
                    except:
                        BkMatchTeamStats['goals'] = 0
                    try:
                        BkMatchTeamStats['field'] = pbp_dict['tm'][key]['tot_sFieldGoalsAttempted']
                    except:
                        BkMatchTeamStats['field'] = 0
                    try:
                        BkMatchTeamStats['two_points_goals'] = pbp_dict['tm'][key]['tot_sTwoPointersMade']
                    except:
                        BkMatchTeamStats['two_points_goals'] = 0
                    try:
                        BkMatchTeamStats['two_points_total'] = pbp_dict['tm'][key]['tot_sTwoPointersAttempted']
                    except:
                        BkMatchTeamStats['two_points_total'] = 0
                    try:
                        BkMatchTeamStats['three_point_goals'] = pbp_dict['tm'][key]['tot_sThreePointersMade']
                    except:
                        BkMatchTeamStats['three_point_goals'] = 0
                    try:
                        BkMatchTeamStats['three_point_field'] = pbp_dict['tm'][key]['tot_sThreePointersAttempted']
                    except:
                        BkMatchTeamStats['three_point_field'] = 0
                    try:
                        BkMatchTeamStats['free_throw_goals'] = pbp_dict['tm'][key]['tot_sFreeThrowsMade']
                    except:
                        BkMatchTeamStats['free_throw_goals'] = 0
                    try:
                        BkMatchTeamStats['free_throw_field'] = pbp_dict['tm'][key]['tot_sFreeThrowsAttempted']
                    except:
                        BkMatchTeamStats['free_throw_field'] = 0
                    try:
                        BkMatchTeamStats['offensive_rebounds'] = pbp_dict['tm'][key]['tot_sReboundsOffensive']
                    except:
                        BkMatchTeamStats['offensive_rebounds'] = 0
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
                        player['belong'] = int(key)
                        player_name = pbp_dict['tm'][key]['pl'][player_key]['firstName'] + ' ' + pbp_dict['tm'][key]['pl'][player_key]['familyName']
                        player['player_id'] = get_player_id(player_name)
                        player['player_name'] = player_name
                        minutes  = pbp_dict['tm'][key]['pl'][player_key]['sMinutes']
                        minute = minutes.split(':')[0]
                        second = minutes.split(':')[1]
                        if int(second) >= 30:
                            player['minutes'] = int(minute) + 1
                        else:
                            player['minutes'] = int(minute)
                        player['goals'] = int(pbp_dict['tm'][key]['pl'][player_key]['sFieldGoalsMade'])
                        player['field'] = int(pbp_dict['tm'][key]['pl'][player_key]['sFieldGoalsAttempted'])
                        player['two_points_goals'] = int(pbp_dict['tm'][key]['pl'][player_key]['sTwoPointersMade'])
                        player['two_points_total'] = int(pbp_dict['tm'][key]['pl'][player_key]['sTwoPointersAttempted'])
                        player['three_point_goals'] = int(pbp_dict['tm'][key]['pl'][player_key]['sThreePointersMade'])
                        player['three_point_field'] = int(pbp_dict['tm'][key]['pl'][player_key]['sThreePointersAttempted'])
                        player['free_throw_goals'] = int(pbp_dict['tm'][key]['pl'][player_key]['sFreeThrowsMade'])
                        player['free_throw_field'] = int(pbp_dict['tm'][key]['pl'][player_key]['sFreeThrowsAttempted'])
                        player['offensive_rebounds'] = int(pbp_dict['tm'][key]['pl'][player_key]['sReboundsOffensive'])
                        player['defensive_rebounds'] = int(pbp_dict['tm'][key]['pl'][player_key]['sReboundsDefensive'])
                        player['rebounds'] = int(pbp_dict['tm'][key]['pl'][player_key]['sReboundsTotal'])
                        player['assists'] = int(pbp_dict['tm'][key]['pl'][player_key]['sAssists'])
                        player['steals'] = int(pbp_dict['tm'][key]['pl'][player_key]['sSteals'])
                        player['blocks'] = int(pbp_dict['tm'][key]['pl'][player_key]['sBlocks'])
                        player['turnovers'] = int(pbp_dict['tm'][key]['pl'][player_key]['sTurnovers'])
                        player['personal_fouls'] = int(pbp_dict['tm'][key]['pl'][player_key]['sFoulsPersonal'])
                        player['point'] = int(pbp_dict['tm'][key]['pl'][player_key]['sPoints'])
                        player['first_publish'] = int(pbp_dict['tm'][key]['pl'][player_key]['starter'])
                        if pbp_dict['tm'][key]['pl'][player_key]['sMinutes'] == '0:00':
                            player['enter_ground'] = 0
                        elif pbp_dict['tm'][key]['pl'][player_key]['sMinutes'] != '0:00':
                            player['enter_ground'] = 1
                        else:
                            player['enter_ground'] = 0
                        player['on_ground'] = int(pbp_dict['tm'][key]['pl'][player_key]['active'])
                        player['shirt_number'] = int(pbp_dict['tm'][key]['pl'][player_key]['shirtNumber'])
                        player_stats_list.append(player)
                except:
                    print(traceback.format_exc())
                for pbp_shot in pbp_dict['tm'][key]['shot']:
                    if 'jumpshot' in pbp_shot['subType']:
                        shot_location = (pbp_shot['y'],pbp_shot['x'])
                        actionNumber_shot_dict[pbp_shot['actionNumber']] = shot_location
            for pbp_info in pbp_dict['pbp'][::-1]:
                period = pbp_info['period']
                type = 0
                home_score = pbp_info['s1']
                away_score = pbp_info['s2']
                belong = pbp_info['tno']
                try:
                    actionNumber = pbp_info['actionNumber']
                    if round(actionNumber_shot_dict[actionNumber][1]) < 50:
                        location_y = round(actionNumber_shot_dict[actionNumber][1]) * 0.01 * 32
                    else:
                        location_y = (round(actionNumber_shot_dict[actionNumber][1]) - 50) * 0.01 * 32
                    location_x = round(actionNumber_shot_dict[actionNumber][0]) * 0.01 * 49
                except:
                    location_x = -1
                    location_y = -1
                try:
                    player_name = pbp_info['firstName'] + ' ' + pbp_info['familyName']
                except:
                    player_name = ''
                if player_name:
                    player_ids = int(get_player_id(player_name))

                else:
                    player_ids = 0
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
                                if 'f' not in pbp_info['actionType'][0]:
                                    score_value = pbp_info['actionType'][0]
                                else:
                                    score_value = 0
                                scoring_play = 1
                                if pbp_info['lead'] > 0 and pbp_info['tno'] == 1:
                                    word_text = pbp_info['shirtNumber'] + ',' + pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                                pbp_info['actionType'] + ' ' + pbp_info['subType']
                                elif pbp_info['lead'] > 0 and pbp_info['tno'] == 2:
                                    word_text = pbp_info['shirtNumber'] + ',' + pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                    pbp_info['actionType'] + ' ' + pbp_info['subType']
                                elif pbp_info['lead'] < 0 and pbp_info['tno'] == 1:
                                    word_text = pbp_info['shirtNumber'] + ',' + pbp_info['firstName'] + ' ' + pbp_info[
                                        'familyName'] + ',' + pbp_info['actionType'] + ' ' + pbp_info['subType']
                                elif pbp_info['lead'] < 0 and pbp_info['tno'] == 2:
                                    word_text = pbp_info['shirtNumber'] + ',' + pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                                pbp_info['actionType'] + ' ' + pbp_info['subType']
                                else:
                                    word_text = pbp_info['shirtNumber'] + ',' + pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                                pbp_info['actionType'] + ' ' + pbp_info['subType']
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
                word_text_zh = translate(word_text)
                data = {
                    'id' : int(match_id),
                    'text':word_text_zh,
                    'period':int(period),
                    'type':int(type),
                    'home_score':int(home_score),
                    'away_score':int(away_score),
                    'belong':int(belong),
                    'player_name':player_name,
                    'player_ids':[player_ids],
                    'period_time':str(period_time),
                    'shooting_play':int(shooting_play),
                    'score_value':int(score_value),
                    'scoring_play':int(scoring_play),
                    'text_en':word_text,
                    'location_x' : int(location_x),
                    'location_y' : int(location_y),
                }
                playbyplay_list.append(data)
            match_data_boxscore = {'match': {'id': int(match_id),
                                             'basketball_items': {
                                                 'player_stat': {
                                                     'items': player_stats_list},
                                                 'team_stat': {'items': team_stats_list}
                                             }}}
            data_queue.put(match_data_boxscore)
            print('球员技术统计推送完成...')
            match_data_playbyplay = {'match': {'id': int(match_id),
                                               'basketball_items': {
                                                   'incident': {
                                                       'period': period_total,
                                                       'items': playbyplay_list}
                                                   }}}
            data_queue.put(match_data_playbyplay)
            print('球员技术文字直播推送完成...')
            if pbp_dict['clock'] == '00:00':
                break
            else:
                time.sleep(10)
                print('休息10秒再请求....')
                continue

# data_queue = queue.Queue()
#
# pbp_box_live(data_queue)
# def get_match_id():
#     url = 'https://api.nbl.com.au/_/custom/api/genius?route=competitions/24346/matches&matchType=REGULAR&limit=200&fields=matchId,matchStatus,matchTimeUTC,competitors,roundNumber,venue,ticketURL&liveapidata=false&filter[owner]=nbl'
#     headers = {
#         'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
#     }
#     res = requests.get(url,headers=headers)
#     match_dict = json.loads(res.text)
#     for id_time in match_dict['data']:
#         match_id = id_time['matchId']
#         match_time = change_bjtime(id_time['matchTimeUTC'])
#         pbp_box_live(match_id,match_time)




