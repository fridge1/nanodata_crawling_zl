import requests
import json

from common.libs.log import LogMgr

logger = LogMgr.get('eur_basketball_score_live')



class GetEurScore(object):

    def get_score(self,data_queue,match_id):
        while True:
            headers = {
                        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
                    }
            url = 'https://live.euroleague.net/api/PlayByPlay?gamecode=%s&seasoncode=E2019&disp=' % str(match_id)[3:]
            res = requests.get(url,headers=headers)
            if res.text == '':
                logger.info('比赛未开赛。。。')
            else:
                home_scores,away_scores,home_score,away_score = self.scores(json.loads(res.text))
                status_id,match_time = self.status(json.loads(res.text),home_score,away_score)
                data = {
                    'sport_id': 2,
                    'site': 'eur',
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
                data_queue.put(data)
                if data['matches'][match_id]['score']['status_id'] == 10:
                    break



    def scores(self,text):
        point_A = 0
        point_B = 0
        home_score = []
        away_score = []
        playbyplay = {}
        keys = list(text.keys())
        for key in keys[6:]:
            for playbyplay_info in text[key]:
                if playbyplay_info['POINTS_A'] != None:
                    playbyplay['POINTS_A'] = playbyplay_info['POINTS_A']
                    point_A = playbyplay['POINTS_A']
                else:
                    playbyplay['POINTS_A'] = point_A
                if playbyplay_info['POINTS_B'] != None:
                    playbyplay['POINTS_B'] = playbyplay_info['POINTS_B']
                    point_B = playbyplay['POINTS_B']
                else:
                    playbyplay['POINTS_B'] = point_B
            home_score.append(playbyplay['POINTS_A'])
            away_score.append(playbyplay['POINTS_B'])
        home_scores = []
        away_scores = []
        home_scores.append(home_score[0])
        away_scores.append(away_score[0])
        for i in range(len(home_score)-1):
            a = home_score[i+1] - home_score[i]
            b = away_score[i+1] - away_score[i]
            home_scores.append(a)
            away_scores.append(b)
        return home_scores,away_scores,home_score[-1],away_score[-1]

    def status(self,text,home_score,away_score):
        playbyplay = {}
        keys = list(text.keys())
        period = 0
        status_id = 0
        match_time = 0
        for key in keys[6:]:
            period += 1
            if text[key]:
                if not text[key][-1]['MARKERTIME']:
                    time = '00:00'
                else:
                    time = text[key][-1]['MARKERTIME']
                playbyplay['match_time'] = time
                match_time = int(playbyplay['match_time'].split(':')[0]) * 60 + int(playbyplay['match_time'].split(':')[1])
            else:
                match_time = 0
            if period <= 4:
                if match_time == 0:
                    status_id = period * 2 + 1
                else:
                    status_id = period * 2
            else:
                status_id = 9
            if match_time == 0 and period >= 4 and home_score != away_score:
                status_id = 10
            else:
                status_id = status_id
        return status_id, match_time






