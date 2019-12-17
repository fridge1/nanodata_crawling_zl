import requests
from apps.ACB.tools import tree_parse
from orm_connection.orm_session import MysqlSvr
from orm_connection.acb_basketball import BleagueAcbBasketballPlayer
import asyncio


def team_upsert(team_url):
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
    session = MysqlSvr.get('spider_zl')
    player_info = {}
    print('http://www.acb.com' + team_url)
    team_res = requests.get('http://www.acb.com' + team_url, headers=headers)
    team_tree = tree_parse(team_res)
    player_url_list = team_tree.xpath('//div[@class="grid_plantilla principal"]/article/div[@class="foto"]/a/@href')
    for player_url in player_url_list:
        player_info['id'] = player_url.split('/')[-1].split('-')[0]
        player_res = requests.get('http://www.acb.com/jugador/temporada-a-temporada/id/%s', headers=headers)
        player_tree = tree_parse(player_res)
        player_info['name_en'] = player_tree.xpath('//div[@class="datos_secundarios roboto_condensed"]/span/text()')[0]
        player_info['short_name_en'] = \
        player_tree.xpath('//div[@class="f-l-a-100 contenedora_datos_basicos"]/h1/text()')[0]
        player_info['logo'] = player_tree.xpath('//div[@class="foto"]/img/@src')[0]
        player_info['shirt_number'] = \
        player_tree.xpath('//div[@class="datos_basicos dorsal roboto_condensed"]/span/text()')[0]
        player_info['position'] = \
        player_tree.xpath('//div[@class="datos_basicos posicion roboto_condensed"]/span/text()')[0]
        player_info['height'] = player_tree.xpath('//div[@class="datos_basicos altura roboto_condensed"]/span/text()')[
            0]
        player_info['city'] = player_tree.xpath(
            '//div[@class="datos_secundarios lugar_nacimiento roboto_condensed"]/span[@class="roboto_condensed_bold"]/text()')[
            0]
        born_time = player_tree.xpath('//div[@class="datos_secundarios fecha_nacimiento roboto_condensed"]/span[@class="roboto_condensed_bold"]/text()')[0]
        date = born_time.split(' ')
        player_info['team_id'] = int(team_url.split('/')[-1])
        player_info['sport_id'] = 2
        try:
            player_info['manager_id'] = team_tree.xpath(
                '//article[@class="caja_miembro_plantilla caja_entrenador_principal"]/div[@class="foto"]/a/@href')[
                0].split('/')[-1].split('-')[0]
        except:
            player_info['manager_id'] = 0
        BleagueAcbBasketballPlayer.upsert(
            session,
            'id',
            player_info
        )
        print(player_info)


def get_team_info():
    team_set = set()
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
    url = 'http://www.acb.com/club/index/temporada_id/2019'
    res = requests.get(url, headers=headers)
    res_tree = tree_parse(res)
    team_url_list = res_tree.xpath('//article[@class="club"]/h4/a/@href')
    for team_url in team_url_list:
        if team_url not in team_set:
            team_upsert(team_url)
        else:
            print('已经爬取过。。。')
        team_set.add(team_url)


get_team_info()
