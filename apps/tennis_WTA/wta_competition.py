import requests
import json
from orm_connection.orm_session import MysqlSvr
from orm_connection.tennis import TennisCompetition
from apps.tennis_WTA.tools import competition_time_stamp,get_city_id,get_country_id,upsert_city,upsert_country




class GetCompetitionInfo(object):
    def __init__(self):
        self.session = MysqlSvr.get('spider_zl')
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.door_dict = {
            'O' : 2,
            'I' : 1,
        }
        self.city_id = get_city_id()
        self.country_id = get_country_id()
        self.surface_id = {
            'Clay' : 2,
            'Hard' : 1,
            'Grass' : 3,
            'Carpet' : 6,
        }


    def competition_info(self,year):
        url = 'https://api.wtatennis.com/tennis/tournaments/?page=0&pageSize=100&excludeLevels=ITF&from=%s-01-01&to=%s-12-31' % (year,year)
        res = requests.get(url=url,headers=self.headers)
        infos = json.loads(res.text)
        for info in infos['content']:
            competition_info = {}
            competition_info['season_id'] = info['year']
            competition_info['id'] = str(info['year']) + str(info['tournamentGroup']['id'])
            competition_info['singlesDrawSize'] = info['singlesDrawSize']
            competition_info['doublesDrawSize'] = info['doublesDrawSize']
            competition_info['prizeMoney'] = info['prizeMoney']
            competition_info['sport_id'] = 3
            competition_info['name_en'] = info['title']
            competition_info['start_time'] = competition_time_stamp(info['startDate'])
            competition_info['end_time'] = competition_time_stamp(info['endDate'])
            competition_info['level'] = info['tournamentGroup']['level']
            competition_info['prizeMoneyCurrency'] = 1
            competition_info['inOutdoor'] = self.door_dict[info['inOutdoor']]
            city_name = info['city']
            country_name = info['country']
            if city_name in list(self.city_id.keys()):
                competition_info['city_id'] = self.city_id[city_name]
            else:
                competition_info['city_id'] = upsert_city(city_name)
            if country_name in list(self.country_id.keys()):
                competition_info['country_id'] = self.country_id[country_name]
            else:
                competition_info['country_id'] = upsert_country(country_name)
            competition_info['has_player_stats'] = 1
            competition_info['surface'] = self.surface_id[info['surface']]
            TennisCompetition.upsert(
                self.session,
                'id',
                competition_info
            )
            print(competition_info)


    def run(self):
        # for year in range(2010,2020):
        self.competition_info(str(2020))






