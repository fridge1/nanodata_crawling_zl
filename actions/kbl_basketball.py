import asyncio
from apps.kbl.kbl_client import KblBasketballFeedClient
from apps.kbl.kbl_svr import KblBasketballFeedSvr
from apps.kbl.kbl_match import match_info

servers = ["nats://hub.nats.namincs.com:4222"]
user = 'nana'
password = 'aa123456'

def start_kbl_basketball_svr(opts):
    topic = 'kbl.bk.live'
    asyncio.run(KblBasketballFeedSvr().start(topic=topic))


def start_kbl_basketball_client(opts):
    topic = 'kbl.bk.live'
    asyncio.run(KblBasketballFeedClient().start(topic=topic))


def start_kbl_basketball_match(opts):
    match_info().run()




kbl_basketball_actions = {
    'start_kbl_basketball_match' : start_kbl_basketball_match,
    'start_kbl_basketball_svr' : start_kbl_basketball_svr,
    'start_kbl_basketball_client' : start_kbl_basketball_client,
}