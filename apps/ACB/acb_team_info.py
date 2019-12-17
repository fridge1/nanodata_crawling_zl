import requests
from apps.ACB.tools import tree_parse
from orm_connection.orm_session import MysqlSvr
from orm_connection.acb_basketball import BleagueAcbBasketballTeam
import asyncio


def team_upsert(team_url):
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
    session = MysqlSvr.get('spider_zl')
    team_info = {}
    print('http://www.acb.com'+team_url)
    team_res = requests.get('http://www.acb.com'+team_url,headers=headers)
    team_tree = tree_parse(team_res)
    team_info['id'] = int(team_url.split('/')[-1])
    team_info['sport_id'] = 2
    try:
        team_info['manager_id'] = team_tree.xpath('//article[@class="caja_miembro_plantilla caja_entrenador_principal"]/div[@class="foto"]/a/@href')[0].split('/')[-1].split('-')[0]
    except:
        team_info['manager_id'] = 0
    try:
        team_info['name_en'] = team_tree.xpath('//div[@class="datos"]/h3/text()')[0]
    except:
        team_info['name_en'] = ''
    try:
        team_info['logo'] = 'http://www.acb.com' + team_tree.xpath('//div[@class="logo borde_club"]/img/@src')[0]
    except:
        team_info['logo'] = ''
    try:
        team_info['venue_id'] = team_tree.xpath('//ul[@class="roboto_bold"]/li[4]/a/@href')[0].split('/')[-1]
    except:
        team_info['venue_id'] = 0
    BleagueAcbBasketballTeam.upsert(
        session,
        'id',
        team_info
    )
    print(team_info)


def get_team_info():
    team_set = set()
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
    url = 'http://www.acb.com/club/index/temporada_id/2019'
    res = requests.get(url,headers=headers)
    res_tree = tree_parse(res)
    year_list = res_tree.xpath('//div[@id="listado_temporada"]/div/@data-t2v-id')
    for year in year_list:
        year_url = 'http://www.acb.com/club/index/temporada_id/%s' % year
        res = requests.get(year_url, headers=headers)
        res_tree = tree_parse(res)
        team_url_list = res_tree.xpath('//article[@class="club"]/h4/a/@href')
        for team_url in team_url_list:
            if team_url not in team_set:
                team_upsert(team_url)
            else:
                print('已经爬取过。。。')
            team_set.add(team_url)


get_team_info()