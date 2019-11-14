#服务接收方   接收数据

import asyncio
import time
import traceback

from nats.aio.client import Client
from common.libs.log import LogMgr
from common.libs.pbjson import dict2pb
from pb.nana.biz.base_pb2 import Request, Result
from pb.nana.biz.example import demo_pb2



#-----日志信息-----
logger = LogMgr.get('demo_feed_client')


def now():
    return int(time.time() * 1000)


class DemoFeedClient(object):
    data = dict()

    topic = ''

    cnt = 0

    def __init__(self):
        self.nc = Client()

    async def start(self, topic, servers=None, user=None, password=None):
        self.topic = topic
        await self.nc.connect(servers=servers, user=user, password=password)
        await self.nc.subscribe(topic, cb=self.msg_handler)

        rpc_topic = '%s.rpc' % self.topic

        while True:
            self.cnt += 1

            # 请求时间数据
            req = {
                'code': demo_pb2.SID_DEMO_TIME_REQ,
            }
            req_bin = dict2pb(Request, req).SerializeToString()
            try:
                msg = await self.nc.request(rpc_topic, req_bin)
                print('time', msg.data)
            except Exception:
                logger.error(traceback.format_exc())

            await asyncio.sleep(100)

            # 检查服务是否可用
            if self.cnt % 5 == 0:
                req = {
                    'code': demo_pb2.SID_DEMO_HEARTBEAT_REQ,
                }
                req_bin = dict2pb(Request, req).SerializeToString()
                try:
                    msg = await self.nc.request(rpc_topic, req_bin)
                    print('check', msg.data)
                except Exception:
                    logger.error(traceback.format_exc())

            # 请求服务重启
            # if self.cnt % 8 == 0:
            #     req = {
            #         'code': SID_DEMO_RESTART_REQ,
            #     }
            #     req_bin = dict2pb(Request, req).SerializeToString()
            #     try:
            #         msg = await self.nc.request(rpc_topic, req_bin)
            #         print('restart', msg.data)
            #         await asyncio.sleep(5)
            #         os._exit(1)
            #     except Exception:
            #         logger.error(traceback.format_exc())

            await asyncio.sleep(1)

    # 消息处理
    @classmethod
    async def msg_handler(cls, msg):
        res_pb = Result()
        res_pb.ParseFromString(msg.data)
        print(res_pb)

        # if res_pb.code == demo_pb2.SID_DEMO_TIME_RES:
        #     time_pb = demo_pb2.DemoTimeRes()
        #     time_pb.ParseFromString(res_pb.res)
        #
        #     now_time = now()
        #     print(now_time, now_time - time_pb.time)
