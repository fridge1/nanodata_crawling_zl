# 服务接收方   接收数据

import asyncio
import json
import time
from stan.aio.client import Client as STAN
from google.protobuf.json_format import MessageToDict
from common.libs.log import LogMgr
from common.utils import NatsSvr
from pb.nana.biz.base_pb2 import Request, Result

# -----日志信息-----
from pb.nana.biz.japan_ball import match_pb2

logger = LogMgr.get('demo_feed_client')


def now():
    return int(time.time() * 1000)


class AcbBasketballFeedClient(object):
    data = dict()

    topic = ''

    cnt = 0

    def __init__(self):
        self.nc = STAN()

    async def start(self, topic, servers=None, user=None, password=None):
        self.topic = topic
        self.nc = await NatsSvr.get_stan('hub.nats')
        await self.nc.subscribe(topic, cb=self.msg_handler)
        rpc_topic = '%s.rpc' % self.topic
        while True:
            self.cnt += 1
            await asyncio.sleep(1)

    # 消息处理
    @classmethod
    async def msg_handler(cls, msg):
        res_pb = Result()
        res_pb.ParseFromString(msg.data)
        if res_pb.code == match_pb2.SID_FIBAMATCH_RES:
            match_pb = match_pb2.FibaMatchRes()
            match_pb.ParseFromString(res_pb.data)
            result = MessageToDict(
                match_pb, preserving_proto_field_name=True, including_default_value_fields=True)
            print(json.dumps(result, ensure_ascii=False))
