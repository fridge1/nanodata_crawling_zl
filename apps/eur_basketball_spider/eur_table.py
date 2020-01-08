import requests
from apps.eur_basketball_spider.tools import tree_parse
import re



class GetTable(object):
    def __init__(self):
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }

    def season_type_url(self):
        total_type_urls = []
        for season_id in range(2016, 2020):
            res = requests.get('https://www.euroleague.net/main/standings?seasoncode=%s' % season_id,
                               headers=self.headers)
            res_tree = tree_parse(res)
            type_urls = res_tree.xpath('//div[@class="styled-select"][2]/select/option/@value')
            total_type_urls += type_urls
        return total_type_urls

    def round_url(self):
        total_type_urls = self.season_type_url()
        total_round_urls = []
        for type_url in total_type_urls:
            res = requests.get('https://www.euroleague.net' + type_url, headers=self.headers)
            res_tree = tree_parse(res)
            round_urls = res_tree.xpath('//div[@class="styled-select"][3]/select/option/@value')
            total_round_urls += round_urls
        return total_round_urls

    def match_url(self):
        total_round_urls = self.round_url()
        for round_url in total_round_urls:
            res = requests.get('https://www.euroleague.net' + round_url, headers=self.headers)
            res_tree = tree_parse(res)
            match_urls = res_tree.xpath('//ul[@class="rounds-list"]/li/a/@href')
            for match_url in match_urls:
                res = requests.get('https://www.euroleague.net'+match_url,headers=self.headers)
                res_tree = tree_parse(res)
                typecode = re.findall(r'phasetypecode=(.*?)\+',match_url)[0]
                season_id = re.findall(r'seasoncode=E(.*?)',match_url)[0]
                if 'RS' or 'TS' in typecode:
                    stage_name_zh = '欧篮联%s-%s赛季常规赛' % (str(season_id), str(season_id + 1))
                else:
                    stage_name_zh = '欧篮联%s-%s赛季季后赛' % (str(season_id), str(season_id + 1))
                print(typecode,season_id)
