import asyncio
import queue
import time
import traceback
from stan.aio.client import Client as STAN
from common.libs.log import LogMgr
from common.libs.pbjson import dict2pb
from common.utils import NatsSvr
from pb.nana.biz.base_pb2 import Request, Result
from pb.nana.biz.example import demo_pb2
from pb.nana.biz.japan_ball import match_pb2
from apps.NBL.nbl_score import GetScores
from apps.NBL.tools import get_match_id_score

def now():
    return int(time.time() * 1000)


# 设置日志
logger = LogMgr.get('NblBasketball_score_svr')


class NblBasketballScore(object):
    data = dict()
    topic = ''
    cnt = 0

    def __init__(self):
        self.data_queue_svr = queue.Queue()
        self.nc = STAN()

    async def start(self, topic):
        self.topic = topic
        self.nc = await NatsSvr.get_stan('hub.nats')
        await self.start_feed_rpc()
        await self.start_feed()

    async def start_feed(self):
        # match_id_list = get_match_id_score()
        match_id_list = [1307453]
        while True:
            coro = [asyncio.create_task(GetScores().get_scores(game_id)) for game_id in match_id_list]
            data = await asyncio.gather(*coro)
            for i in data:
                if i != 0:
                    await self.pub_time_data(self.topic, i)
                    logger.info('球队分数推送成功...')
                else:
                    logger.info('比赛未开赛。。。')

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
                await self.pub_time_data(msg.reply, '')
            elif req_pb.code == demo_pb2.SID_DEMO_HEARTBEAT_REQ:
                await self.pub_check_data(msg.reply)
            elif req_pb.code == demo_pb2.SID_DEMO_RESTART_REQ:
                await self.pub_restart_data(msg.reply)
                await asyncio.sleep(1)
        except Exception:
            # 将异常信息记录到log日志中
            logger.error(traceback.format_exc())

    async def pub_time_data(self, topic, match_data):
        self.cnt += 1
        # print('aaaa')
        data_pb = dict2pb(match_pb2.FibaMatchRes, match_data)
        res = {
            'code': match_pb2.SID_FIBAMATCH_RES,
            'data': data_pb.SerializeToString()
        }
        res_bin = dict2pb(Result, res).SerializeToString()
        await self.nc.publish(topic, res_bin)
        logger.info('推送成功')

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
