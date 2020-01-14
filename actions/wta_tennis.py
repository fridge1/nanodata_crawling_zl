import asyncio
from apps.tennis_WTA.wta_double_rank import GetRankInfo
from apps.tennis_WTA.wta_single_rank import GetSingleRankInfo
from apps.tennis_WTA.wta_player_info import GetPlayerInfo
from apps.tennis_WTA.wta_competition import GetCompetitionInfo
from apps.tennis_WTA.wta_single_player_stat import GetSinglePlayerStat
from apps.tennis_WTA.wta_match_info import GetMatchInfo
from apps.tennis_WTA.wta_update_data import WtaTennisFeedSvr
from apps.tennis_WTA.wta_player_match_stat import GetMatchPlayerStat


def send_wta_tennis_rank(opt):
    topic = 'wta.tennis.ranking'
    asyncio.run(WtaTennisFeedSvr().start(topic=topic))


def wta_tennis_double_rank(opt):
    GetRankInfo().run()


def wta_tennis_single_rank(opt):
    GetSingleRankInfo().run()


def wta_tennis_player_single_info(opt):
    GetPlayerInfo().get_single_player()

def wta_tennis_player_double_info(opt):
    GetPlayerInfo().get_double_player()


def wta_tennis_competition_info(opt):
    GetCompetitionInfo().run()


def wta_tennis_player_stat_info(opt):
    GetSinglePlayerStat().get_double_player()
    GetSinglePlayerStat().get_single_player()


def wta_tennis_player_match_info(opt):
    GetMatchInfo().run()

def test(opt):
    GetMatchPlayerStat().get_match_info()


wta_tennis_actions = {
    'wta_tennis_double_rank': wta_tennis_double_rank,
    'wta_tennis_single_rank': wta_tennis_single_rank,
    'wta_tennis_player_single_info': wta_tennis_player_single_info,
    'wta_tennis_player_double_info': wta_tennis_player_double_info,
    'wta_tennis_competition_info': wta_tennis_competition_info,
    'wta_tennis_player_stat_info': wta_tennis_player_stat_info,
    'wta_tennis_player_match_info': wta_tennis_player_match_info,
    'send_wta_tennis_rank': send_wta_tennis_rank,
    'test': test,
}
