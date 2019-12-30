import asyncio
from apps.ACB.acb_client import AcbBasketballFeedClient
from apps.ACB.acb_svr import AcbBasketballFeedSvr
from apps.ACB.abc_match import GetMatchInfo
from apps.ACB.acb_score_svr import AcbBasketballScore


def start_acb_basketball_svr(opts):
    topic = 'acb.bk.live'
    asyncio.run(AcbBasketballFeedSvr().start(topic))


def start_acb_basketball_client(opts):
    topic = 'acb.bk.live'
    asyncio.run(AcbBasketballFeedClient().start(topic))


def acb_basketball_match(opts):
    GetMatchInfo().run()


def start_acb_basketball_score_svr(opts):
    topic = 'bk.score.live'
    asyncio.run(AcbBasketballScore().start(topic))


acb_basketball_actions = {
    'start_acb_basketball_svr': start_acb_basketball_svr,
    'start_acb_basketball_client': start_acb_basketball_client,
    'acb_basketball_match': acb_basketball_match,
    'start_acb_basketball_score_svr': start_acb_basketball_score_svr,
}
