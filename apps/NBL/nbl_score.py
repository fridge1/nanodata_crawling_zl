from aiohttp import ClientSession
import aiohttp
import json
import traceback


class GetScores(object):
    async def get_scores(self, game_id):
        url = 'https://www.fibalivestats.com/data/%s/data.json' % str(game_id)
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with ClientSession(connector=conn) as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        response = await response.text()
                        player_stat = json.loads(response)
                        try:
                            scores_info = player_stat['pbp'][0]
                            try:
                                home_p1_score = player_stat['tm']['1']['p1_score']
                            except:
                                home_p1_score = 0
                            try:
                                home_p2_score = player_stat['tm']['1']['p2_score']
                            except:
                                home_p2_score = 0
                            try:
                                home_p3_score = player_stat['tm']['1']['p3_score']
                            except:
                                home_p3_score = 0
                            try:
                                home_p4_score = player_stat['tm']['1']['p4_score']
                            except:
                                home_p4_score = 0
                            try:
                                home_p5_score = player_stat['tm']['1']['p5_score']
                            except:
                                home_p5_score = 0

                            try:
                                away_p1_score = player_stat['tm']['2']['p1_score']
                            except:
                                away_p1_score = 0
                            try:
                                away_p2_score = player_stat['tm']['2']['p2_score']
                            except:
                                away_p2_score = 0
                            try:
                                away_p3_score = player_stat['tm']['2']['p3_score']
                            except:
                                away_p3_score = 0
                            try:
                                away_p4_score = player_stat['tm']['2']['p4_score']
                            except:
                                away_p4_score = 0
                            try:
                                away_p5_score = player_stat['tm']['2']['p5_score']
                            except:
                                away_p5_score = 0

                            home_scores = [home_p1_score,home_p2_score,home_p3_score,home_p4_score,home_p5_score]
                            away_scores = [away_p1_score,away_p2_score,away_p3_score,away_p4_score,away_p5_score]
                            if player_stat['inOT'] != 0:
                                period = scores_info['period'] + 4
                            else:
                                period = scores_info['period']
                            match_time = scores_info['gt']
                            minutes = match_time.split(':')[0]
                            second = match_time.split(':')[1]
                            seconds = int(minutes) * 60 + int(second)
                            if period < 5:
                                if match_time == '00:00':
                                    status_id = 2 * period + 1
                                else:
                                    status_id = 2 * period
                            else:
                                status_id = 9
                            data = {
                                'sport_id': 2,
                                'site': 'nbl',
                                'matches': {
                                    game_id: {
                                        'score': {
                                            'tmr': {'ticking': 0, 'coundown': 1, 'addtime': 0, 'second': seconds},
                                            'status_id': status_id,
                                            'home_scores': home_scores,
                                            'away_scores': away_scores,
                                        }
                                    }
                                }
                            }
                            return data
                        except:
                            return 0
                    else:
                        return 0
            except:
                return 0
