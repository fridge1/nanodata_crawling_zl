import asyncio

from apps.eur_basketball_spider.eur_client import EurBasketballFeedClient
from apps.eur_basketball_spider.eur_svr import EurBasketballFeedSvr
from apps.eur_basketball_spider import eur_spider,eur_match,eur_player_stat,eur_team_stat
from apps.NBL.nbl_client import NblBasketballFeedClient
from apps.NBL.nbl_svr import NblBasketballFeedSvr


servers = ["nats://hub.nats.namincs.com:4222"]
user = 'nana'
password = 'aa123456'


def start_eur_basketball_svr(opts):
    topic = 'euro.bk.live'
    asyncio.run(EurBasketballFeedSvr().start(topic=topic, servers=servers, user=user, password=password))


def start_eur_basketball_client(opts):
    topic = 'euro.bk.live'
    asyncio.run(EurBasketballFeedClient().start(topic=topic, servers=servers, user=user, password=password))

def eur_player_team_manager_info(opts):
    eur_spider.timing_run()

def eur_match_info(opts):
    eur_match.run()

def eur_player_stat_info(opts):
    eur_player_stat.player_stat_run()

def eur_team_stat_info(opt):
    eur_team_stat.team_stat_run()

def start_nbl_basketball_svr(opts):
    topic = 'nbl.bk.live'
    asyncio.run(NblBasketballFeedSvr().start(topic=topic, servers=servers, user=user, password=password))

def start_nbl_basketball_client(opts):
    topic = 'nbl.bk.live'
    asyncio.run(NblBasketballFeedClient().start(topic=topic, servers=servers, user=user, password=password))

eur_basketball_actions = {
    'start_eur_basketball_svr': start_eur_basketball_svr,
    'start_eur_basketball_client': start_eur_basketball_client,
    'eur_player_team_manager_info': eur_player_team_manager_info,
    'eur_match_info': eur_match_info,
    'eur_player_stat_info' : eur_player_stat_info,
    'eur_team_stat_info'  : eur_team_stat_info,
    'start_nbl_basketball_svr': start_nbl_basketball_svr,
    'start_nbl_basketball_client': start_nbl_basketball_client,
}
