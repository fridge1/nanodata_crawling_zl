from aiohttp import ClientSession
import aiohttp
import json
from apps.NBL.tools import safe_get
import time
from common.libs.log import LogMgr


# 设置日志
logger = LogMgr.get('acb_score_svr')


class GetScores(object):
    async def get_scores(self, game_id):
        url = 'https://www.fibalivestats.com/data/%s/data.json' % str(game_id)
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with ClientSession(connector=conn) as session:
            try:
                logger.info('请求前。。。。')
                logger.info(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                async with session.get(url) as response:
                    logger.info('请求后。。。。')
                    logger.info(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                    if response.status == 200:
                        response = await response.text()
                        player_stat = json.loads(response)
                        try:
                            scores_info = player_stat['pbp'][0]
                            home_p1_score = safe_get(player_stat,'tm.1.p1_score')
                            home_p2_score = safe_get(player_stat,'tm.1.p2_score')
                            home_p3_score = safe_get(player_stat,'tm.1.p3_score')
                            home_p4_score = safe_get(player_stat,'tm.1.p4_score')
                            home_p5_score = safe_get(player_stat,'tm.1.p5_score')
                            away_p1_score = safe_get(player_stat,'tm.2.p1_score')
                            away_p2_score = safe_get(player_stat,'tm.2.p2_score')
                            away_p3_score = safe_get(player_stat,'tm.2.p3_score')
                            away_p4_score = safe_get(player_stat,'tm.2.p4_score')
                            away_p5_score = safe_get(player_stat,'tm.2.p5_score')
                            home_scores = [home_p1_score,home_p2_score,home_p3_score,home_p4_score,home_p5_score]
                            away_scores = [away_p1_score,away_p2_score,away_p3_score,away_p4_score,away_p5_score]
                            home_scores_total = sum(home_scores)
                            away_scores_total = sum(away_scores)
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
                            if seconds == 0 and period >= 4 and home_scores_total != away_scores_total:
                                status_id = 10
                            data = {
                                'sport_id': 2,
                                'site': 'acb',
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
