import requests
from apps.eur_basketball_spider.tools import tree_parse


class GetTable(object):
    def __init__(self):
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }



    def table_info(self):
        url = 'https://www.euroleague.net/main/standings'
        res = requests.get(url,headers=self.headers)
        res_tree = tree_parse(res)
        season_urls = res_tree.xpath('//div[@class="styled-select"][1]/select/option/@value')
        return season_urls

    def season_type_url(self):
        season_urls = self.table_info()
        total_type_urls = []
        for season_url in season_urls:
            res = requests.get('https://www.euroleague.net' + season_url,headers=self.headers)
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
            res = requests.get('https://www.euroleague.net'+round_url,headers=self.headers)
            res_tree = tree_parse(res)
            match_urls = res_tree.xpath('//ul[@class="rounds-list"]/li/a/@href')
            print(match_urls)




