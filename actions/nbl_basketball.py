import asyncio
from apps.NBL.nbl_client import NblBasketballFeedClient
from apps.NBL.nbl_svr import NblBasketballFeedSvr
from apps.NBL.nbl_match import *



def start_nbl_basketball_svr(opts):
    topic = 'nbl.bk.live'
    asyncio.run(NblBasketballFeedSvr().start(topic))


def start_nbl_basketball_client(opts):
    topic = 'nbl.bk.live'
    asyncio.run(NblBasketballFeedClient().start(topic))

def start_nbl_basketball_match(opts):
    match_live()





nbl_basketball_actions = {
    'start_nbl_basketball_svr': start_nbl_basketball_svr,
    'start_nbl_basketball_client': start_nbl_basketball_client,
    'start_nbl_basketball_match' : start_nbl_basketball_match
}