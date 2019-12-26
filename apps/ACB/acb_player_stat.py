import requests
from orm_connection.orm_session import MysqlSvr
import time
import json
from orm_connection.acb_basketball import BleagueAcbBasketballPlayerStats,BleagueAcbBasketballPlayer
from apps.ACB.tools import get_team_id,get_player_id_position_update,tree_parse


class GetPlayerStat(object):
    def __init__(self):
        self.team_id_get = get_team_id()
        self.player_id_position = get_player_id_position_update()
        self.id = 1


    def pbp_box_live(self,match_id):
        data = {}
        spx_dev_session = MysqlSvr.get('spider_zl')
        headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
        url = 'https://www.fibalivestats.com/data/%s/data.json' % str(match_id)
        pbp_res = requests.get(url, headers=headers)
        if pbp_res.status_code != 200:
            print('比赛未开赛.... %s' % str(match_id))
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
                    data['team_id'] = self.team_id_get[team_name.lower()]
                    name_en = player_box['firstName'] + ' ' + player_box['familyName']
                    if str(name_en).lower() in self.player_id_position.keys():
                        data['player_id'] = self.player_id_position[str(name_en).lower()][0]
                    else:
                        data_upsert = {}
                        data_upsert['name_en'] = name_en
                        _,row = BleagueAcbBasketballPlayer.upsert(
                            spx_dev_session,
                            'name_en',
                            data_upsert
                        )
                        data['player_id'] = row.id
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
                    data['id'] = self.id
                    BleagueAcbBasketballPlayerStats.upsert(
                        spx_dev_session,
                        'id',
                        data
                    )
                    self.id += 1
                    print(data)
            spx_dev_session.close()


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
                    self.pbp_box_live(match_id)


if __name__ == '__main__':
    GetPlayerStat().get_match_info()
