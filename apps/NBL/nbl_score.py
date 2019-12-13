from aiohttp import ClientSession
import aiohttp
import json




class GetScores(object):
    async def get_scores(self,game_id):
        url = 'https://www.fibalivestats.com/data/%s/data.json' % str(game_id)
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with ClientSession(connector=conn) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    response = await response.text()
                    player_stat = json.loads(response)
                    try:
                        scores_info = player_stat['pbp'][0]
                        home_scores = scores_info['s1']
                        away_scores = scores_info['s2']
                        if player_stat['inOT'] != 0:
                            period = scores_info['period'] + 4
                        else:
                            period = scores_info['period']
                        match_time = scores_info['gt']
                        if period < 5:
                            if match_time == '00:00':
                                status_id = 2*period + 1
                            else:
                                status_id = 2 * period
                        else:
                            status_id = 9
                        data = {
                            'sport_id': 2,
                            'site': 'bt',
                            'matches': {
                                game_id: {
                                    'score': {
                                        'tmr': {'ticking': 0, 'coundown': 1, 'addtime': 0, 'second': match_time},
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










