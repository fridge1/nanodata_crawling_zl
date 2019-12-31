import asyncio
import queue
import time
import threading
from stan.aio.client import Client as STAN
from common.libs.log import LogMgr
from common.libs.pbjson import dict2pb
from common.utils import NatsSvr
from pb.nana.biz.sport import match_pb2
from apps.eur_basketball_spider.eur_send_score import GetEurScore
from apps.eur_basketball_spider.tools import get_match_id_score

def now():
    return int(time.time() * 1000)


# 设置日志
logger = LogMgr.get('EurBasketball_score_svr')


class EurBasketballScore(object):
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
        match_id_list = get_match_id_score()
        for match_id in match_id_list:
            threading.Thread(target=GetEurScore().get_score,args=(self.data_queue_svr, match_id)).start()
        while True:
            data = self.data_queue_svr.get()
            print('get_data+++++++')
            await self.pub_time_data(self.topic, data)
            await asyncio.sleep(0.1)

    async def pub_time_data(self, topic, match_data):
        data_pb = dict2pb(match_pb2.SportsMatchesRes, match_data).SerializeToString()
        print(data_pb)
        await self.nc.publish(topic, data_pb)


