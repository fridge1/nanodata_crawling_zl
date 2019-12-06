# -*- coding: utf-8 -*-
import requests
from apps.kbl.tools import tree_parse
import re
import asyncio
import json
import time



async def get_match_info_async():
    headers = {
        'user_agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    url = 'https://sports.news.naver.com/basketball/schedule/index.nhn?date=20191206&month=11&year=2008&teamCode=&category=kbl'
    res = requests.get(url,headers=headers)
    res_tree = tree_parse(res)
    match_urls = res_tree.xpath('//span[@class="td_btn"]/a[1]/@href')
    print(len(match_urls))
    for match_url in match_urls:
        game_id = re.findall(r'gameId=(.*)',match_url)[0]
        print(game_id)
        # await asyncio.sleep(3)
        url_api = 'https://sports.news.naver.com/ajax/game/relayData.nhn?gameId=%s' % game_id
        url_api_res = requests.get(url_api,headers=headers).json()
        for key in url_api_res:
            print(key)


# if __name__ == '__main__':
    asyncio.run(get_match_info_async())

