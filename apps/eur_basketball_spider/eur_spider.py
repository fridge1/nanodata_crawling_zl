import requests
from apps.eur_basketball_spider.tools import tree_parse,time_stamp,manager_name,translate_dict,team_name,get_manager_id_upsert,get_team_id
import re
from orm_connection.orm_session import MysqlSvr
from orm_connection.eur_basketball import *
import schedule
import time
from common.libs.log import LogMgr
logger = LogMgr.get('eur_basketball_player_coach_team')




def get_coach_info(season_id):
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
    start_url = 'https://www.euroleague.net'
    team_map_url = 'https://www.euroleague.net/competition/teams?seasoncode=E%s' % season_id
    teams_res = requests.get(team_map_url,headers=headers)
    teams_tree = tree_parse(teams_res)
    team_list = teams_tree.xpath('//div[@class="RoasterName"]/a/@href')
    for team_url in team_list:
        team_url_res = requests.get(start_url + team_url,headers=headers)
        team_url_tree = tree_parse(team_url_res)
        coach_url = team_url_tree.xpath('//div[contains(@class,"item")]/div[@class="img"]/a/@href')[-1]
        if 'showcoach' in coach_url:
            coach_res = requests.get(start_url + coach_url, headers=headers)
            coach_tree = tree_parse(coach_res)
            coach = {}
            coach['sport_id'] = 2
            coach['key'] = re.findall(r'pcode=(.*?)&', coach_url)[0]
            coach['name_en'] = coach_tree.xpath('//div[@class="name"]/text()')[0]
            try:
                coach['name_zh'] = manager_name[coach['name_en']]
            except:
                coach['name_zh'] = ''
            try:
                coach_img = coach_tree.xpath('//div[@class="coach-img"]/img/@src')[0]
                coach['logo'] = coach_img
            except:
                coach['logo'] = ''
                print('没有该教练的图片...')
            time_birthday = coach_tree.xpath('//div[@class="summary-second"]/span[1]/text()')[0]
            coach['birthday'], coach['age'] = time_stamp(time_birthday)
            try:
                coach['nationality'] = coach_tree.xpath('//div[@class="summary-second"]/span[2]/text()')[0].split(':')[
                    -1]
            except:
                coach['nationality'] = ''
                print('没有教练的国籍信息...')
            print('coach:', coach)
            data = {
                'key': coach['key'],
                'name_en': coach['name_en'],
                'sport_id': coach['sport_id'],
                'birthday': coach['birthday'],
                'age': coach['age'],
                'nationality': coach['nationality'],
                'name_zh' : coach['name_zh'],
                'logo' : coach['logo'],
            }
            spx_dev_session = MysqlSvr.get('spider_zl')
            BleaguejpBasketballManager.upsert(
                spx_dev_session,
                'key',
                data
            )
            logger.info(data)



def get_team_info(season_id):
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
    start_url = 'https://www.euroleague.net'
    team_map_url = 'https://www.euroleague.net/competition/teams?seasoncode=E%s' % season_id
    print(team_map_url)
    teams_res = requests.get(team_map_url,headers=headers)
    teams_tree = tree_parse(teams_res)
    team_list = teams_tree.xpath('//div[@class="teams"]/div[@class="item"]')
    for team_info in team_list:
        team={}
        team['logo'] = team_info.xpath('./div[@class="RoasterImage"]/a/img/@src')[0]
        team['name_en'] = team_info.xpath('./div[@class="RoasterName"]/a/text()')[0]
        team_url = team_info.xpath('./div[@class="RoasterName"]/a/@href')[0]
        team_url_res = requests.get(start_url+team_url,headers=headers)
        team_url_tree = tree_parse(team_url_res)
        coach_url = team_url_tree.xpath('//div[contains(@class,"item")]/div[@class="img"]/a/@href')[-1]
        if 'showcoach' in coach_url:
            coach_key = re.findall(r'pcode=(.*?)&', coach_url)[0]
        else:
            coach_key=''
        team['sport_id'] = 2
        team['manager_id'] = get_manager_id_upsert(coach_key)
        try:
            team['name_zh'] = team_name[team['name_en']]
        except:
            team['name_zh'] = ''
        team['gender'] = 0
        print('team:',team)
        spx_dev_session = MysqlSvr.get('spider_zl')
        BleaguejpBasketballTeam.upsert(
            spx_dev_session,
            'key',
            team
        )
        logger.info(team)


