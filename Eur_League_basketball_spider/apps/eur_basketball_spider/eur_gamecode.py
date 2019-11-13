import requests
from apps.eur_basketball_spider.tools import tree_parse,change_bjtime,get_team_id
import re
import json
from apps.eur_basketball_spider.eur_playbyplay import EurLeagueSpider_playbyplay





def get_match():
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
    start_url = 'https://www.euroleague.net/'
    url = 'https://www.euroleague.net/main/results?seasoncode=E%s'
    seasons_id = [2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
    sport_id = 2
    has_table = 1
    for season_id in seasons_id:
        res = requests.get(url % str(season_id),headers=headers)
        res_tree = tree_parse(res)
        typecode_urls = res_tree.xpath('//div[@class="game-center-selector"]/div[2]/select/option/@value')
        for typecode_url in typecode_urls:
            typecode = re.findall(r'phasetypecode=(.*?)&',typecode_url)[0]
            if 'RS' or 'TS' in typecode:
                mode = 5
                name_zh = '欧篮联%s-%s赛季常规赛' % (str(season_id),str(season_id-1))
                typecode_res = requests.get(start_url + typecode_url,headers=headers)
                typecode_res_tree = tree_parse(typecode_res)
                round_urls = typecode_res_tree.xpath('//div[@class="game-center-selector"]/div[3]/select/option/@value')
                for round_url in round_urls:
                    round_num = re.findall(r'gamenumber=(.*?)&', round_url)[0]
                    round_res = requests.get(start_url+round_url,headers=headers)
                    round_res_tree = tree_parse(round_res)
                    gamecode_urls = round_res_tree.xpath('//div[@class="game played"]/a/@href')
                    for gamecode_url in gamecode_urls:
                        match = {}
                        gamecode = re.findall(r'gamecode=(.*?)&',gamecode_url)[0]
                        box_url = 'https://www.euroleague.net/main/results/showgame?gamecode=%s&seasoncode=E%s' % (gamecode, season_id)
                        box_url_res = requests.get(box_url, headers=headers)
                        box_url_tree = tree_parse(box_url_res)
                        date = box_url_tree.xpath('//div[@class="date cet"]/text()')[0]
                        match_time = change_bjtime(date)
                        box_api_url = 'https://live.euroleague.net/api/Boxscore?gamecode=%s&seasoncode=E%s&disp=' % (gamecode, season_id)
                        box_api_res = requests.get(box_api_url, headers=headers)
                        box_api_dict = json.loads(box_api_res.text)
                        home_team_key = box_api_dict['ByQuarter'][0]['Team']
                        away_team_key = box_api_dict['ByQuarter'][1]['Team']
                        home_team_id = get_team_id(home_team_key)
                        away_team_id = get_team_id(away_team_key)
                        key_list = list(box_api_dict['ByQuarter'][0].keys())[1:]
                        home_scores = []
                        away_scores = []
                        for key in key_list:
                            home_scores.append(box_api_dict['ByQuarter'][0][key])
                            away_scores.append(box_api_dict['ByQuarter'][1][key])
                        home_half_score = box_api_dict['EndOfQuarter'][0]['Quarter2']
                        away_half_score = box_api_dict['EndOfQuarter'][1]['Quarter2']
                        home_score = box_api_dict['EndOfQuarter'][0][key_list[-1]]
                        away_score = box_api_dict['EndOfQuarter'][0][key_list[-1]]
                        if box_api_dict['Live'] == False:
                            status_id = 1
                        else:
                            status_id = 0
                        match['sport_id'] = sport_id
                        match['season_id'] = season_id
                        match['home_team_id'] = home_team_id
                        match['away_team_id'] = away_team_id
                        match['match_time'] = match_time
                        match['home_score'] = home_score
                        match['away_score'] = away_score
                        match['round_num'] = round_num
                        match['home_half_score'] = str(home_half_score)
                        match['away_half_score'] = str(away_half_score)
                        match['stage_id'] = ''
                        match['status_id'] = status_id
            if 'PO' or 'FF' in typecode:
                stage = {}
                mode = 6
                name_zh = '欧篮联%s-%s赛季季后赛' % (str(season_id), str(season_id + 1))
                typecode_res = requests.get(start_url + typecode_url, headers=headers)
                typecode_res_tree = tree_parse(typecode_res)
                round_urls = typecode_res_tree.xpath('//div[@class="game-center-selector"]/div[3]/select/option/@value')
                for round_url in round_urls:
                    round_num = re.findall(r'gamenumber=(.*?)&', round_url)[0]
                    round_res = requests.get(start_url + round_url, headers=headers)
                    round_res_tree = tree_parse(round_res)
                    gamecode_urls = round_res_tree.xpath('//div[@class="game played"]/a/@href')
                    for gamecode_url in gamecode_urls:
                        match = {}
                        gamecode = re.findall(r'gamecode=(.*?)&', gamecode_url)[0]
                        box_url = 'https://www.euroleague.net/main/results/showgame?gamecode=%s&seasoncode=E%s' % (
                        gamecode, season_id)
                        box_url_res = requests.get(box_url, headers=headers)
                        box_url_tree = tree_parse(box_url_res)
                        date = box_url_tree.xpath('//div[@class="date cet"]/text()')[0]
                        match_time = change_bjtime(date)
                        box_api_url = 'https://live.euroleague.net/api/Boxscore?gamecode=%s&seasoncode=E%s&disp=' % (gamecode,season_id)
                        box_api_res = requests.get(box_api_url,headers=headers)
                        box_api_dict = json.loads(box_api_res.text)
                        home_team_key = box_api_dict['ByQuarter'][0]['Team']
                        away_team_key = box_api_dict['ByQuarter'][1]['Team']
                        home_team_id = get_team_id(home_team_key)
                        away_team_id = get_team_id(away_team_key)
                        key_list = list(box_api_dict['ByQuarter'][0].keys())[1:]
                        home_scores = []
                        away_scores = []
                        for key in key_list:
                            home_scores.append(box_api_dict['ByQuarter'][0][key])
                            away_scores.append(box_api_dict['ByQuarter'][1][key])
                        home_half_score = box_api_dict['EndOfQuarter'][0]['Quarter2']
                        away_half_score = box_api_dict['EndOfQuarter'][1]['Quarter2']
                        home_score = box_api_dict['EndOfQuarter'][0][key_list[-1]]
                        away_score = box_api_dict['EndOfQuarter'][0][key_list[-1]]
                        if box_api_dict['Live'] == False:
                            status_id = 1
                        else:
                            status_id = 0
                        match['sport_id'] = sport_id
                        match['season_id'] = season_id
                        match['home_team_id'] = home_team_id
                        match['away_team_id'] = away_team_id
                        match['match_time'] = match_time
                        match['home_score'] = home_score
                        match['away_score'] = away_score
                        match['round_num'] = round_num
                        match['home_half_score'] = str(home_half_score)
                        match['away_half_score'] = str(away_half_score)
                        match['stage_id'] = ''
                        match['status_id'] = status_id




