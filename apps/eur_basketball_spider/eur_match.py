import requests
from apps.eur_basketball_spider.tools import tree_parse, change_bjtime, get_team_id, seasons, stage_id
import re
import json
from orm_connection.orm_session import MysqlSvr
from orm_connection.eur_basketball import *
import time
import traceback
from apps.send_error_msg import dingding_alter
from common.libs.log import LogMgr

logger = LogMgr.get('eur_basketball_match_live')


class GetMatchInfo(object):
    def __init__(self):
        self.get_team_id = get_team_id()

    def match_end(self, sport_id, season_id, typecode, round_num, season, gamecode):
        headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
        spx_dev_session = MysqlSvr.get('spider_zl')
        match_id = seasons[str(season_id) + '-' + str(season_id + 1)]
        while True:
            time.sleep(10)
            match = {}
            box_url = 'https://www.euroleague.net/main/results/showgame?gamecode=%s&seasoncode=E%s' % (
            gamecode, season_id)
            box_url_res = requests.get(box_url, headers=headers)
            if box_url_res.status_code == 200:
                box_url_tree = tree_parse(box_url_res)
                date = box_url_tree.xpath('//div[@class="date cet"]/text()')[0]
                match_time = change_bjtime(date)
                box_api_url = 'https://live.euroleague.net/api/Boxscore?gamecode=%s&seasoncode=E%s&disp=' % (
                    gamecode, season_id)
                home_team_url = \
                    box_url_tree.xpath('//div[@class="team local "]/a/@href|//div[@class="team local winner"]/a/@href')[
                        0]
                away_team_url = \
                    box_url_tree.xpath('//div[@class="team road "]/a/@href|//div[@class="team road winner"]/a/@href')[0]
                home_team_key = re.findall(r'clubcode=(.*?)&', home_team_url)[0]
                away_team_key = re.findall(r'clubcode=(.*?)&', away_team_url)[0]
                home_team_id = self.get_team_id[home_team_key.lower()]
                away_team_id = self.get_team_id[away_team_key.lower()]
                if 'RS' or 'TS' in typecode:
                    stage_name_zh = '欧篮联%s-%s赛季常规赛' % (str(season_id), str(season_id + 1))
                else:
                    stage_name_zh = '欧篮联%s-%s赛季季后赛' % (str(season_id), str(season_id + 1))
                box_api_res = requests.get(box_api_url, headers=headers)
                if box_api_res.text == '':
                    logger.info(box_api_url)
                    logger.info('比赛未开始...')
                    status_id = 1
                    match['sport_id'] = sport_id
                    match['season_id'] = season_id
                    match['home_team_id'] = home_team_id
                    match['away_team_id'] = away_team_id
                    match['match_time'] = match_time
                    match['home_score'] = 0
                    match['away_score'] = 0
                    match['round_num'] = round_num
                    match['home_half_score'] = 0
                    match['away_half_score'] = 0
                    match['home_scores'] = 0
                    match['away_scores'] = 0
                    match['stage_id'] = stage_id[stage_name_zh]
                    match['status_id'] = status_id
                    match['season_id'] = seasons[season]
                    match['id'] = int(str(match_id) + '0000') + int(gamecode)
                    BleaguejpBasketballMatch.upsert(
                        spx_dev_session,
                        'id',
                        match
                    )
                    logger.info(match)
                    break
                else:
                    box_api_dict = json.loads(box_api_res.text)
                    key_list = list(box_api_dict['ByQuarter'][0].keys())[1:]
                    home_scores = []
                    away_scores = []
                    for key in key_list:
                        home_scores.append(box_api_dict['ByQuarter'][0][key])
                        away_scores.append(box_api_dict['ByQuarter'][1][key])
                    home_half_score = box_api_dict['EndOfQuarter'][0]['Quarter2']
                    away_half_score = box_api_dict['EndOfQuarter'][1]['Quarter2']
                    home_score = box_api_dict['Stats'][0]['totr']['Points']
                    away_score = box_api_dict['Stats'][1]['totr']['Points']
                    if box_api_dict['Live'] == False:
                        status_id = 10
                        if int(home_score) != sum(home_scores):
                            ot_score = int(home_score) - sum(home_scores)
                            home_scores.append(ot_score)
                        if int(away_score) != sum(away_scores):
                            ot_score = int(away_score) - sum(away_scores)
                            away_scores.append(ot_score)
                        match['sport_id'] = sport_id
                        match['season_id'] = season_id
                        match['home_team_id'] = home_team_id
                        match['away_team_id'] = away_team_id
                        match['match_time'] = match_time
                        match['home_score'] = home_score
                        match['away_score'] = away_score
                        match['round_num'] = round_num
                        match['home_half_score'] = int(home_half_score)
                        match['away_half_score'] = int(away_half_score)
                        match['home_scores'] = str(home_scores).replace(']', '') + ', ' + str(home_score) + ']'
                        match['away_scores'] = str(away_scores).replace(']', '') + ', ' + str(away_score) + ']'
                        match['stage_id'] = stage_id[stage_name_zh]
                        match['status_id'] = status_id
                        match['season_id'] = seasons[season]
                        match['id'] = int(str(match_id) + '0000') + int(gamecode)
                        BleaguejpBasketballMatch.upsert(
                            spx_dev_session,
                            'id',
                            match
                        )
                        logger.info(match)
                        break
                    else:
                        status_id = 1
                        match['sport_id'] = sport_id
                        match['season_id'] = season_id
                        match['home_team_id'] = home_team_id
                        match['away_team_id'] = away_team_id
                        match['match_time'] = match_time
                        match['home_score'] = 0
                        match['away_score'] = 0
                        match['round_num'] = round_num
                        match['home_half_score'] = 0
                        match['away_half_score'] = 0
                        match['home_scores'] = 0
                        match['away_scores'] = 0
                        match['stage_id'] = stage_id[stage_name_zh]
                        match['status_id'] = status_id
                        match['season_id'] = seasons[season]
                        match['id'] = int(str(match_id) + '0000') + int(gamecode)
                        BleaguejpBasketballMatch.upsert(
                            spx_dev_session,
                            'id',
                            match
                        )
                        logger.info(match)
                        break
        spx_dev_session.close()

    def match_run(self):
        try:
            headers = {
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            }
            start_url = 'https://www.euroleague.net/'
            url = 'https://www.euroleague.net/main/results?seasoncode=E%s'
            seasons_id = [2019]
            sport_id = 2
            for season_id in seasons_id:
                season = '%s-%s' % (str(season_id), str(season_id + 1))
                res = requests.get(url % str(season_id), headers=headers)
                res_tree = tree_parse(res)
                typecode_urls = res_tree.xpath('//div[@class="game-center-selector"]/div[2]/select/option/@value')
                for typecode_url in typecode_urls:
                    typecode = re.findall(r'phasetypecode=(.*?)&', typecode_url)[0]
                    typecode_res = requests.get(start_url + typecode_url, headers=headers)
                    typecode_res_tree = tree_parse(typecode_res)
                    round_urls = typecode_res_tree.xpath(
                        '//div[@class="game-center-selector"]/div[3]/select/option/@value')
                    for round_url in round_urls:
                        round_num = re.findall(r'gamenumber=(.*?)&', round_url)[0]
                        round_res = requests.get(start_url + round_url, headers=headers)
                        round_res_tree = tree_parse(round_res)
                        gamecode_urls = round_res_tree.xpath(
                            '//div[@class="game played"]/a/@href|//div[@class="game "]/a/@href')
                        for gamecode in gamecode_urls:
                            code = re.findall(r'gamecode=(.*?)&', gamecode)[0]
                            self.match_end(sport_id, season_id, typecode, round_num, season, code)
        except:
            dingding_alter(traceback.format_exc())
            logger.error(traceback.format_exc())

    def run(self):
        while True:
            try:
                self.match_run()
                time.sleep(300)
            except:
                dingding_alter(traceback.format_exc())
                logger.error(traceback.format_exc())
                continue
