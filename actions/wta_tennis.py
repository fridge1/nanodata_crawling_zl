import asyncio
from apps.tennis_WTA.wta_double_rank import GetRankInfo
from apps.tennis_WTA.wta_single_rank import GetSingleRankInfo
from apps.tennis_WTA.wta_player_info import GetPlayerInfo
from apps.tennis_WTA.wta_competition import GetCompetitionInfo
from apps.tennis_WTA.wta_single_player_stat import GetSinglePlayerStat


def wta_tennis_double_rank(opt):
    GetRankInfo().run()


def wta_tennis_single_rank(opt):
    GetSingleRankInfo().run()

def wta_tennis_player_info(opt):
    GetPlayerInfo().get_player_info()

def wta_tennis_competition_info(opt):
    GetCompetitionInfo().run()

def wta_tennis_player_career_info(opt):
    GetPlayerInfo().get_player_career()

def wta_tennis_player_stat_info(opt):
    GetSinglePlayerStat().run()




wta_tennis_actions = {
    'wta_tennis_double_rank': wta_tennis_double_rank,
    'wta_tennis_single_rank': wta_tennis_single_rank,
    'wta_tennis_player_info': wta_tennis_player_info,
    'wta_tennis_competition_info': wta_tennis_competition_info,
    'wta_tennis_player_career_info': wta_tennis_player_career_info,
    'wta_tennis_player_stat_info': wta_tennis_player_stat_info,
}
