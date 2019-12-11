from apps.kbl.tools import *

headers = {
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
start_url = 'https://www.kbl.or.kr'
url = 'https://www.kbl.or.kr/common/js/menu.js?ver=1'
res = requests.get(url, headers=headers)
team_urls = re.findall(r'linknhd+(.*?);', res.text)
team_url_list = []
for team_url in team_urls:
    if 'teams' in team_url:
        a = team_url.replace('+', '').replace('\"', '')
        if a not in team_url_list:
            team_url_list.append(a)
team = {}
for team_info_url in team_url_list:
    team_id = re.findall(r'\d+', team_info_url)[0]
    team_res = requests.get(start_url + team_info_url, headers=headers)
    team_tree = tree_parse(team_res)
    team['logo'] = team_tree.xpath('//div[@class="top_g"]/img/@src')[0]
    team['name_en'] = team_tree.xpath('//strong[@class="team_name"]/text()')[0]
    team['sport_id'] = 2
    team['id'] = team_id
    manager_name = team_tree.xpath('//tr[1]/td[3]/text()')[0]
    assistant = team_tree.xpath('//tr[2]/td[1]/text()')[0]
    team['manager_id'] = get_manager_id(manager_name, team_id, assistant)
    city_name = team_tree.xpath('//tr[2]/td[2]/text()')[0]
    team['city_id'] = get_city_id(city_name)
    spx_dev_session = MysqlSvr.get('spider_zl')
    BleagueNblBasketballTeam.upsert(
        spx_dev_session,
        'id',
        team
    )
    player_url_list = team_tree.xpath('//ul[@class="playerlist_2019"]/li/dl/dd/a/@href')
    player = {}
    for player_url in player_url_list:
        player_res = requests.get(start_url + player_url, headers=headers)
        print(start_url + player_url)
        player_tree = tree_parse(player_res)
        player['id'] = re.findall(r'\d+', player_url)[0]
        player['sport_id'] = 2
        player['name_en'] = player_tree.xpath('//strong[@class="name"]/text()')[0]
        player['logo'] = player_tree.xpath('//div[@class="frame_g"]/img/@src')[0]
        try:
            birth = player_tree.xpath('//span[@class="birth"]/text()')[0].replace('.', '-')
            player['birthday'], player['age'] = age_timeStamp(birth)
        except:
            player['birthday'] = 0
            player['age'] = 0
        height = player_tree.xpath('//span[@class="stature"]/text()')[0]
        player['height'] = re.findall(r'\d+', height)[0]
        shirt_number = player_tree.xpath('//strong[@class="name"]/em/text()')[0]
        player['shirt_number'] = re.findall(r'\d+', shirt_number)[0]
        try:
            school = player_tree.xpath('//span[@class="school"]/text()')[0]
            if '-' in school:
                player['school'] = school.split('-')[-1].replace('\xa0', '')
            else:
                player['school'] = school
        except:
            player['school'] = ''
        player['school_id'] = get_school_id(player['school'])
        player['position'] = player_tree.xpath('//span[@class="position"]/text()')[0]
        player['team_id'] = team_id
        spx_dev_session = MysqlSvr.get('spider_zl')
        BleagueNblBasketballPlayer.upsert(
            spx_dev_session,
            'id',
            player
        )
