import json
import threading
import traceback
from orm_connection.orm_session import MysqlSvr
from orm_connection.orm_tableStruct_basketball import BleagueNblBasketballPlayer
from apps.NBL.nbl_tools import translate
from apps.NBL.tools import *
from apps.send_error_msg import dingding_alter
from common.libs.log import LogMgr

logger = LogMgr.get('nbl_basketball_pbp_box_live')


class pbp_box(object):
    def __init__(self):
        self.team_id_get = get_team_id()
        self.get_match_id_start = get_match_id_start()
        self.get_player_id = get_player_id()

    def pbp_box_live(self, data_queue, match_id):
        while True:
            try:
                headers = {
                    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
                }
                url = 'https://www.fibalivestats.com/data/%s/data.json' % str(match_id)
                logger.info(url)
                pbp_res = requests.get(url, headers=headers)
                if pbp_res.status_code != 200:
                    logger.info('比赛未开赛.... %s' % str(match_id))
                    time.sleep(10)
                else:
                    pbp_dict = json.loads(pbp_res.text)
                    if pbp_dict['inOT'] == 0:
                        period_total = pbp_dict['period']
                    else:
                        period_total = pbp_dict['period'] + 4
                    player_stats_list = []
                    team_stats_list = []
                    playbyplay_list = []
                    actionNumber_shot_dict = {}
                    keys = pbp_dict['tm'].keys()
                    for key in keys:
                        try:
                            BkMatchTeamStats = {}
                            BkMatchTeamStats['belong'] = int(key)
                            BkMatchTeamStats['team_id'] = self.team_id_get[str(pbp_dict['tm'][key]['name'])]
                            BkMatchTeamStats['team_name'] = pbp_dict['tm'][key]['name']
                            BkMatchTeamStats['goals'] = int(safe_get(pbp_dict,'tm.%s.tot_sFieldGoalsMade' % key))
                            BkMatchTeamStats['field'] = int(safe_get(pbp_dict,'tm.%s.tot_sFieldGoalsAttempted' % key))
                            BkMatchTeamStats['two_points_goals'] = int(safe_get(pbp_dict,'tm.%s.tot_sTwoPointersMade' % key))
                            BkMatchTeamStats['two_points_total'] = int(safe_get(pbp_dict,'tm.%s.tot_sTwoPointersAttempted' % key))
                            BkMatchTeamStats['three_point_goals'] = int(safe_get(pbp_dict,'tm.%s.tot_sThreePointersMade' % key))
                            BkMatchTeamStats['three_point_field'] = int(safe_get(pbp_dict,'tm.%s.tot_sThreePointersAttempted' % key))
                            BkMatchTeamStats['free_throw_goals'] = int(safe_get(pbp_dict,'tm.%s.tot_sFreeThrowsMade' % key))
                            BkMatchTeamStats['free_throw_field'] = int(safe_get(pbp_dict,'tm.%s.tot_sFreeThrowsAttempted' % key))
                            BkMatchTeamStats['offensive_rebounds'] = int(safe_get(pbp_dict,'tm.%s.tot_sReboundsOffensive' % key))
                            BkMatchTeamStats['defensive_rebounds'] = int(safe_get(pbp_dict,'tm.%s.tot_sReboundsDefensive' % key))
                            BkMatchTeamStats['rebounds'] = int(safe_get(pbp_dict,'tm.%s.tot_sReboundsTotal' % key))
                            BkMatchTeamStats['assists'] = int(safe_get(pbp_dict,'tm.%s.tot_sAssists' % key))
                            BkMatchTeamStats['steals'] = int(safe_get(pbp_dict,'tm.%s.tot_sSteals' % key))
                            BkMatchTeamStats['blocks'] = int(safe_get(pbp_dict,'tm.%s.tot_sBlocks' % key))
                            BkMatchTeamStats['turnovers'] = int(safe_get(pbp_dict,'tm.%s.tot_sTurnovers' % key))
                            BkMatchTeamStats['personal_fouls'] = int(safe_get(pbp_dict,'tm.%s.tot_sFoulsPersonal' % key))
                            BkMatchTeamStats['point'] = int(safe_get(pbp_dict,'tm.%s.tot_sPoints' % key))
                            team_stats_list.append(BkMatchTeamStats)
                            player_keys = pbp_dict['tm'][key]['pl'].keys()
                            for player_key in player_keys:
                                player = {}
                                player['belong'] = int(key)
                                player_name = pbp_dict['tm'][key]['pl'][player_key]['internationalFirstName'] + ' ' + \
                                              pbp_dict['tm'][key]['pl'][player_key]['internationalFamilyName']
                                if player_name.lower() in self.get_player_id.keys():
                                    player['player_id'] = int(self.get_player_id[player_name.lower()])
                                else:
                                    player_upsert = {}
                                    player_upsert['name_en'] = player_name
                                    try:
                                        player_upsert['logo'] = pbp_dict['tm'][key]['pl'][player_key]['photoS']
                                    except:
                                        player_upsert['logo'] = ''
                                    player_upsert['shirt_number'] = pbp_dict['tm'][key]['pl'][player_key]['shirtNumber']
                                    player_upsert['position'] = pbp_dict['tm'][key]['pl'][player_key]['playingPosition']
                                    player_upsert['short_name_en'] = pbp_dict['tm'][key]['pl'][player_key]['name']
                                    player['player_id'] = get_player_id_upsert(player_upsert)
                                player['player_name'] = player_name
                                try:
                                    minutes = pbp_dict['tm'][key]['pl'][player_key]['sMinutes']
                                    minute = minutes.split(':')[0]
                                    second = minutes.split(':')[1]
                                except:
                                    minutes = '0:00'
                                    minute = 0
                                    second = 0
                                if int(second) >= 30:
                                    player['minutes'] = int(minute) + 1
                                else:
                                    player['minutes'] = int(minute)
                                player['goals'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sFieldGoalsMade' % (key,player_key)))
                                player['field'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sFieldGoalsAttempted' % (key,player_key)))
                                player['two_points_goals'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sTwoPointersMade' % (key,player_key)))
                                player['two_points_total'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sTwoPointersAttempted' % (key,player_key)))
                                player['three_point_goals'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sThreePointersMade' % (key,player_key)))
                                player['three_point_field'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sThreePointersAttempted' % (key,player_key)))
                                player['free_throw_goals'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sFreeThrowsMade' % (key,player_key)))
                                player['free_throw_field'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sFreeThrowsAttempted' % (key,player_key)))
                                player['offensive_rebounds'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sReboundsOffensive' % (key,player_key)))
                                player['defensive_rebounds'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sReboundsDefensive' % (key,player_key)))
                                player['rebounds'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sReboundsTotal' % (key,player_key)))
                                player['assists'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sAssists' % (key,player_key)))
                                player['steals'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sSteals' % (key,player_key)))
                                player['blocks'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sBlocks' % (key,player_key)))
                                player['turnovers'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sTurnovers' % (key,player_key)))
                                player['personal_fouls'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sFoulsPersonal' % (key,player_key)))
                                player['point'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.sPoints' % (key,player_key)))
                                player['first_publish'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.starter' % (key,player_key)))
                                player['shirt_number'] = int(safe_get(pbp_dict,'tm.%s.pl.%s.shirtNumber' % (key,player_key)))
                                if minutes == '0:00':
                                    player['enter_ground'] = 0
                                elif minutes != '0:00':
                                    player['enter_ground'] = 1
                                else:
                                    player['enter_ground'] = 0
                                if int(pbp_dict['tm'][key]['pl'][player_key]['active']) == 0:
                                    player['on_ground'] = 1
                                else:
                                    player['on_ground'] = 0
                                player_stats_list.append(player)
                        except:
                            logger.error(traceback.format_exc())
                        try:
                            for pbp_shot in pbp_dict['tm'][key]['shot']:
                                shot_location = (pbp_shot['y'], pbp_shot['x'])
                                actionNumber_shot_dict[pbp_shot['actionNumber']] = shot_location
                        except:
                            actionNumber_shot_dict = {}
                    for pbp_info in pbp_dict['pbp'][::-1]:
                        if 'OVERTIME' in pbp_info['periodType']:
                            period = pbp_info['period'] + 4
                        else:
                            period = pbp_info['period']
                        type = 0
                        home_score = pbp_info['s1']
                        away_score = pbp_info['s2']
                        belong = pbp_info['tno']
                        actionNumber = pbp_info['actionNumber']
                        try:
                            if round(actionNumber_shot_dict[actionNumber][1]) < 50:
                                location_y = (round(actionNumber_shot_dict[actionNumber][1]) * 0.01 * 70)
                            else:
                                location_y = (abs(round(actionNumber_shot_dict[actionNumber][1]) - 100) * 0.01 * 70)
                            location_x = (round(actionNumber_shot_dict[actionNumber][0]) * 0.01 * 50) - 1
                        except:
                            location_x = 0
                            location_y = 0
                        try:
                            player_name = pbp_info['firstName'] + ' ' + pbp_info['familyName']
                        except:
                            player_name = ''
                        try:
                            player_ids = int(self.get_player_id[player_name.lower()])
                        except:
                            player_ids = 0
                        period_time = pbp_info['gt']
                        if player_name:
                            if 'jumpball' in pbp_info['actionType']:
                                shooting_play = 0
                                score_value = 0
                                scoring_play = 0
                                word_text = pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + pbp_info[
                                    'actionType'] + ' - ' + pbp_info['subType']
                            else:
                                if pbp_info['scoring'] == 0:
                                    shooting_play = pbp_info['scoring']
                                    score_value = 0
                                    scoring_play = 0
                                    word_text = pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + pbp_info[
                                        'actionType'] + ' ' + pbp_info['subType']
                                elif pbp_info['scoring'] == 1:
                                    if pbp_info['success'] == 0:
                                        shooting_play = pbp_info['scoring']
                                        score_value = 0
                                        scoring_play = 0
                                        word_text = pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                                    pbp_info[
                                                        'actionType'] + ' ' + pbp_info['subType'] + ' ' + 'missed'
                                    elif pbp_info['success'] == 1:
                                        shooting_play = pbp_info['scoring']
                                        if 'f' not in pbp_info['actionType'][0]:
                                            score_value = pbp_info['actionType'][0]
                                        else:
                                            score_value = 0
                                        scoring_play = 1
                                        if pbp_info['lead'] > 0 and pbp_info['tno'] == 1:
                                            word_text = pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                                        pbp_info['actionType'] + ' ' + pbp_info['subType']
                                        elif pbp_info['lead'] > 0 and pbp_info['tno'] == 2:
                                            word_text = pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                                        pbp_info['actionType'] + ' ' + pbp_info['subType']
                                        elif pbp_info['lead'] < 0 and pbp_info['tno'] == 1:
                                            word_text = pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                                        pbp_info['actionType'] + ' ' + pbp_info['subType']
                                        elif pbp_info['lead'] < 0 and pbp_info['tno'] == 2:
                                            word_text = pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
                                                        pbp_info['actionType'] + ' ' + pbp_info['subType']
                                        else:
                                            word_text = pbp_info['firstName'] + ' ' + pbp_info['familyName'] + ',' + \
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
                            'id': int(match_id),
                            'text': word_text_zh,
                            'period': int(period),
                            'type': int(type),
                            'home_score': int(home_score),
                            'away_score': int(away_score),
                            'belong': int(belong),
                            'player_name': player_name,
                            'player_ids': [player_ids],
                            'period_time': str(period_time),
                            'shooting_play': int(shooting_play),
                            'score_value': int(score_value),
                            'scoring_play': int(scoring_play),
                            'text_en': word_text,
                            'location_x': int(location_x),
                            'location_y': int(location_y),
                        }
                        playbyplay_list.append(data)
                    match_data_boxscore = {'match': {'id': int(match_id),
                                                     'basketball_items': {
                                                         'player_stat': {
                                                             'items': player_stats_list},
                                                         'team_stat': {'items': team_stats_list}
                                                     }}}
                    data_queue.put(match_data_boxscore)
                    logger.info('球员技术统计推送完成... %s' % str(match_id))
                    match_data_playbyplay = {'match': {'id': int(match_id),
                                                       'basketball_items': {
                                                           'incident': {
                                                               'period': period_total,
                                                               'items': playbyplay_list}
                                                       }}}
                    data_queue.put(match_data_playbyplay)
                    logger.info('球员技术文字直播推送完成... %s' % str(match_id))
                    try:
                        if playbyplay_list[-1]['text'] == '比赛结束':
                            break
                        else:
                            time.sleep(3)
                            logger.info('休息3s再次请求....')
                    except:
                        time.sleep(3)
                        logger.info('未找到赛节状态。。。')
            except:
                dingding_alter(traceback.format_exc())
                logger.error(traceback.format_exc())
                continue

    def get_match_id(self, data_queue):
        try:
            for key, value in self.get_match_id_start.items():
                threading.Thread(target=pbp_box().pbp_box_live, args=(data_queue, value)).start()
        except:
            dingding_alter(traceback.format_exc())
            logger.error(traceback.format_exc())
