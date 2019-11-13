import requests
from apps.eur_basketball_spider.tools import tree_parse, time_stamp, team_id ,manager_id
import re
from orm_connection.orm_session import MysqlSvr
from orm_connection.eur_basketball import *
import time
import schedule



def info_spider():
    try:
        headers = {
            'user_agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }

        start_url = 'https://www.euroleague.net'
        start_res = requests.get(start_url,headers=headers)
        start_tree = tree_parse(start_res)
        node_title = start_tree.xpath('//*[@id="navigation-main"]/ul/li/a/@href')
        i = 1
        for node in node_title:
            if node.split('/')[-1] == 'teams':
                teams_res = requests.get(start_url+node,headers=headers)
                teams_tree = tree_parse(teams_res)
                season_urls = teams_tree.xpath('//*[@id="main-two"]/div/div/div[1]/div/div[2]/select/option/@value')
                season_res = requests.get(start_url+season_urls[0],headers=headers)
                season_tree = tree_parse(season_res)
                team_list = season_tree.xpath('//*[@id="main-two"]/div/div/div[1]/div/div[2]/select/option/@value')
                for team_url in team_list:
                    team_player_res = requests.get(start_url+team_url,headers=headers)
                    player_list_tree = tree_parse(team_player_res)
                    team_infos = player_list_tree.xpath('//div[@class="teams"]/div[@class="item"]')
                    for team_info in team_infos:
                        team_url = team_info.xpath('./div[@class="RoasterImage"]/a/@href')[0]
                        team = {}
                        team['key'] = re.findall(r'clubcode=(.*?)&',team_url)[0]
                        team_ids = team_id[team['key']]
                        team['logo_url'] = team_info.xpath('./div[@class="RoasterImage"]/a/img/@src')[0]
                        team['name_en'] = team_info.xpath('./div[@class="RoasterName"]/a/text()')[0]
                        team['sport_id'] = 2
                        print('team:',team)
                        data = {
                            'key': team['key'],
                            'name_en': team['name_en'],
                            'sport_id': team['sport_id'],

                        }
                        spx_dev_session = MysqlSvr.get('spider_zl')
                        BleaguejpBasketballTeam.upsert(
                            spx_dev_session,
                            'key',
                            data
                        )
                    player_list_urls = player_list_tree.xpath('//div[@class="teams"]/div[@class="item"]/div[@class="RoasterImage"]/a/@href')
                    for player_list_url in player_list_urls:
                        player_list_res = requests.get(start_url+player_list_url,headers=headers)
                        player_list_tree = tree_parse(player_list_res)
                        player_urls = player_list_tree.xpath('//div[@class="wp-module"]/div[contains(@class,"item")]/div[@class="img"]/a/@href')
                        for player_url in player_urls[:-1]:
                            player={}
                            print(start_url+player_url)
                            player_res = requests.get(start_url+player_url,headers=headers)
                            player_tree = tree_parse(player_res)
                            player['sport_id'] = 2
                            try:
                                player['name_en'] = player_tree.xpath('//div[@class="name"]/text()')[0]
                            except:
                                print('请求失败。。')
                            player['id'] = re.findall(r'pcode=(.*?)&',player_url)[0]
                            print(player['id'])
                            try:
                                player_img = player_tree.xpath('//div[@class="player-img"]/img/@src')[0]
                            except:
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
                            coach_key = re.findall(r'pcode=(.*?)&', player_url)[0]
                            manager_ids = manager_id[coach_key]
                            print('player:',player)
                            data = {
                                'key': player['id'],
                                'name_en': player['name_en'],
                                'sport_id': player['sport_id'],
                                'age': player['age'],
                                'birthday': player['birthday'],
                                'nationality': player['nationality'],
                                'height': player['height'],
                                'shirt_number': player['shirt_number'],
                                'position': player['position'],
                                'team_id' : team_ids,
                                'manager_id' : manager_ids,
                            }
                            spx_dev_session = MysqlSvr.get('spider_zl')
                            BleaguejpBasketballPlayer.upsert(
                                spx_dev_session,
                                'key',
                                data
                            )
                        coach_res = requests.get(start_url + player_urls[-1], headers=headers)
                        coach_tree = tree_parse(coach_res)
                        coach={}
                        coach['sport_id'] = 2
                        coach['key'] = re.findall(r'pcode=(.*?)&', player_url)[0]
                        coach['name_en'] = coach_tree.xpath('//div[@class="name"]/text()')[0]
                        try:
                            coach_img = coach_tree.xpath('//div[@class="coach-img"]/img/@src')[0]
                        except:
                            print('没有该教练的图片...')
                        time_birthday = coach_tree.xpath('//div[@class="summary-second"]/span[1]/text()')[0]
                        coach['birthday'], coach['age'] = time_stamp(time_birthday)
                        try:
                            coach['nationality'] = coach_tree.xpath('//div[@class="summary-second"]/span[2]/text()')[0].split(':')[-1]
                        except:
                            coach['nationality'] = ''
                            print('没有教练的国籍信息...')
                        print('coach:',coach)
                        data = {
                            'key' : coach['key'],
                            'name_en' : coach['name_en'],
                            'sport_id' : coach['sport_id'],
                            'birthday' : coach['birthday'],
                            'age' : coach['age'],
                            'nationality' : coach['nationality'],
                        }
                        spx_dev_session = MysqlSvr.get('spider_zl')
                        BleaguejpBasketballManager.upsert(
                            spx_dev_session,
                            'key',
                            data
                        )
    except Exception as e:
        print(e)


schedule.every(6).hour.do(info_spider)

while True:
    schedule.run_pending()
    time.sleep(30)





