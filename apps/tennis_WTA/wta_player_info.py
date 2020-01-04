import requests
import json
from apps.tennis_WTA.tools import *
from orm_connection.orm_session import MysqlSvr
from orm_connection.tennis import TennisCity,TennisPlayer
import re



class GetPlayerInfo(object):
    def __init__(self):
        self.double_dict = get_double_player_id()
        self.single_dict = get_single_player_id()
        self.session = MysqlSvr.get('spider_zl')
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.plays_dict = {
            'Right-Handed': 2,
            'Left-Handed': 1,
            'N/A' : 0,
        }
        self.city_id = get_city_id()
        self.single_name_dict = get_player_single_name()
        self.double_name_dict = get_player_double_name()


    def set_id(self):
        double_key = list(self.double_dict.keys())
        single_key = list(self.single_dict.keys())
        total_key = list(set(double_key + single_key))
        return total_key


    def get_city(self):
        url = 'https://www.wtatennis.com/players/%s/%s'
        total_key = self.set_id()
        for key in total_key:
            city_info = {}

            if key in self.single_dict.keys():
                res = requests.get(url % (key, self.single_dict[key]), headers=self.headers)
                print(url % (key, self.single_dict[key]))
            else:
                res = requests.get(url % (key, self.double_dict[key]), headers=self.headers)
                print(url % (key, self.double_dict[key]))
            res_tree = tree_parse(res)
            city_info['name_en'] = res_tree.xpath('//div[@class="player-header-info__detail player-header-info__birthplace"]/div[@class="player-header-info__detail-stat--small"]/text()')[0].strip()
            TennisCity.upsert(
                self.session,
                'name_en',
                city_info
            )



    def get_player_info(self):
        url = 'https://www.wtatennis.com/players/%s/%s'
        total_key = self.set_id()
        for key in total_key:
            player_info = {}
            if key in self.single_dict.keys():
                res = requests.get(url % (key,self.single_dict[key]),headers=self.headers)
                print(url % (key,self.single_dict[key]))
            else:
                res = requests.get(url % (key, self.double_dict[key]), headers=self.headers)
                print(url % (key, self.double_dict[key]))
            res_tree = tree_parse(res)
            player_info['id'] = key
            player_info['sport_id'] = 3
            height_m = res_tree.xpath('//div[@class="player-header-info__detail-stat--small"]/text()')[0].strip()
            height_m = re.findall('\d+',height_m)
            if height_m:
                height_cm = ''.join(height_m)
            else:
                height_cm = 0
            player_info['height'] = int(height_cm)
            player_info['nationality'] = res_tree.xpath('//div[@class="player-header-info__nationalityCode"]/text()')[0].strip()
            player_info['gender'] = 2
            if key in list(self.single_name_dict):
                player_info['name_en'] = self.single_name_dict[key]
            elif key in list(self.double_name_dict):
                player_info['name_en'] = self.double_name_dict[key]
            else:
                player_info['name_en'] = ''
            try:
                birthday = res_tree.xpath('//div[@class="player-header-info__detail-stat js-player-header-info__age"]/@data-dob')[0]
            except:
                birthday = 'N/A'
            player_info['birthday'],player_info['age'] = time_stamp(birthday)
            player_info['plays'] = self.plays_dict[res_tree.xpath('//div[@class="player-header-info__detail player-header-info__handed"]/div[@class="player-header-info__detail-stat--small"]/text()')[0].strip()]
            city_name = res_tree.xpath('//div[@class="player-header-info__detail player-header-info__birthplace"]/div[@class="player-header-info__detail-stat--small"]/text()')[0].strip()
            if city_name in list(self.city_id.keys()):
                player_info['city_id'] = self.city_id[res_tree.xpath('//div[@class="player-header-info__detail player-header-info__birthplace"]/div[@class="player-header-info__detail-stat--small"]/text()')[0].strip()]
            else:
                player_info['city_id'] = 0
            print(player_info)
            TennisPlayer.upsert(
                self.session,
                'id',
                player_info
            )



