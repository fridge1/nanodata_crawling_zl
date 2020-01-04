import requests
import json
from apps.tennis_WTA.tools import get_single_player_id,get_double_player_id,tree_parse,time_stamp,get_city_id
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
        }
        self.city_id = get_city_id()


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
            else:
                res = requests.get(url % (key, self.double_dict[key]), headers=self.headers)
            res_tree = tree_parse(res)
            player_info['id'] = key
            player_info['sport_id'] = 3
            height_m = res_tree.xpath('//div[@class="player-header-info__detail-stat--small"]/text()')[0].strip()
            height_cm = ''.join(re.findall('\d+',height_m))
            player_info['height'] = height_cm
            player_info['nationality'] = res_tree.xpath('//div[@class="player-header-info__nationalityCode"]/text()')[0].strip()
            player_info['gender'] = 2
            name_en = res_tree.xpath('//h1[@class="player-header-info__name"]')
            player_info['name_en'] = name_en[0].xpath('string(.)')
            try:
                birthday = res_tree.xpath('//div[@class="player-header-info__detail-stat js-player-header-info__age"]/@data-dob')[0]
            except:
                birthday = 'N/A'
            player_info['birthday'],player_info['age'] = time_stamp(birthday)
            player_info['plays'] = self.city_id[res_tree.xpath('//div[@class="player-header-info__detail player-header-info__handed"]/div[@class="player-header-info__detail-stat--small"]/text()')[0].strip()]
            TennisPlayer.upsert(
                self.session,
                'id',
                player_info
            )
            print(player_info)


