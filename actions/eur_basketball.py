import asyncio
from apps.eur_basketball_spider.eur_client import EurBasketballFeedClient
from apps.eur_basketball_spider.eur_svr import EurBasketballFeedSvr
from apps.eur_basketball_spider import eur_team_stat
from apps.eur_basketball_spider.eur_match import GetMatchInfo
from apps.eur_basketball_spider.eur_spider import GetPlayerTeamCoachInfo
from apps.eur_basketball_spider.eur_player_stat import GetPlayerStat
from apps.eur_basketball_spider.eur_score_svr import EurBasketballScore
from apps.eur_basketball_spider.eur_table import GetTable

servers = ["nats://hub.nats.namincs.com:4222"]
user = 'nana'
password = 'aa123456'


def start_eur_basketball_svr(opts):
    topic = 'euro.bk.live'
    asyncio.run(EurBasketballFeedSvr().start(topic=topic, servers=servers, user=user, password=password))


def start_eur_basketball_client(opts):
    topic = 'euro.bk.live'
    asyncio.run(EurBasketballFeedClient().start(topic=topic, servers=servers, user=user, password=password))

def start_eur_basketball_score_svr(opts):
    topic = 'bk.score.live'
    asyncio.run(EurBasketballScore().start(topic=topic))


def eur_player_team_manager_info(opts):
    GetPlayerTeamCoachInfo().run()


def eur_match_info(opts):
    GetMatchInfo().run()


def eur_player_stat_info(opts):
    GetPlayerStat().player_stat_run()


def eur_team_stat_info(opt):
    eur_team_stat.team_stat_run()

def eur_table_info_url(opt):
    GetTable().match_url()





eur_basketball_actions = {
    'start_eur_basketball_svr': start_eur_basketball_svr,
    'start_eur_basketball_client': start_eur_basketball_client,
    'eur_player_team_manager_info': eur_player_team_manager_info,
    'eur_match_info': eur_match_info,
    'eur_player_stat_info': eur_player_stat_info,
    'eur_team_stat_info': eur_team_stat_info,
    'start_eur_basketball_score_svr': start_eur_basketball_score_svr,
    'eur_table_info_url': eur_table_info_url,
}
