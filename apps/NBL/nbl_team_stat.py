import requests
import json
import traceback
import threading
from apps.NBL.nbl_tools import translate
from apps.NBL.tools import *
import time
from apps.send_error_msg import dingding_alter
from common.libs.log import LogMgr

logger = LogMgr.get('nbl_basketball_team_stat')


class nbl_team_stat(object):
    def __init__(self):
        self.team_id_get = get_team_id()

    def team_stat(self, match_id, match_time):
        headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
        url = 'https://www.fibalivestats.com/data/%s/data.json' % str(match_id)
        logger.info(url)
        pbp_res = requests.get(url, headers=headers)
        if int(match_time) >= int(time.time()) and pbp_res.status_code != 200:
            logger.info('比赛未开赛.... %s' % str(match_id))
            time.sleep(10)
        else:
            pbp_dict = json.loads(pbp_res.text)
            keys = pbp_dict['tm'].keys()
            for key in keys:
                BkMatchTeamStats = {}
                try:
                    BkMatchTeamStats['team_id'] = self.team_id_get[str(pbp_dict['tm'][key]['name'])]
                except:
                    BkMatchTeamStats['team_id'] = 0
                BkMatchTeamStats['match_id'] = match_id
                BkMatchTeamStats['id'] = int(str(match_id) + str(BkMatchTeamStats['team_id']))
                BkMatchTeamStats['field_goals_scored'] = safe_get(pbp_dict,'tm.%s.tot_sFieldGoalsMade' % key)
                BkMatchTeamStats['field_goals_total'] = safe_get(pbp_dict,'tm.%s.tot_sFieldGoalsAttempted' % key)
                BkMatchTeamStats['two_pointers_scored'] = safe_get(pbp_dict,'tm.%s.tot_sTwoPointersMade' % key)
                BkMatchTeamStats['two_pointers_total'] = safe_get(pbp_dict,'tm.%s.tot_sTwoPointersAttempted' % key)
                BkMatchTeamStats['three_pointers_scored'] = safe_get(pbp_dict,'tm.%s.tot_sThreePointersMade' % key)
                BkMatchTeamStats['three_pointers_total'] = safe_get(pbp_dict,'tm.%s.tot_sThreePointersAttempted' % key)
                BkMatchTeamStats['free_throws_scored'] = safe_get(pbp_dict,'tm.%s.tot_sFreeThrowsMade' % key)
                BkMatchTeamStats['free_throws_total'] = safe_get(pbp_dict,'tm.%s.tot_sFreeThrowsAttempted' % key)
                BkMatchTeamStats['offensive_rebounds'] = safe_get(pbp_dict,'tm.%s.tot_sReboundsOffensive' % key)
                BkMatchTeamStats['defensive_rebounds'] = safe_get(pbp_dict,'tm.%s.tot_sReboundsDefensive' % key)
                BkMatchTeamStats['rebounds'] = safe_get(pbp_dict,'tm.%s.tot_sReboundsTotal' % key)
                BkMatchTeamStats['assists'] = safe_get(pbp_dict,'tm.%s.tot_sAssists' % key)
                BkMatchTeamStats['steals'] = safe_get(pbp_dict,'tm.%s.tot_sSteals' % key)
                BkMatchTeamStats['blocks'] = safe_get(pbp_dict,'tm.%s.tot_sBlocks' % key)
                BkMatchTeamStats['turnovers'] = safe_get(pbp_dict,'tm.%s.tot_sTurnovers' % key)
                BkMatchTeamStats['total_fouls'] = safe_get(pbp_dict,'tm.%s.tot_sFoulsOn' % key)
                BkMatchTeamStats['sport_id'] = 2
                if BkMatchTeamStats['field_goals_total'] == 0:
                    BkMatchTeamStats['field_goals_accuracy'] = 0
                else:
                    BkMatchTeamStats['field_goals_accuracy'] = round(
                        (BkMatchTeamStats['field_goals_scored'] / BkMatchTeamStats['field_goals_total']) * 100)
                if BkMatchTeamStats['two_pointers_total'] == 0:
                    BkMatchTeamStats['two_pointers_accuracy'] = 0
                else:
                    BkMatchTeamStats['two_pointers_accuracy'] = round(
                        (BkMatchTeamStats['two_pointers_scored'] / BkMatchTeamStats['two_pointers_total']) * 100)
                if BkMatchTeamStats['three_pointers_total'] == 0:
                    BkMatchTeamStats['three_pointers_accuracy'] = 0
                else:
                    BkMatchTeamStats['three_pointers_accuracy'] = round((BkMatchTeamStats['three_pointers_scored'] /
                                                                         BkMatchTeamStats[
                                                                             'three_pointers_total']) * 100)
                if BkMatchTeamStats['free_throws_total'] == 0:
                    BkMatchTeamStats['free_throws_accuracy'] = 0
                else:
                    BkMatchTeamStats['free_throws_accuracy'] = round(
                        (BkMatchTeamStats['free_throws_scored'] / BkMatchTeamStats['free_throws_total']) * 100)
                spx_dev_session = MysqlSvr.get('spider_zl')
                BleagueNblBasketballTeamStats.upsert(
                    spx_dev_session,
                    'id',
                    BkMatchTeamStats
                )
                print(BkMatchTeamStats)

    def get_match_id(self):
        try:
            competitionId_list = [2254, 9224, 21029, 18527, 24346]
            for competitionId in competitionId_list:
                url = 'https://api.nbl.com.au/_/custom/api/genius?route=competitions/%s/matches&matchType=REGULAR&limit=200&fields=matchId,matchStatus,matchTimeUTC,competitors,roundNumber,venue,ticketURL&liveapidata=false&filter[owner]=nbl' % str(
                    competitionId)
                headers = {
                    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
                }
                res = requests.get(url, headers=headers)
                match_dict = json.loads(res.text)
                for id_time in match_dict['data']:
                    match_id = id_time['matchId']
                    match_time = change_bjtime(id_time['matchTimeUTC'])
                    threading.Thread(target=nbl_team_stat().team_stat, args=(match_id, match_time)).start()
        except:
            dingding_alter(traceback.format_exc())
            logger.error(traceback.format_exc())



if __name__ == '__main__':
    nbl_team_stat().get_match_id()
