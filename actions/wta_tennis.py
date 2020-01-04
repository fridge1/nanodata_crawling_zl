import asyncio
from apps.tennis_WTA.wta_double_rank import GetRankInfo
from apps.tennis_WTA.wta_single_rank import GetSingleRankInfo
# from apps.tennis_WTA.wta_player_info import GetPlayerInfo


def wta_tennis_double_rank(opt):
    GetRankInfo().run()


def wta_tennis_single_rank(opt):
    GetSingleRankInfo().run()






wta_tennis_actions = {
    'wta_tennis_double_rank': wta_tennis_double_rank,
    'wta_tennis_single_rank': wta_tennis_single_rank,
}
