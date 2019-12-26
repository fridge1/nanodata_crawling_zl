import requests
from apps.ACB.tools import tree_parse,change_match_bjtime
from orm_connection.orm_session import MysqlSvr
from orm_connection.acb_basketball import BleagueAcbBasketballManager
import asyncio
import re


def team_upsert(team_url):
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
    session = MysqlSvr.get('spider_zl')
    team_res = requests.get('http://www.acb.com'+team_url,headers=headers)
    print('http://www.acb.com'+team_url)
    team_tree = tree_parse(team_res)
    coach_url = team_tree.xpath('//article[@class="caja_miembro_plantilla caja_entrenador_principal"]/div[@class="foto"]/a/@href')
    if coach_url:
        coach_res = requests.get('http://www.acb.com'+coach_url[0],headers=headers)
        coach_tree = tree_parse(coach_res)
        coach_info = {}
        coach_info['id'] = re.findall(r'\d+',coach_url[0])[0]
        coach_info['team_id'] = int(team_url.split('/')[-1])
        coach_info['sport_id'] = 2
        coach_info['name_en'] = coach_tree.xpath('//div[@class="datos_secundarios roboto_condensed"]/span/text()')[0]
        coach_info['short_name_en'] = coach_tree.xpath('//div[@class="f-l-a-100 contenedora_datos_basicos"]/h1/text()')[0]
        date = coach_tree.xpath('//div[@class="datos_basicos fecha_nacimiento roboto_condensed"]/span[@class="roboto_condensed_bold"]/text()')[0].split(' ')[0]
        coach_info['short_name_en'] = coach_tree.xpath('//div[@class="f-l-a-100 contenedora_datos_basicos"]/h1/text()')[0]
        coach_info['birthday'],coach_info['age'] = change_match_bjtime(date)
        coach_info['nationality'] = coach_tree.xpath('//div[@class="datos_basicos nacionalidad roboto_condensed"]/span[@class="roboto_condensed_bold"]/text()')[0]
        coach_info['logo'] = 'http:'+coach_tree.xpath('//div[@class="foto"]/img/@src')[0]
        coach_info['type'] = 1
        BleagueAcbBasketballManager.upsert(
            session,
            'id',
            coach_info
        )
        print(coach_info)
    else:
        print('没有该球队的教练信息')
    assistant_coach_urls = team_tree.xpath('//div[@class="entrenadores_asistentes"]/article/div[@class="foto"]/a/@href')
    if assistant_coach_urls:
        for assistant_coach_url in assistant_coach_urls:
            coach_res = requests.get('http://www.acb.com' + assistant_coach_url, headers=headers)
            coach_tree = tree_parse(coach_res)
            coach_info = {}
            coach_info['id'] = re.findall(r'\d+', assistant_coach_url)[0]
            coach_info['team_id'] = int(team_url.split('/')[-1])
            coach_info['sport_id'] = 2
            coach_info['name_en'] = coach_tree.xpath('//div[@class="datos_secundarios roboto_condensed"]/span/text()')[
                0]
            coach_info['short_name_en'] = \
            coach_tree.xpath('//div[@class="f-l-a-100 contenedora_datos_basicos"]/h1/text()')[0]
            date = coach_tree.xpath(
                '//div[@class="datos_basicos fecha_nacimiento roboto_condensed"]/span[@class="roboto_condensed_bold"]/text()')[
                0].split(' ')[0]
            coach_info['short_name_en'] = \
            coach_tree.xpath('//div[@class="f-l-a-100 contenedora_datos_basicos"]/h1/text()')[0]
            coach_info['birthday'], coach_info['age'] = change_match_bjtime(date)
            coach_info['nationality'] = coach_tree.xpath(
                '//div[@class="datos_basicos nacionalidad roboto_condensed"]/span[@class="roboto_condensed_bold"]/text()')[
                0]
            coach_info['logo'] = 'http:' + coach_tree.xpath('//div[@class="foto"]/img/@src')[0]
            coach_info['type'] = 0
            BleagueAcbBasketballManager.upsert(
                session,
                'id',
                coach_info
            )
            print(coach_info)
    else:
        print('没有该球队的助理教练信息')



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