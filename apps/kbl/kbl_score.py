from aiohttp import ClientSession
import aiohttp
import json
from apps.kbl.tools import safe_get
from common.libs.log import LogMgr
logger = LogMgr.get('kbl_basketball_score')


class GetScores(object):
    def __init__(self):
        self.period_dict = {
                'Q1': 1,
                'Q2': 2,
                'Q3': 3,
                'Q4': 4,
                'X1': 5,
                'X2': 6,
                'X3': 7,
                'X4': 8,
            }

    async def get_scores(self, game_id, match_id):
        url = 'https://sports.news.naver.com/ajax/game/relayData.nhn?gameId=%s' % str(game_id)
        list_time = []
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with ClientSession(connector=conn) as session:
            async with session.get(url) as response:
                try:
                    response = await response.text()
                    player_stat = json.loads(response)
                    home_team_id = player_stat['home_team']
                    away_team_id = player_stat['away_team']
                    home_p1_score = int(safe_get(player_stat, 'quarter_score.%s.Q1' % home_team_id))
                    home_p2_score = int(safe_get(player_stat, 'quarter_score.%s.Q2' % home_team_id))
                    home_p3_score = int(safe_get(player_stat, 'quarter_score.%s.Q3' % home_team_id))
                    home_p4_score = int(safe_get(player_stat, 'quarter_score.%s.Q4' % home_team_id))
                    home_p5_score = int(safe_get(player_stat, 'quarter_score.%s.X1' % home_team_id)) + int(
                        safe_get(player_stat, 'quarter_score.%s.X2' % home_team_id)) + int(
                        safe_get(player_stat, 'quarter_score.%s.X3' % home_team_id))
                    away_p1_score = int(safe_get(player_stat, 'quarter_score.%s.Q1' % away_team_id))
                    away_p2_score = int(safe_get(player_stat, 'quarter_score.%s.Q2' % away_team_id))
                    away_p3_score = int(safe_get(player_stat, 'quarter_score.%s.Q3' % away_team_id))
                    away_p4_score = int(safe_get(player_stat, 'quarter_score.%s.Q4' % away_team_id))
                    away_p5_score = int(safe_get(player_stat, 'quarter_score.%s.X1' % away_team_id)) + int(
                        safe_get(player_stat, 'quarter_score.%s.X2' % away_team_id)) + int(
                        safe_get(player_stat, 'quarter_score.%s.X3' % away_team_id))
                    home_scores = [home_p1_score, home_p2_score, home_p3_score, home_p4_score, home_p5_score]
                    away_scores = [away_p1_score, away_p2_score, away_p3_score, away_p4_score, away_p5_score]
                    home_scores_total = sum(home_scores)
                    away_scores_total = sum(away_scores)
                    for stage in list(player_stat['live_text']):
                        if 'Q' in stage or 'X' in stage:
                            for minutes_second in player_stat['live_text'][stage]:
                                minute = minutes_second.split(':')[0]
                                second = minutes_second.split(':')[1]
                                period_time = 600 - (int(minute)*60 + int(second))
                                list_time.append(period_time)
                                period = self.period_dict[stage]
                                if period < 5:
                                    if period_time == 0:
                                        status_id = 2 * period + 1
                                    else:
                                        status_id = 2 * period
                                else:
                                    status_id = 9
                                if period_time == 0 and period >= 4 and home_scores_total != away_scores_total:
                                    status_id = 10
                    match_time = list_time[-1]
                    data = {
                        'sport_id': 2,
                        'site': 'kbl',
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
                    return data
                except:
                    logger.info('比赛未开赛。。。%s' % game_id)
                    return 0


