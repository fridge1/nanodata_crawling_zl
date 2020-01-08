import requests
from apps.eur_basketball_spider.tools import tree_parse,team_id,table_id
import re
from orm_connection.orm_session import MysqlSvr
from orm_connection.eur_basketball import BleagueEurBasketballTable,BleagueNblBasketballTableRow



class GetTable(object):
    def __init__(self):
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
        self.season_id = {
            '2016':10,
            '2017':11,
            '2018':12,
            '2019':13,
        }
        self.session = MysqlSvr.get('spider_zl')
        self.team_id = team_id
        self.table_id = table_id()

    def season_type_url(self):
        total_type_urls = []
        for season_id in range(2016, 2020):
            res = requests.get('https://www.euroleague.net/main/standings?seasoncode=E%s' % season_id,
                               headers=self.headers)
            res_tree = tree_parse(res)
            type_url = res_tree.xpath('//div[@class="styled-select"][2]/select/option/@value')[-1]
            total_type_urls.append(type_url)
        return total_type_urls

    def round_url(self):
        total_type_urls = self.season_type_url()
        total_round_urls = []
        for type_url in total_type_urls:
            res = requests.get('https://www.euroleague.net' + type_url, headers=self.headers)
            res_tree = tree_parse(res)
            round_url = res_tree.xpath('//div[@class="styled-select"][3]/select/option/@value')[-1]
            total_round_urls.append(round_url)
        return total_round_urls

    def match_url(self):
        total_round_urls = self.round_url()
        for round_url in total_round_urls:
            res = requests.get('https://www.euroleague.net' + round_url, headers=self.headers)
            res_tree = tree_parse(res)
            match_url = res_tree.xpath('//ul[@class="rounds-list"]/li/a/@href')[-1]
            res = requests.get('https://www.euroleague.net'+match_url,headers=self.headers)
            print('https://www.euroleague.net'+match_url)
            res_tree = tree_parse(res)
            table_row_infos = res_tree.xpath('//tbody/tr')
            for table_row_info in table_row_infos:
                table_info = {}
                season_id = re.findall(r'\d+',match_url)[-1]
                table_info['season_id'] = self.season_id[str(season_id)]
                table_info['sport_id'] = 2
                table_name_zh = str(season_id)+'-'+str(int(season_id) + 1)+'赛季积分榜'
                rank_name = table_row_info.xpath('./td[1]/a/text()')[0].strip().split('.')
                table_info['position'] = rank_name[0]
                team_url = table_row_info.xpath('./td[1]/a/@href')[0]
                team_key = re.findall(r'clubcode=(.*?)&',team_url)[0]
                table_info['team_id'] = self.team_id[team_key]
                table_info['table_id'] = self.table_id[table_name_zh]
                table_info['key'] = str(season_id) + str(table_info['team_id'])
                detail = {}
                detail['win'] = int(table_row_info.xpath('./td[2]/text()')[0].strip())
                detail['lost'] = int(table_row_info.xpath('./td[3]/text()')[0].strip())
                detail['won_rate'] = int(detail['win']/(detail['win']+detail['lost']) * 100)
                win_pts = int(table_row_info.xpath('./td[4]/text()')[0].strip())
                lost_pts = int(table_row_info.xpath('./td[5]/text()')[0].strip())
                detail['points_avg'] = round(win_pts / (detail['win'] + detail['lost']))
                detail['points_against_avg'] = round(lost_pts / (detail['win'] + detail['lost']))
                diff_avg_score = int(table_row_info.xpath('./td[6]/text()')[0].strip())
                detail['diff_avg'] = round(diff_avg_score / (detail['win'] + detail['lost']))
                table_info['detail'] = str(detail)
                BleagueNblBasketballTableRow.upsert(
                    self.session,
                    'key',
                    table_info
                )
                print(table_info)



if __name__ == '__main__':
    GetTable().match_url()