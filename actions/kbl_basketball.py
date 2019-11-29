import asyncio
# from apps.NBL.nbl_client import NblBasketballFeedClient
# from apps.NBL.nbl_svr import NblBasketballFeedSvr
from apps.kbl.kbl_match import match_info
# from apps.NBL import nbl_spider
# from apps.NBL.nbl_player_stat import player_stats




def start_kbl_basketball_match(opts):
    url = 'https://www.kbl.or.kr/main/main.asp?game_date=20191005'
    match_info().get_date_url(url)




kbl_basketball_actions = {
    'start_kbl_basketball_match' : start_kbl_basketball_match
}