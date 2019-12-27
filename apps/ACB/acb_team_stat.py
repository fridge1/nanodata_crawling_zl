import requests
from orm_connection.orm_session import MysqlSvr
import time
import json
from orm_connection.acb_basketball import BleagueAcbBasketballTeamStats
from apps.ACB.tools import get_team_id,get_player_id_position_update,tree_parse,safe_get


class GetTeamStat(object):
    def __init__(self):
        self.team_id_get = get_team_id()
        self.player_id_position = get_player_id_position_update()

    def team_stat(self, match_id):
        headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
        url = 'https://www.fibalivestats.com/data/%s/data.json' % str(match_id)
        print(url)
        pbp_res = requests.get(url, headers=headers)
        if pbp_res.status_code != 200:
            time.sleep(10)
        else:
            pbp_dict = json.loads(pbp_res.text)
            keys = pbp_dict['tm'].keys()
            for key in keys:
                BkMatchTeamStats = {}
                try:
                    BkMatchTeamStats['team_id'] = self.team_id_get[str(pbp_dict['tm'][key]['name']).lower()]
                except:
                    BkMatchTeamStats['team_id'] = 0
                BkMatchTeamStats['match_id'] = match_id
                BkMatchTeamStats['id'] = int(str(match_id) + str(BkMatchTeamStats['team_id']))
                BkMatchTeamStats['field_goals_scored'] = safe_get(pbp_dict, 'tm.%s.tot_sFieldGoalsMade' % key)
                BkMatchTeamStats['field_goals_total'] = safe_get(pbp_dict, 'tm.%s.tot_sFieldGoalsAttempted' % key)
                BkMatchTeamStats['two_pointers_scored'] = safe_get(pbp_dict, 'tm.%s.tot_sTwoPointersMade' % key)
                BkMatchTeamStats['two_pointers_total'] = safe_get(pbp_dict, 'tm.%s.tot_sTwoPointersAttempted' % key)
                BkMatchTeamStats['three_pointers_scored'] = safe_get(pbp_dict, 'tm.%s.tot_sThreePointersMade' % key)
                BkMatchTeamStats['three_pointers_total'] = safe_get(pbp_dict,
                                                                    'tm.%s.tot_sThreePointersAttempted' % key)
                BkMatchTeamStats['free_throws_scored'] = safe_get(pbp_dict, 'tm.%s.tot_sFreeThrowsMade' % key)
                BkMatchTeamStats['free_throws_total'] = safe_get(pbp_dict, 'tm.%s.tot_sFreeThrowsAttempted' % key)
                BkMatchTeamStats['offensive_rebounds'] = safe_get(pbp_dict, 'tm.%s.tot_sReboundsOffensive' % key)
                BkMatchTeamStats['defensive_rebounds'] = safe_get(pbp_dict, 'tm.%s.tot_sReboundsDefensive' % key)
                BkMatchTeamStats['rebounds'] = safe_get(pbp_dict, 'tm.%s.tot_sReboundsTotal' % key)
                BkMatchTeamStats['assists'] = safe_get(pbp_dict, 'tm.%s.tot_sAssists' % key)
                BkMatchTeamStats['steals'] = safe_get(pbp_dict, 'tm.%s.tot_sSteals' % key)
                BkMatchTeamStats['blocks'] = safe_get(pbp_dict, 'tm.%s.tot_sBlocks' % key)
                BkMatchTeamStats['turnovers'] = safe_get(pbp_dict, 'tm.%s.tot_sTurnovers' % key)
                BkMatchTeamStats['total_fouls'] = safe_get(pbp_dict, 'tm.%s.tot_sFoulsOn' % key)
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
                BleagueAcbBasketballTeamStats.upsert(
                    spx_dev_session,
                    'id',
                    BkMatchTeamStats
                )
                print(BkMatchTeamStats)


    def get_match_info(self):
        headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        }
        match_url = 'http://jv.acb.com/historico.php?jornada=%s'
        for jornada in range(1, 26):
            match_res = requests.get(match_url % jornada, headers=headers)
            match_tree = tree_parse(match_res)
            match_api_ids = match_tree.xpath('//div[@class="partidos"]/div/@id')
            for match_api_id in match_api_ids:
                match_id = match_api_id.split('-')[-1]
                if match_id:
                    self.team_stat(match_id)


if __name__ == '__main__':
    GetTeamStat().get_match_info()
