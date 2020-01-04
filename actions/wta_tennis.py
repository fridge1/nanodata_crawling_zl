import asyncio
from apps.tennis_WTA.wta_double_rank import GetRankInfo
from apps.tennis_WTA.wta_single_rank import GetSingleRankInfo
# from apps.tennis_WTA.wta_player_info import GetPlayerInfo


def wta_tennis_double_rank(opt):
    GetRankInfo().run()


def wta_tennis_single_rank(opt):
    GetSingleRankInfo().run()


def wta_tennis_player_city(opt):
    GetPlayerInfo().get_city()


def wta_tennis_player_info(opt):
    GetPlayerInfo().get_player_info()


wta_tennis_actions = {
    'wta_tennis_double_rank': wta_tennis_double_rank,
    'wta_tennis_single_rank': wta_tennis_single_rank,
    'wta_tennis_player_city': wta_tennis_player_city,
    'wta_tennis_player_info': wta_tennis_player_info,
}
