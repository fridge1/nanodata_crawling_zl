# -*- coding: utf-8 -*-
import requests
from apps.kbl.tools import tree_parse,season_id_dict,change_match_bjtime
import re
import asyncio
import json
import time
import threading
from orm_connection.kbl_basketball import BleagueNblBasketballMatch
from orm_connection.orm_session import MysqlSvr



class GetMatchObj():
    def __init__(self):
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.url = 'https://sports.news.naver.com/basketball/schedule/index.nhn?date=20191206&month=11&year=2008&teamCode=&category=kbl'
        self.spx_dev_session = MysqlSvr.get('spider_zl')


    async def get_match_info(self,game_id):
        url_api = 'https://sports.news.naver.com/ajax/game/relayData.nhn?gameId=%s' % game_id
        url_api_res = requests.get(url_api, headers=self.headers).json()
        key1 = game_id
        date = game_id[:8]
        if int(date[4:6]) >= 5:
            season = str(date[:4]) + '-' + str(int(date[:4])+1)
        else:
            season = str(int(date[:4])-1) + '-' + str(int(date[:4]))
        date_time = date+' '+url_api_res['kick_off'].replace(' ','')
        print(date_time)
        match_time = change_match_bjtime(date_time)
        print(match_time)
        season_id = season_id_dict[season]
        stage_id = season_id
        sport_id = 2
        if url_api_res['line_up']['status'] == 0:
            home_team_id = url_api_res['home_team']
            away_team_id = url_api_res['away_team']
            status = 1
            home_score = 0
            away_score = 0
            home_half_score = 0
            away_half_score = 0
            home_scores = 0
            away_scores = 0
        else:
            home_team_id = url_api_res['home_team']
            away_team_id = url_api_res['away_team']
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
                away_scores.append(url_api_res['quarter_score'][away_team_id][key])
            home_scores = str(list(map(int, home_scores)))
            away_scores = str(list(map(int, away_scores)))
        data = {
            'key':key1,
            'sport_id':int(sport_id),
            'home_team_id':int(home_team_id),
            'away_team_id':int(away_team_id),
            'status_id':int(status),
            'home_score':int(home_score),
            'away_score':int(away_score),
            'home_half_score':int(home_half_score),
            'away_half_score':int(away_half_score),
            'home_scores':home_scores,
            'away_scores':away_scores,
            'season_id':int(season_id),
            'stage_id':int(stage_id),
            'match_time':int(match_time),
        }
        BleagueNblBasketballMatch.upsert(
            self.spx_dev_session,
            'key',
            data
        )
        print(data)





    async def get_match_info_async(self,url):
        res = requests.get(url,headers=self.headers)
        res_tree = tree_parse(res)
        match_urls = res_tree.xpath('//span[@class="td_btn"]/a[1]/@href')
        if match_urls:
            for match_url in match_urls:
                game_id = re.findall(r'gameId=(.*)',match_url)[0]
                await self.get_match_info(game_id)
        else:
            return '赛程暂未安排。。。'
        next_url_date = res_tree.xpath('//button[@class="btn_move_date next"]/@onclick')
        year = re.findall(r'\d+',next_url_date[0])[0]
        month = re.findall(r'\d+',next_url_date[0])[1]
        date = time.strftime('%Y%m%d', time.localtime(time.time()))
        next_url = 'https://sports.news.naver.com/basketball/schedule/index.nhn?date=%s&month=%s&year=%s&teamCode=&category=kbl' % (date,month,year)
        print(next_url)
        await self.get_match_info_async(next_url)



    async def run(self):
        while True:
            url = 'https://sports.news.naver.com/basketball/schedule/index.nhn?date=20191206&month=11&year=2008&teamCode=&category=kbl'
            await self.get_match_info_async(url)
            time.sleep(7200)


