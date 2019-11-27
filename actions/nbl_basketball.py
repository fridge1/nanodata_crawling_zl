import asyncio
from apps.NBL.nbl_client import NblBasketballFeedClient
from apps.NBL.nbl_svr import NblBasketballFeedSvr
from apps.NBL import nbl_match
from apps.NBL import nbl_spider
from apps.NBL.nbl_player_stat import player_stats



def start_nbl_basketball_svr(opts):
    topic = 'nbl.bk.live'
    asyncio.run(NblBasketballFeedSvr().start(topic))


def start_nbl_basketball_client(opts):
    topic = 'nbl.bk.live'
    asyncio.run(NblBasketballFeedClient().start(topic))

def start_nbl_basketball_match(opts):
    nbl_match.run()

def nbl_player_team_info(opts):
    nbl_spider.run()

def nbl_player_stats(opts):
    player_stats().get_match_id_player_stats()





nbl_basketball_actions = {
    'start_nbl_basketball_svr': start_nbl_basketball_svr,
    'start_nbl_basketball_client': start_nbl_basketball_client,
    'start_nbl_basketball_match' : start_nbl_basketball_match,
    'nbl_player_team_info' : nbl_player_team_info,
    'nbl_player_stats' : nbl_player_stats
}