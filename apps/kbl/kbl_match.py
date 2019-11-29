import requests
from apps.kbl.tools import *



headers = {
    'user_agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
url = 'https://www.kbl.or.kr/schedule/today/todaygame.asp'
res = requests.get(url,headers=headers)
res_tree = tree_parse(res)
year_list = res_tree.xpath('//select[@name="SchYear"]/option/@value')
month_list = res_tree.xpath('//select[@name="SchMonth"]/option/@value')
for year in year_list:
    for month in month_list:
        data = {
            'SeachFlag': 'T',
            'SchSeason': 'S1',
            'SchYear': '%d' % year,
            'SchMonth': '%d' % month,
        }
        match_res = requests.post(url,data=data,headers=headers)
        match_tree = tree_parse(match_res)

