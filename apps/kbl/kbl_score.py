import asyncio
from aiohttp import ClientSession
import aiohttp
import json




class GetScores(object):
    def __init__(self):
        pass

    async def get_scores(self,game_id,match_id):
        url = 'https://sports.news.naver.com/ajax/game/relayData.nhn?gameId=%s' % str(game_id)
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with ClientSession(connector=conn) as session:
            async with session.get(url) as response:
                response = await response.text()
                player_stat = json.loads(response)
                print(json.dumps(player_stat))




        # data = {
        #     'sport_id': 2,
        #     'site': 'bt',
        #     'matches': {
        #         match_id: {
        #             'score': {
        #                 'tmr': {'ticking': 0, 'coundown': 1, 'addtime': 0, 'second': match_time},
        #                 'status_id': status_id,
        #                 'home_scores': home_scores,
        #                 'away_scores': away_scores,
        #             }
        #         }
        #     }
        # }


if __name__ == '__main__':
    a = GetScores()
    asyncio.run(a.get_scores('2019121155063501101','3334'))