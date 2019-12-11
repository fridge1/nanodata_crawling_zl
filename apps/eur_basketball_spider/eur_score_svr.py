import asyncio
import queue
import time
import traceback
# from spx_msg.schema.comm import match_pb2
from stan.aio.client import Client as STAN
import threading

from apps.eur_basketball_spider.eur_send_score import match_end
from common.utils import NatsSvr
from pb.nana.biz.japan_ball import match_pb2
from common.libs.pbjson import dict2pb
from common.libs.log import LogMgr

logger = LogMgr.get('eur_basketball_score_svr')


def now():
    return int(time.time() * 1000)


class BeitaiCbaScroeFeedSvr(object):
    data = dict()
    topic = ''
    cnt = 0

    def __init__(self):
        self.nc = STAN()
        self.cln = 1
        self.data_queue = queue.Queue()

    async def start(self, topic):
        self.topic = topic
        self.nc = await NatsSvr.get_stan('hub.nats')
        await self.start_feed()
        await self.match_data()

    def match_data(self):
        match_end(self.data_queue)  # 跟新 问题

    async def start_feed(self):
        t = threading.Thread(target=self.match_data, args=())
        t.setDaemon(True)
        t.start()
        while True:
            data = self.data_queue.get()
            await self.pub_match_data(self.topic, data)

    async def pub_match_data(self, topic, match):
        data_pb = dict2pb(match_pb2.SportsMatchesRes, match).SerializeToString()
        print(data_pb)
        await self.nc.publish(topic, data_pb)
