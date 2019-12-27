import requests
import json

from common.libs.log import LogMgr

logger = LogMgr.get('eur_basketball_score_live')


headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
url = 'https://live.euroleague.net/api/Boxscore?gamecode=100&seasoncode=E2019&disp='
res = requests.get(url,headers=headers)
if res.text == '':
    logger.info('比赛未开赛。。。')
else:
    a = json.loads(res.text)


data = {
    'sport_id': 2,
    'site': 'bt',
    'matches': {
        match_id: {
            'score': {
                'tmr': {'ticking': 0, 'coundown': 1, 'addtime': 0, 'second': match_time},
                'status_id': status_id,
                'home_scores': home_scores,
                'away_scores': away_scores,
            }
        }
    }
}



