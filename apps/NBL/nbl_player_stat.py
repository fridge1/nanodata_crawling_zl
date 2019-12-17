import json
import traceback
import threading
from apps.NBL.tools import *
import time
from apps.send_error_msg import dingding_alter
from common.libs.log import LogMgr

logger = LogMgr.get('nbl_basketball_player_stats_live')


class player_stats(object):
    def __init__(self):
        self.team_id_get = get_team_id()
        self.player_id_position = get_player_id_position_update()

    def pbp_box_live(self, match_id, match_time, id):
        data = {}
        spx_dev_session = MysqlSvr.get('spider_zl')
        while True:
            headers = {
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            }
            url = 'https://www.fibalivestats.com/data/%s/data.json' % str(match_id)
            pbp_res = requests.get(url, headers=headers)
            if int(match_time) >= int(time.time()) and pbp_res.status_code != 200:
                logger.info('比赛未开赛.... %s' % str(match_id))
                time.sleep(10)
            else:
                pbp_dict = json.loads(pbp_res.text)
                for pbp_info in pbp_dict['tm'].values():
                    team_name = pbp_info['name']
                    for player_box in pbp_info['pl'].values():
                        data["sport_id"] = 2
                        minute = player_box['sMinutes'].split(':')[0]
                        second = player_box['sMinutes'].split(':')[1]
                        if int(second) >= 30:
                            data['minutes_played'] = int(minute) + 1
                        else:
                            data['minutes_played'] = int(minute)
                        data['team_id'] = self.team_id_get[team_name]
                        name_en = player_box['firstName'] + ' ' + player_box['familyName']
                        data['player_id'] = self.player_id_position[str(name_en).lower()][0]
                        data['position'] = player_box['playingPosition']
                        if player_box['starter'] == 0:
                            data['first'] = 1
                        else:
                            data['first'] = 0
                        data['match_id'] = match_id
                        data['points'] = player_box['sPoints']
                        data['free_throws_scored'] = player_box['sFreeThrowsMade']
                        data['free_throws_total'] = player_box['sFreeThrowsAttempted']
                        data['free_throws_accuracy'] = player_box['sFreeThrowsPercentage']
                        data['two_points_scored'] = player_box['sTwoPointersMade']
                        data['two_points_total'] = player_box['sTwoPointersAttempted']
                        data['two_points_accuracy'] = player_box['sTwoPointersPercentage']
                        data['three_points_scored'] = player_box['sThreePointersMade']
                        data['three_points_total'] = player_box['sThreePointersAttempted']
                        data['three_points_accuracy'] = player_box['sThreePointersPercentage']
                        data['field_goals_scored'] = player_box['sFieldGoalsMade']
                        data['field_goals_total'] = player_box['sFieldGoalsAttempted']
                        data['field_goals_accuracy'] = player_box['sFieldGoalsPercentage']
                        data['rebounds'] = player_box['sReboundsTotal']
                        data['defensive_rebounds'] = player_box['sReboundsDefensive']
                        data['offensive_rebounds'] = player_box['sReboundsOffensive']
                        data['assists'] = player_box['sAssists']
                        data['turnovers'] = player_box['sTurnovers']
                        data['steals'] = player_box['sSteals']
                        data['blocks'] = player_box['sBlocks']
                        data['personal_fouls'] = player_box['sFoulsPersonal']
                        data['id'] = id
                        logger.info(data)
                        BleagueNblBasketballPlayerStats.upsert(
                            spx_dev_session,
                            'id',
                            data
                        )
                        id += 1
            spx_dev_session.close()

    def get_match_id_player_stats(self):
        try:
            url = 'https://api.nbl.com.au/_/custom/api/genius?route=competitions/24346/matches&matchType=REGULAR&limit=200&fields=matchId,matchStatus,matchTimeUTC,competitors,roundNumber,venue,ticketURL&liveapidata=false&filter[owner]=nbl'
            headers = {
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            }
            res = requests.get(url, headers=headers)
            match_dict = json.loads(res.text)
            id = 1
            for id_time in match_dict['data']:
                match_id = id_time['matchId']
                match_time = change_bjtime(id_time['matchTimeUTC'])
                threading.Thread(target=player_stats().pbp_box_live, args=(match_id, match_time, id)).start()
        except:
            dingding_alter(traceback.format_exc())
            logger.error(traceback.format_exc())
