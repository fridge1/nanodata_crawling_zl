import requests
from apps.ACB.tools import tree_parse,change_match_bjtime
from orm_connection.orm_session import MysqlSvr
from orm_connection.acb_basketball import BleagueAcbBasketballPlayer,BleagueAcbBasketballVenue
import re
import asyncio


def team_upsert(team_url):
    position_dict = {
        'Ala-pívot' : 'C',
        'Escolta' : 'SG',
        'Alero' : 'SF',
        'Pívot' : 'F',
        'Base' : 'PG',
    }
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
    session = MysqlSvr.get('spider_zl')
    player_info = {}
    venue_info = {}
    team_res = requests.get('http://www.acb.com' + team_url, headers=headers)
    team_tree = tree_parse(team_res)
    venue_url = 'http://www.acb.com' + team_tree.xpath('//ul[@class="roboto_bold"]/li[4]/a/@href')[0]
    venue_info['id'] = venue_url.split('/')[-1]
    venue_info['sport_id'] = 2
    venue_res = requests.get(venue_url,headers=headers)
    venue_tree = tree_parse(venue_res)
    venue_info['name_en'] = venue_tree.xpath('//div[@class="tagtitularsolido roboto_bold mayusculas"]/text()')[0]
    venue_info['city'] = venue_tree.xpath('//section[@class="datos_pabellon"]/div[@class="contenedora_informacion f-l-a-100"]//div[@class="datos"]/text()')[0]
    capacity1 = venue_tree.xpath('//section[@class="datos_pabellon"]/div[@class="contenedora_informacion f-l-a-100"]//div[@class="datos"]/text()')[1]
    venue_info['capacity'] = re.findall(r'\d+',capacity1.replace('.',''))[0]
    BleagueAcbBasketballVenue.upsert(
            session,
            'id',
            venue_info
        )
    print(venue_info)
    # player_url_list = team_tree.xpath('//div[@class="grid_plantilla principal"]/article/div[@class="foto"]/a/@href')
    # for player_url in player_url_list:
    #     player_info['id'] = player_url.split('/')[-1].split('-')[0]
    #     player_res = requests.get('http://www.acb.com/jugador/temporada-a-temporada/id/%s' % player_info['id'], headers=headers)
    #     print('http://www.acb.com/jugador/temporada-a-temporada/id/%s' % player_info['id'])
    #     player_tree = tree_parse(player_res)
    #     player_info['name_en'] = player_tree.xpath('//div[@class="datos_secundarios roboto_condensed"]/span/text()')[0]
    #     player_info['short_name_en'] = \
    #     player_tree.xpath('//div[@class="f-l-a-100 contenedora_datos_basicos"]/h1/text()')[0]
    #     player_info['logo'] = 'http:' + player_tree.xpath('//div[@class="foto"]/img/@src')[0]
    #     player_info['shirt_number'] = \
    #     player_tree.xpath('//div[@class="datos_basicos dorsal roboto_condensed"]/span/text()')[0]
    #     position = player_tree.xpath('//div[@class="datos_basicos posicion roboto_condensed"]/span/text()')[0]
    #     player_info['position'] = position_dict[position]
    #     height = player_tree.xpath('//div[@class="datos_basicos altura roboto_condensed"]/span/text()')[0]
    #     player_info['height'] = float(height.replace(',','.').replace('m','').strip()) * 100
    #     player_info['city'] = player_tree.xpath('//div[@class="datos_secundarios lugar_nacimiento roboto_condensed"]/span[@class="roboto_condensed_bold"]/text()')[0]
    #     born_time = player_tree.xpath('//div[@class="datos_secundarios fecha_nacimiento roboto_condensed"]/span[@class="roboto_condensed_bold"]/text()')[0]
    #     born = born_time.split(' ')[0]
    #     player_info['birthday'],player_info['age'] = change_match_bjtime(born)
    #     player_info['nationality'] = player_tree.xpath('//div[@class="datos_secundarios nacionalidad roboto_condensed"]/span[@class="roboto_condensed_bold"]/text()')[0]
    #     player_info['team_id'] = int(team_url.split('/')[-1])
    #     player_info['sport_id'] = 2
    #     BleagueAcbBasketballPlayer.upsert(
    #         session,
    #         'id',
    #         player_info
    #     )
    #     print(player_info)


def get_team_info():
    team_set = set()
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
    year_list = [2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
    for year in year_list:
        url = 'http://www.acb.com/club/index/temporada_id/%s'
        res = requests.get(url % year, headers=headers)
        res_tree = tree_parse(res)
        team_url_list = res_tree.xpath('//article[@class="club"]/h4/a/@href')
        for team_url in team_url_list:
            if team_url not in team_set:
                team_upsert(team_url)
            else:
                print('已经爬取过。。。')
            team_set.add(team_url)


get_team_info()
