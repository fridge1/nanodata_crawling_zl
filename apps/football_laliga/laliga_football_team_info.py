import requests
import json
from apps.football_laliga.tools import replace_text


headers = {
    'user_agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
    'Ocp-Apim-Subscription-Key' : 'c13c3a8e2f6b46da9c5c425cf61fab3e'
}

url = 'https://apim.laliga.com/public-service/api/v1/teams?subscriptionSlug=laliga-santander-%s&limit=99&offset=0&orderField=nickname&orderType=ASC'
for year in range(2013,2020):
    res = requests.get(url % str(year),headers=headers)
    infos = json.loads(res.text)
    for info in infos['teams']:
        team_info = {}
        team_info['id'] = info['id']
        team_info['name_en'] = info['name']
        team_info['name_short'] = info['nickname']
        team_info['url'] = 'https://www.laliga.com/en-GB/clubs/'+ replace_text(info['name']).replace(' ','-')
        print(team_info)