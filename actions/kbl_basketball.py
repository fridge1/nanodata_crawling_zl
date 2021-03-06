import asyncio
from apps.kbl.kbl_client import KblBasketballFeedClient
from apps.kbl.kbl_svr import KblBasketballFeedSvr
from apps.kbl.kbl_match import GetMatchObj
from apps.kbl.kbl_play_team_stat import PlayerTeamStats
from apps.kbl.kbl_score_svr import KblBasketballScore

# from apps.kbl.kbl_score_client import BeitaiCbaScroeFeedSvr


servers = ["nats://hub.nats.namincs.com:4222"]
user = 'nana'
password = 'aa123456'


def start_kbl_basketball_svr(opts):
    topic = 'kbl.bk.live'
    asyncio.run(KblBasketballFeedSvr().start(topic=topic))


def start_kbl_basketball_client(opts):
    topic = 'kbl.bk.live'
    asyncio.run(KblBasketballFeedClient().start(topic=topic))


def start_kbl_basketball_score_svr(opts):
    topic = 'bk.score.live'
    asyncio.run(KblBasketballScore().start(topic=topic))


def start_kbl_basketball_match(opts):
    asyncio.run(GetMatchObj().run())


def kbl_basketball_player_team_stat(opts):
    PTS = PlayerTeamStats()
    asyncio.run(PTS.run())


kbl_basketball_actions = {
    'start_kbl_basketball_match': start_kbl_basketball_match,
    'start_kbl_basketball_svr': start_kbl_basketball_svr,
    'start_kbl_basketball_client': start_kbl_basketball_client,
    'kbl_basketball_player_team_stat': kbl_basketball_player_team_stat,
    'start_kbl_basketball_score_svr': start_kbl_basketball_score_svr,
}
