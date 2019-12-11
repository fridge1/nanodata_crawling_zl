import requests
import json
from apps.NBL.tools import *
import traceback

headers = {
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
}
season_id_list = get_season_id()
for season_id in season_id_list:
    url = 'https://api.nbl.com.au/_/custom/api/genius?route=competitions/%s/matches&matchType=REGULAR&limit=200&fields=matchId,matchStatus,matchTimeUTC,competitors,roundNumber,venue,ticketURL&liveapidata=false&filter[owner]=nbl' % str(
        season_id)
    res = requests.get(url, headers=headers)
    res_dict = json.loads(res.text)
    season = res_dict['data'][0]['matchTimeUTC'].split('-')[0] + '-' + str(
        int(res_dict['data'][0]['matchTimeUTC'].split('-')[0]) + 1)
    round_count = res_dict['data'][-1]['roundNumber']
    sport_id = 2
    name_zh = str(season) + '常规赛'
    mode = 5
    season_data = {
        'season_id': season_id,
        'name_zh': name_zh,
        'sport_id': sport_id,
        'mode': mode,
        'round_count': round_count,
    }
    spx_dev_session = MysqlSvr.get('spider_zl')
    BleagueNblBasketballStage.upsert(
        spx_dev_session,
        'season_id',
        season_data
    )
