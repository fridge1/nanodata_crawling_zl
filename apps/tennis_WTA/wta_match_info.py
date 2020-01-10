import requests
import json
import re
from orm_connection.orm_session import MysqlSvr
from orm_connection.tennis import TennisMatch


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
            'F':12,
            'U':1,
            'P':1,
            'M':1,
            'C':12,
            'W':1,
        }
        self.type_id = {
            'D': 2,
            'S': 1,
        }
        self.session = MysqlSvr.get('spider_zl')



    def get_competition_season(self,year):
        url = 'https://api.wtatennis.com/tennis/tournaments/?page=0&pageSize=100&excludeLevels=ITF&from=%s-01-01&to=%s-12-31' % (year,year)
        res = requests.get(url,headers=self.headers)
        infos = json.loads(res.text)
        for info in infos['content']:
            season_id = info['year']
            competition_id = info['tournamentGroup']['id']
            surface = self.surface_dict[info['surface']]
            match_url = 'https://api.wtatennis.com/tennis/tournaments/%s/%s/matches/' % (competition_id,season_id)
            match_res = requests.get(match_url,headers=self.headers)
            match_infos = json.loads(match_res.text)
            for info in match_infos['matches']:
                try:
                    match_info = {}
                    match_info['surface'] = int(surface)
                    match_info['key'] = str(season_id) + str(competition_id) + str(info['MatchID'])
                    match_info['sport_id'] = 3
                    match_info['competition_id'] = str(season_id) + str(competition_id)
                    match_info['season_id'] = season_id
                    match_info['type'] = self.type_id[info['DrawMatchType']]
                    if match_info['type'] == 2:
                        match_info['home_player_id'] = str([int(info['PlayerIDA']),int(info['PlayerIDA2'])])
                        match_info['away_player_id'] = str([int(info['PlayerIDB']),int(info['PlayerIDB2'])])
                    else:
                        match_info['home_player_id'] = str([int(info['PlayerIDA'])])
                        match_info['away_player_id'] = str([int(info['PlayerIDB'])])
                    ScoreString = info['ScoreString']
                    if "Ret'd" in ScoreString:
                        match_info['status_id'] = 15
                    else:
                        match_info['status_id'] = self.status_id[info['MatchState']]
                    if match_info['status_id'] == 1:
                        match_info['home_player_score'] = str([])
                        match_info['away_player_score'] = str([])
                    else:
                        score_infos = ScoreString.split(',')
                        home_player_score = []
                        away_player_score = []
                        for score_info in score_infos:
                            match_score = score_info.split('-')
                            if '(' in match_score[0]:
                                home_score = re.findall(r'\d+',match_score[0])
                                home_player_score += home_score
                            else:
                                score = 0
                                home_score = match_score[0]
                                home_player_score.append(int(home_score))
                                home_player_score.append(score)
                            if '(' in match_score[1]:
                                away_score = re.findall(r'\d+',match_score[1])
                                away_player_score += away_score
                            else:
                                score = 0
                                away_score = match_score[1]
                                away_player_score.append(int(away_score))
                                away_player_score.append(score)
                            match_info['home_player_score'] = str(home_player_score)
                            match_info['away_player_score'] = str(away_player_score)
                    TennisMatch.upsert(
                        self.session,
                        'key',
                        match_info
                    )
                    print(match_info)
                except:
                    continue

    def run(self):
        for year in range(2016,2021):
            self.get_competition_season(year)



