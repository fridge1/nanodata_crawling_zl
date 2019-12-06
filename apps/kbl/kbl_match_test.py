# -*- coding: utf-8 -*-
import requests
from apps.kbl.tools import tree_parse
import re
import asyncio
import json
import time
import threading
from orm_connection.kbl_basketball import BleagueNblBasketballMatch
from orm_connection.orm_session import MysqlSvr



class get_match_obj():
    def __init__(self):
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.url = 'https://sports.news.naver.com/basketball/schedule/index.nhn?date=20191206&month=11&year=2008&teamCode=&category=kbl'
        self.spx_dev_session = MysqlSvr.get('spider_zl')


    async def get_match_info(self,game_id):
        url_api = 'https://sports.news.naver.com/ajax/game/relayData.nhn?gameId=%s' % game_id
        url_api_res = requests.get(url_api, headers=self.headers).json()
        if url_api_res['line_up']['status'] == 0:
            pass
        else:
            home_team_id = url_api_res['home_team']
            away_team_id = url_api_res['away_team']
            id = game_id[8:]
            sport_id = 2
            status = 10
            home_score = url_api_res['quarter_score'][home_team_id]['total_score']
            away_score = url_api_res['quarter_score'][away_team_id]['total_score']
            home_half_score = int(url_api_res['quarter_score'][home_team_id]['Q1']) + int(url_api_res['quarter_score'][home_team_id]['Q2'])
            away_half_score = int(url_api_res['quarter_score'][away_team_id]['Q1']) + int(url_api_res['quarter_score'][away_team_id]['Q2'])
            home_scores = []
            for key in url_api_res['quarter_score'][home_team_id]:
                home_scores.append(url_api_res['quarter_score'][home_team_id][key])
            away_scores = []
            for key in url_api_res['quarter_score'][away_team_id]:
                away_scores.append(url_api_res['quarter_score'][home_team_id][key])
            data = {
                'id':int(id),
                'sport_id':int(sport_id),
                'home_team_id':int(home_team_id),
                'away_team_id':int(away_team_id),
                'status_id':int(status),
                'home_score':int(home_score),
                'away_score':int(away_score),
                'home_half_score':int(home_half_score),
                'away_half_score':int(away_half_score),
                'home_scores':str(home_scores),
                'away_scores':str(away_scores),
            }
            BleagueNblBasketballMatch.upsert(
                self.spx_dev_session,
                'id',
                data
            )





    async def get_match_info_async(self):
        res = requests.get(self.url,headers=self.headers)
        res_tree = tree_parse(res)
        match_urls = res_tree.xpath('//span[@class="td_btn"]/a[1]/@href')
        print(len(match_urls))
        for match_url in match_urls:
            game_id = re.findall(r'gameId=(.*)',match_url)[0]
            await get_match_obj().get_match_info(game_id)




if __name__ == '__main__':
    asyncio.run(get_match_obj().get_match_info_async())

