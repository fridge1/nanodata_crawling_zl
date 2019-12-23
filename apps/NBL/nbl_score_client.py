import asyncio
import time
from cacheout import Cache
from google.protobuf.json_format import MessageToDict
from stan.aio.client import Client as STAN
from common.utils import NatsSvr
from pb.nana.biz.sport import match_pb2


def now():
    return int(time.time() * 1000)


class NblBasketballScoreClient(object):
    data = dict()
    topic = ''
    cnt = 0

    def __init__(self):
        self.nc = STAN()
        self.cache = Cache()

    async def start(self, topic):
        self.topic = topic
        self.nc = await NatsSvr.get_stan('hub.nats')
        await self.nc.subscribe(topic, cb=self.msg_handler)

        while True:
            await asyncio.sleep(0.1)

    async def msg_handler(self, msg):
        match_pb = match_pb2.SportsMatchesRes()
        match_pb.ParseFromString(msg.data)
        result = MessageToDict(
            match_pb, preserving_proto_field_name=True, including_default_value_fields=True)
        print(result)