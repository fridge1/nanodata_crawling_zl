import requests
import json
from apps.tennis_WTA.tools import safe_get
import re
from orm_connection.orm_session import MysqlSvr
from orm_connection.tennis import TennisMatch
from apps.tennis_WTA.tools import change_match_bjtime


class GetMatchInfo(object):
    def __init__(self):
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.surface_dict = {
            'Hard': 1,
            'Clay': 2,
            'Grass': 3,
        }
        self.status_id = {
            'F':10,
            'U':1,
            'P':1,
            'M':1,
            'C':10,
            'W':1,
        }
        self.type_id = {
            'D': 2,
            'S': 1,
        }
        self.session = MysqlSvr.get('spider_zl')

    def get_match_api_info(self):
        api_url = 'https://api.wtatennis.com/tennis/matches/global'
        res = requests.get(api_url,headers=self.headers)
        match_infos = json.loads(res.text)
        for info in match_infos:
            match_info = {}
            match_info['season_id'] = info['EventYear']
            match_info['key'] = str(match_info['season_id']) + str(info['EventID']) + str(info['MatchID'])
            print(match_info['key'])
            match_info['sport_id'] = 3
            match_info['competition_id'] = str(match_info['season_id']) + str(info['Tournament']['tournamentGroup']['id'])
            match_info['surface'] = self.surface_dict[info['Tournament']['surface']]
            match_info['status_id'] = self.status_id[info['MatchState']]
            match_info['type'] = self.type_id[info['DrawMatchType']]
            if  match_info['type'] == 1:
                match_info['home_player_id'] = str([int(info['PlayerIDA'])])
                match_info['away_player_id'] = str([int(info['PlayerIDB'])])
            else:
                match_info['home_player_id'] = str([int(info['PlayerIDA']),int(info['PlayerIDA2'])])
                match_info['away_player_id'] = str([int(info['PlayerIDB']),int(info['PlayerIDB2'])])
            if match_info['status_id'] == 10:
                ScoreString = safe_get(info,'ScoreString')
                ScoreString_infos = str(ScoreString).split(',')
                home_player_score_list = []
                away_player_score_list = []
                for ScoreString_info in ScoreString_infos:
                    home_player_score_info = ScoreString_info.split('-')[0]
                    if '(' in home_player_score_info:
                        score = re.findall(r'\d+',home_player_score_info)[1]
                        home_player_score = re.findall(r'\d+',home_player_score_info)[0]
                    else:
                        score = 0
                        home_player_score = home_player_score_info
                    home_player_score_list.append(int(home_player_score))
                    home_player_score_list.append(int(score))
                    away_player_score_info = ScoreString_info.split('-')[1]
                    if "Ret'd" in away_player_score_info:
                        match_info['abandon_type'] = 1
                    else:
                        match_info['abandon_type'] = 0
                    if '(' in away_player_score_info:
                        score = re.findall(r'\d+', away_player_score_info)[1]
                        away_player_score = re.findall(r'\d+', away_player_score_info)[0]
                    else:
                        away_player_score = away_player_score_info
                        score = 0
                    away_player_score_list.append(int(re.findall(r'\d+', away_player_score)[0]))
                    away_player_score_list.append(int(score))
            else:
                home_player_score_list = 0
                away_player_score_list = 0
            match_info['home_player_score'] = str(home_player_score_list)
            match_info['away_player_score'] = str(away_player_score_list)
            match_time = info['MatchTimeStamp'].split('+')[0].replace('T',' ')
            match_info['match_time'] = change_match_bjtime(match_time)
            TennisMatch.upsert(
                self.session,
                'key',
                match_info
            )
            print(match_info)


if __name__ == '__main__':
    GetMatchInfo().get_match_api_info()
