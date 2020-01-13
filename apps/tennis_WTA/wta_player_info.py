import requests
from apps.tennis_WTA.tools import *
from orm_connection.orm_session import MysqlSvr
from orm_connection.tennis import TennisCity, TennisPlayer, TennisPlayerCareer
import re
import traceback
from common.libs.log import LogMgr

logger = LogMgr.get('wta_tennis_player_info')


class GetPlayerInfo(object):
    def __init__(self):
        self.session = MysqlSvr.get('spider_zl')
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.plays_dict = {
            'Right-Handed': 2,
            'Left-Handed': 1,
            'N/A': 0,
        }
        self.city_id = get_city_id()

    def get_city(self, player_id, name):
        url = 'https://www.wtatennis.com/players/%s/%s' % (player_id, replace_text(name))
        city_info = {}
        res = requests.get(url, headers=self.headers)
        res_tree = tree_parse(res)
        city_info['name_en'] = res_tree.xpath(
            '//div[@class="player-header-info__detail player-header-info__birthplace"]/div[@class="player-header-info__detail-stat--small"]/text()')[
            0].strip()
        TennisCity.upsert(
            self.session,
            'name_en',
            city_info
        )

    def get_player_info(self, player_id, name):
        url = 'https://www.wtatennis.com/players/%s/%s' % (player_id, replace_text(name))
        res = requests.get(url, headers=self.headers)
        player_info = {}
        res_tree = tree_parse(res)
        player_info['id'] = player_id
        player_info['sport_id'] = 3
        height_m = res_tree.xpath('//div[@class="player-header-info__detail-stat--small"]/text()')[0].strip()
        height_m = re.findall('\d+', height_m)
        if height_m:
            height_cm = ''.join(height_m)
        else:
            height_cm = 0
        player_info['height'] = int(height_cm)
        player_info['nationality'] = res_tree.xpath('//div[@class="player-header-info__nationalityCode"]/text()')[
            0].strip()
        player_info['gender'] = 2
        player_info['name_en'] = name
        try:
            birthday = \
                res_tree.xpath('//div[@class="player-header-info__detail-stat js-player-header-info__age"]/@data-dob')[
                    0]
        except:
            birthday = 'N/A'
        player_info['birthday'], player_info['age'] = time_stamp(birthday)
        player_info['plays'] = self.plays_dict[res_tree.xpath(
            '//div[@class="player-header-info__detail player-header-info__handed"]/div[@class="player-header-info__detail-stat--small"]/text()')[
            0].strip()]
        city_name = res_tree.xpath(
            '//div[@class="player-header-info__detail player-header-info__birthplace"]/div[@class="player-header-info__detail-stat--small"]/text()')[
            0].strip()
        if city_name in list(self.city_id.keys()):
            player_info['city_id'] = self.city_id[res_tree.xpath(
                '//div[@class="player-header-info__detail player-header-info__birthplace"]/div[@class="player-header-info__detail-stat--small"]/text()')[
                0].strip()]
        else:
            player_info['city_id'] = 0
        logger.info(player_info)
        TennisPlayer.upsert(
            self.session,
            'id',
            player_info
        )

    def get_player_career(self, player_id, name):
        url = 'https://www.wtatennis.com/players/%s/%s' % (player_id, replace_text(name))
        res = requests.get(url, headers=self.headers)
        player_career = {}
        res_tree = tree_parse(res)
        single_data_list = res_tree.xpath(
            '//div[@class="player-header-stats__value js-player-header-stat-count-up"]/@data-single')
        double_data_list = res_tree.xpath(
            '//div[@class="player-header-stats__value js-player-header-stat-count-up"]/@data-double')
        double_win_lost = res_tree.xpath('//span[@class="js-player-header-stat-count-up"]/@data-double')
        single_win_lost = res_tree.xpath('//span[@class="js-player-header-stat-count-up"]/@data-single')
        player_career['player_id'] = player_id
        player_career['sport_id'] = 3
        if len(single_data_list) == 6:
            player_career['single_titles'] = single_data_list[4]
            player_career['single_high'] = single_data_list[3]
            player_career['prize_money'] = single_data_list[5]
        else:
            player_career['single_titles'] = 0
            player_career['single_high'] = 0
            player_career['prize_money'] = 0
        if len(double_data_list) == 6:
            player_career['double_titles'] = double_data_list[4]
            player_career['double_high'] = double_data_list[3]
        else:
            player_career['double_titles'] = 0
            player_career['double_high'] = 0
        if len(double_win_lost) == 6:
            player_career['double_win'] = double_win_lost[2]
            player_career['double_lost'] = double_win_lost[3]
        else:
            player_career['double_win'] = 0
            player_career['double_lost'] = 0
        if len(single_win_lost) == 4:
            player_career['single_win'] = single_win_lost[2]
            player_career['single_lost'] = single_win_lost[3]
        else:
            player_career['single_win'] = 0
            player_career['single_lost'] = 0
        TennisPlayerCareer.upsert(
            self.session,
            'player_id',
            player_career
        )
        logger.info(player_career)

    def get_single_player(self):
        session = MysqlSvr.get('spider_zl')
        for row in TennisPlayerInfoSingleRank.inter(
                session=session,
                key='id',
                per_page=1000
        ):
            try:
                self.get_city(row.player_id, row.name_en)
                self.get_player_info(row.player_id, row.name_en)
                self.get_player_career(row.player_id, row.name_en)
            except:
                logger.error(traceback.format_exc())
                continue

    def get_double_player(self):
        session = MysqlSvr.get('spider_zl')
        for row in TennisPlayerInfoDoubleRank.inter(
                session=session,
                key='id',
                per_page=1000
        ):
            try:
                self.get_city(row.player_id, row.name_en)
                self.get_player_info(row.player_id, row.name_en)
                self.get_player_career(row.player_id, row.name_en)
            except:
                logger.error(traceback.format_exc())
                continue
