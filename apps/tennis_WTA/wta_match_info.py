import requests
import json


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
        }
        self.type_id = {
            'D': 2,
            'S': 1,
        }

    def get_match_api_info(self):
        api_url = 'https://api.wtatennis.com/tennis/matches/global'
        res = requests.get(api_url,headers=self.headers)
        match_infos = json.loads(res.text)
        for info in match_infos:
            match_info = {}
            match_info['season_id'] = info['EventYear']
            match_info['key'] = str(match_info['season_id']) + info['MatchID']
            match_info['sport_id'] = 3
            match_info['competition_id'] = int(info['EventID'])
            match_info['surface'] = self.surface_dict[info['surface']]
            match_info['status_id'] = self.status_id[info['MatchState']]
            match_info['type'] = self.type_id[info['DrawMatchType']]
            match_info['key'] = info['MatchID']
            match_info['key'] = info['MatchID']
            match_info['key'] = info['MatchID']
            match_info['key'] = info['MatchID']
            match_info['key'] = info['MatchID']
            match_info['key'] = info['MatchID']
            match_info['key'] = info['MatchID']