def get_player_info(season_id):
    headers = {
        'user_agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }

    start_url = 'https://www.euroleague.net'
    team_map_url = 'https://www.euroleague.net/competition/teams?seasoncode=E%s' % season_id
    teams_res = requests.get(team_map_url, headers=headers)
    teams_tree = tree_parse(teams_res)
    team_list = teams_tree.xpath('//div[@class="teams"]/div[@class="item"]')
    for team_info in team_list:
        team_url = team_info.xpath('./div[@class="RoasterName"]/a/@href')[0]
        team_key = re.findall(r'clubcode=(.*?)&', team_url)[0]
        player_list_res = requests.get(start_url+team_url,headers=headers)
        player_list_tree = tree_parse(player_list_res)
        player_urls = player_list_tree.xpath('//div[@class="wp-module"]/div[@class="item player"]/div[@class="img"]/a/@href')
        for player_url in player_urls:
            player={}
            print(start_url+player_url)
            player_res = requests.get(start_url+player_url,headers=headers)
            player_tree = tree_parse(player_res)
            player['sport_id'] = 2
            try:
                player['name_en'] = player_tree.xpath('//div[@class="name"]/text()')[0]
            except:
                player['name_en'] = ''
            player['key'] = re.findall(r'pcode=(.*?)&',player_url)[0]
            print(player['key'])
            try:
                player['logo'] = player_tree.xpath('//div[@class="player-img"]/img/@src')[0]
            except:
                player['logo'] = ''
                print('没有该球员的图片...')
            try:
                player['shirt_number'] = player_tree.xpath('//span[@class="dorsal"]/text()')[0]
            except:
                player['shirt_number'] = 0
            try:
                position = player_tree.xpath('//div[@class="summary-first"]/span[last()]/span[last()]/text()')[0]
                player['position'] = position.encode('utf-8').decode('utf-8')[0]
            except:
                player['position'] = ''
            if 'Height' in player_tree.xpath('//div[@class="summary-second"]/span[1]/text()')[0].split(':')[0]:
                player['height'] = float(player_tree.xpath('//div[@class="summary-second"]/span[1]/text()')[0].split(':')[-1])*100
                time_birthday = player_tree.xpath('//div[@class="summary-second"]/span[2]/text()')[0]
                player['birthday'],player['age'] = time_stamp(time_birthday)
                player['nationality'] = player_tree.xpath('//div[@class="summary-second"]/span[last()]/text()')[0].split(':')[-1]
            else:
                player['height'] = 0
                time_birthday = player_tree.xpath('//div[@class="summary-second"]/span[1]/text()')[0]
                player['birthday'], player['age'] = time_stamp(time_birthday)
                player['nationality'] = \
                player_tree.xpath('//div[@class="summary-second"]/span[last()]/text()')[0].split(':')[-1]
            try:
                player['team_id'] = get_team_id(team_key)
            except:
                player['team_id'] = 0
            try:
                player['name_zh'] = translate_dict[player['name_en']]
            except:
                player['name_zh'] = ''
            print('player:',player)
            data = {
                'key': player['key'],
                'name_en': player['name_en'],
                'name_zh' : player['name_zh'],
                'sport_id': player['sport_id'],
                'age': player['age'],
                'birthday': player['birthday'],
                'nationality': player['nationality'],
                'height': player['height'],
                'shirt_number': player['shirt_number'],
                'position': player['position'],
                'team_id' : player['team_id'],
                'logo' : player['logo'],
            }
            spx_dev_session = MysqlSvr.get('spider_zl')
            BleaguejpBasketballPlayer.upsert(
                spx_dev_session,
                'key',
                data
            )
            logger.info(data)


def run():
    season_ids = [2019]
    for season_id in season_ids:
        try:
            get_player_info(season_id)
            get_coach_info(season_id)
        except Exception as e:
            logger.error(e)
            continue


def timing_run():
    schedule.every().hour.do(run)
    while True:
        schedule.run_pending()
        time.sleep(600)
