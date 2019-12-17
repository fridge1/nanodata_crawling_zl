import asyncio
import queue
import time
from stan.aio.client import Client as STAN
from common.libs.log import LogMgr
from common.libs.pbjson import dict2pb
from common.utils import NatsSvr
from pb.nana.biz.sport import match_pb2
from apps.kbl.kbl_score import GetScores
from apps.kbl.tools import get_match_id_start

def now():
    return int(time.time() * 1000)


# 设置日志
logger = LogMgr.get('KblBasketball_score_svr')


class KblBasketballScore(object):
    data = dict()
    topic = ''
    cnt = 0

    def __init__(self):
        self.data_queue_svr = queue.Queue()
        self.nc = STAN()

    async def start(self, topic):
        self.topic = topic
        self.nc = await NatsSvr.get_stan('hub.nats')
        await self.start_feed()

    async def start_feed(self):
        match_id_dict = get_match_id_start()
        while True:
            coro = [asyncio.create_task(GetScores().get_scores(game_id,match_id)) for game_id,match_id in match_id_dict.items()]
            data = await asyncio.gather(*coro)
            for i in data:
                if i != 0:
                    logger.info(i)
                    await self.pub_time_data(self.topic, i)
                    logger.info('球队分数推送成功...')
                else:
                    logger.info('比赛未开赛。。。')


    async def pub_time_data(self, topic, match_data):
        data_pb = dict2pb(match_pb2.SportsMatchesRes, match_data).SerializeToString()
        await self.nc.publish(topic, data_pb)


