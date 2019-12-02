import asyncio
# from apps.NBL.nbl_client import NblBasketballFeedClient
# from apps.NBL.nbl_svr import NblBasketballFeedSvr
from apps.kbl.kbl_match import match_info
# from apps.NBL import nbl_spider
# from apps.NBL.nbl_player_stat import player_stats




def start_kbl_basketball_match(opts):
    match_info().run()




kbl_basketball_actions = {
    'start_kbl_basketball_match' : start_kbl_basketball_match
}