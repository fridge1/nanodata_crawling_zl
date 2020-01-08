import requests
from apps.ACB.tools import tree_parse,get_table_id
from orm_connection.orm_session import MysqlSvr
from orm_connection.acb_basketball import BleagueAcbBasketballTable,BleagueAcbBasketballTableRow
import re


class GetAcbTableInfo(object):
    def __init__(self):
        self.headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
        self.session = MysqlSvr.get('spider_zl')
        self.table_id = get_table_id()


    def get_table_info(self,year):

        table_info = {}
        table_info['sport_id'] = 2
        table_info['season_id'] = year
        table_info['name_en'] = str(year) + '-' + str(year+1) + '赛季积分榜'
        BleagueAcbBasketballTable.upsert(
            self.session,
            'season_id',
            table_info
        )


    def get_table_row_info(self,year):
        url = 'http://www.acb.com/resultados-clasificacion/ver/temporada_id/%s/competicion_id/1/jornada_numero/34' % year
        res = requests.get(url,headers=self.headers)
        res_tree = tree_parse(res)
        table_infos = res_tree.xpath('//table/tbody/tr')
        for info in table_infos:
            table_row_info = {}
            table_row_info['position'] = info.xpath('./td[@class="posicion"]/div/text()')[0]
            team_url = info.xpath('./td[@class="nombre_equipo"]/a/@href')[0]
            table_row_info['team_id'] = re.findall(r'\d+',team_url)[0]
            name_en = str(year)+'-'+str(int(year)+1)+'赛季积分榜'
            table_row_info['table_id'] = self.table_id[name_en]
            table_row_info['sport_id'] = 2
            table_row_info['season_id'] = year
            table_row_info['key'] = str(table_row_info['season_id']) + str(table_row_info['team_id'])
            detail = {}
            detail['won'] = int(info.xpath('./td[@class="victorias"]/text()')[0])
            detail['lost'] = int(info.xpath('./td[@class="derrotas"]/text()')[0])
            detail['won_rate'] = round(detail['won']/(detail['won'] + detail['lost']) * 100)
            total_points = int(info.xpath('./td[7]/text()')[0].replace('.',''))
            total_lost_points = int(info.xpath('./td[8]/text()')[0].replace('.',''))
            total_matches = int(info.xpath('./td[4]/text()')[0])
            detail['points_avg'] = round(total_points/total_matches)
            detail['points_against_avg'] = round(total_lost_points/total_matches)
            diff_score = int(info.xpath('./td[9]/text()')[0])
            detail['diff_avg'] = round(diff_score/(detail['won']+detail['lost']))
            table_row_info['detail'] = str(detail)
            BleagueAcbBasketballTableRow.upsert(
                self.session,
                'key',
                table_row_info
            )




if __name__ == '__main__':
    for year in range(2010,2019):
        GetAcbTableInfo().get_table_row_info(year)
