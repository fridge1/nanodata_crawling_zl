
#服务发起方   发送数据
import asyncio
import os
import time

import traceback
from nats.aio.client import Client
from common.libs.pbjson import dict2pb
from pb.nana.biz.base_pb2 import Request, Result
from pb.nana.biz.example import demo_pb2
from apps.eur_basketball_spider import eur_boxscore
from common.libs.log import LogMgr
logger = LogMgr.get('demo_feed')

def now():
    return int(time.time() * 1000)
#设置日志

class DemoFeedSvr(object):
    data = dict()
    topic = 'zl.demo'
    cnt = 0

    def __init__(self):
        self.nc = Client()
    #启动方法
    async def start(self, topic, servers=None, user=None, password=None):
        self.topic = topic
        await self.nc.connect(servers=servers, user=user, password=password)
        await self.start_feed_rpc()
        await self.start_feed()

    async def start_feed(self):
        while True:
            await self.pub_time_data(self.topic)
            await asyncio.sleep(0.1)

    async def start_feed_rpc(self):
        rpc_topic = '%s.rpc' % self.topic
        await self.nc.subscribe(rpc_topic, cb=self.msg_handler, queue='rpc')

    # 消息处理
    async def msg_handler(self, msg):
        try:
            req_pb = Request()
            req_pb.ParseFromString(msg.data)

            print(msg.subject)

            if req_pb.code == demo_pb2.SID_DEMO_TIME_REQ:
                await self.pub_time_data(msg.reply)
            elif req_pb.code == demo_pb2.SID_DEMO_HEARTBEAT_REQ:
                await self.pub_check_data(msg.reply)
            elif req_pb.code == demo_pb2.SID_DEMO_RESTART_REQ:
                await self.pub_restart_data(msg.reply)
                await asyncio.sleep(1)
                os._exit(1)
        except Exception:
            #将异常信息记录到log日志中
            logger.error(traceback.format_exc())

    # 发布时间数据
    async def pub_time_data(self, topic):

        self.cnt += 1

        #数据位置
        data = {
            'cnt' : self.cnt,
            'time': now()
        }

        res = {
            'code': demo_pb2.SID_DEMO_TIME_RES,
            'data' : dict2pb(demo_pb2.DemoTimeRes, data).SerializeToString()
        }
        res_bin = dict2pb(Result, res).SerializeToString()
        await self.nc.publish(topic, res_bin)
        print(data)

    # 发布检查响应
    async def pub_check_data(self, topic):
        result = {
            'code': demo_pb2.SID_DEMO_HEARTBEAT_RES,
        }
        res_bin = dict2pb(Result, result).SerializeToString()
        await self.nc.publish(topic, res_bin)

    # 发布重启响应
    async def pub_restart_data(self, topic):
        result = {
            'code': demo_pb2.SID_DEMO_RESTART_RES,
        }
        res_bin = dict2pb(Result, result).SerializeToString()
        await self.nc.publish(topic, res_bin)
