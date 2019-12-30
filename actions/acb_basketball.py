import asyncio
from apps.ACB.acb_client import AcbBasketballFeedClient
from apps.ACB.acb_svr import AcbBasketballFeedSvr
from apps.ACB.abc_match import GetMatchInfo


def start_acb_basketball_svr(opts):
    topic = 'acb.bk.live'
    asyncio.run(AcbBasketballFeedSvr().start(topic))


def start_acb_basketball_client(opts):
    topic = 'acb.bk.live'
    asyncio.run(AcbBasketballFeedClient().start(topic))


def acb_basketball_match(opts):
    GetMatchInfo().run()


acb_basketball_actions = {
    'start_acb_basketball_svr': start_acb_basketball_svr,
    'start_acb_basketball_client': start_acb_basketball_client,
    'acb_basketball_match': acb_basketball_match,
}
