import asyncio

from apps.eur_basketball_spider.eur_client import EurBasketballFeedClient
from apps.eur_basketball_spider.eur_svr import EurBasketballFeedSvr

servers = ["nats://hub.nats.namincs.com:4222"]
user = 'nana'
password = 'aa123456'


def start_eur_basketball_svr(opts):
    topic = 'euro.bk.live'
    asyncio.run(EurBasketballFeedSvr().start(topic=topic, servers=servers, user=user, password=password))


def start_eur_basketball_client(opts):
    topic = 'euro.bk.live'
    asyncio.run(EurBasketballFeedClient().start(topic=topic, servers=servers, user=user, password=password))


eur_basketball_actions = {
    'start_eur_basketball_svr': start_eur_basketball_svr,
    'start_eur_basketball_client': start_eur_basketball_client,

}
