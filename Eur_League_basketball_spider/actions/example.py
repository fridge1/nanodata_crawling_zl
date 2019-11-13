import asyncio
from apps.example.demo import DemoFeedSvr
from apps.example.demo_client import DemoFeedClient


servers = ["nats://nats.namincs.com:4222"]
user = 'nana'
password = 'aa123456'


def start_demo_feed_svr(opts):
    topic = 'example.demo'
    asyncio.run(DemoFeedSvr().start(topic=topic, servers=servers, user=user, password=password))


def start_demo_feed_client(opts):
    topic = 'example.demo'
    asyncio.run(DemoFeedClient().start(topic=topic, servers=servers, user=user, password=password))


example_actions = {
    'start_demo_feed_svr'   : start_demo_feed_svr,
    'start_demo_feed_client': start_demo_feed_client,

}
