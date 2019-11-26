import requests
import json
from apps.NBL.tools import *
import traceback

headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
url = 'https://api.nbl.com.au/_/custom/api/genius?route=leagues/7/competitions&competitionName=NBL&fields=season,competitionId&limit=500&filter[owner]=nbl'
res = requests.get(url,headers=headers)
res_dict = json.loads(res.text)
for data in res_dict['data']:
    id = data['competitionId']
    season = data['season']
    competition_id = 7
    sport_id = 2
    name_zh = str(season)+'常规赛'
    has_player_stats = 1
    has_team_stats = 1
    season_data = {
        'id' : id,
        'season' : season,
        'competition_id' : competition_id,
        'name_zh' : name_zh,
        'has_player_stats' : has_player_stats,
        'has_team_stats' : has_team_stats,
        'sport_id' : sport_id
    }
    spx_dev_session = MysqlSvr.get('spider_zl')
    BleagueNblBasketballSeason.upsert(
        spx_dev_session,
        'id',
        season_data
    )