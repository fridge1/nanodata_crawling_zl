from apps.eur_basketball_spider.tools import *
from apps.eur_basketball_spider.eur_playbyplay import *
from orm_connection.eur_basketball import *
from orm_connection.orm_session import MysqlSvr
import requests
import json
import re
from common.libs.log import LogMgr
logger = LogMgr.get('eur_basketball_team_stat_end')



def player_stat_end(season_id,gamecode):
    count = 1
    while True:
        headers = {
            'user_agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        }
        code = re.findall(r'gamecode=(.*?)&', gamecode)[0]
        box_api_url = 'https://live.euroleague.net/api/Boxscore?gamecode=%s&seasoncode=E%s&disp=' % (code,season_id)
        box_api_res = requests.get(box_api_url,headers=headers)
        if box_api_res.text == '':
            print('比赛未开赛...')
        else:
            box_api_dict = json.loads(box_api_res.text)
            for index in range(2):
                for player_box in box_api_dict['Stats'][index]['PlayersStats']:
                    sport_id = 2
                    match_id = int(str(seasons[str(season_id)+'-'+str(season_id+1)]) + '0000') + int(code)
                    team_key = player_box['Team']
                    team_id = get_team_id(team_key)
                    player_key = player_box['Player_ID'][1:]
                    if player_key:
                        player_id = get_player_id_upsert(player_key)
                        position = get_player_position_upsert(player_key)
                    else:
                        player_id = ''
                        position = ''
                    IsStarter = player_box['IsStarter']
                    if IsStarter == 0:
                        first = 1
                    elif IsStarter == 1:
                        first = 0
                    else:
                        first = ''
                    points = player_box['Points']
                    free_throws_scored = int(player_box['FreeThrowsMade'])
                    free_throws_total = int(player_box['FreeThrowsAttempted'])
                    if free_throws_total == 0:
                        free_throws_accuracy = 0
                    else:
                        free_throws_accuracy = round((free_throws_scored / free_throws_total) * 100)
                    two_points_scored = int(player_box['FieldGoalsMade2'])
                    two_points_total = int(player_box['FieldGoalsAttempted2'])
                    if two_points_total == 0:
                        two_points_accuracy = 0
                    else:
                        two_points_accuracy = round((two_points_scored / two_points_total) * 100)
                    three_points_scored = int(player_box['FieldGoalsMade3'])
                    three_points_total = int(player_box['FieldGoalsAttempted3'])
                    if three_points_total == 0:
                        three_points_accuracy = 0
                    else:
                        three_points_accuracy = round((three_points_scored / three_points_total) * 100)
                    field_goals_scored = two_points_scored + three_points_scored
                    field_goals_total = two_points_total + three_points_total
                    if field_goals_total == 0:
                        field_goals_accuracy = 0
                    else:
                        field_goals_accuracy = round((field_goals_scored / field_goals_total) * 100)
                    defensive_rebounds = int(player_box['DefensiveRebounds'])
                    offensive_rebounds = int(player_box['OffensiveRebounds'])
                    rebounds = defensive_rebounds + offensive_rebounds
                    assists = int(player_box['Assistances'])
                    turnovers = int(player_box['Turnovers'])
                    steals = int(player_box['Steals'])
                    blocks = int(player_box['BlocksFavour'])
                    personal_fouls = int(player_box['FoulsCommited'])
                    plus_minus = int(player_box['Valuation'])
                    data = {
                        'id' : int(str(season_id) + str(code) + str(count)),
                        'sport_id' : sport_id,
                        'match_id' : match_id,
                        'team_id' : team_id,
                        'player_id' : player_id,
                        'position' : position,
                        'first' : first,
                        'points' : points,
                        'free_throws_scored' : free_throws_scored,
                        'free_throws_total' : free_throws_total,
                        'free_throws_accuracy' : free_throws_accuracy,
                        'two_points_scored' : two_points_scored,
                        'two_points_total' : two_points_total,
                        'two_points_accuracy' : two_points_accuracy,
                        'three_points_scored' : three_points_scored,
                        'three_points_total' : three_points_total,
                        'three_points_accuracy' : three_points_accuracy,
                        'field_goals_scored' : field_goals_scored,
                        'field_goals_total' : field_goals_total,
                        'field_goals_accuracy' : field_goals_accuracy,
                        'defensive_rebounds' : defensive_rebounds,
                        'offensive_rebounds' : offensive_rebounds,
                        'rebounds' : rebounds,
                        'assists' : assists,
                        'turnovers' : turnovers,
                        'steals' : steals,
                        'blocks' : blocks,
                        'personal_fouls' : personal_fouls,
                        'plus_minus' : plus_minus,
                    }
                    spx_dev_session = MysqlSvr.get('spider_zl')
                    BleaguejpBasketballPlayerStats.upsert(
                        spx_dev_session,
                        'id',
                        data
                    )
                    count += 1
                    print(data)
            minutes_team = box_api_dict['Stats'][0]['totr']['Minutes']
            if minutes_team and minutes_team == '200:00':
                break
            else:
                continue



def player_stat_run():
    try:
        headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
        start_url = 'https://www.euroleague.net/'
        url = 'https://www.euroleague.net/main/results?seasoncode=E%s'
        seasons_id = [2008,2009,2010,2012, 2013, 2015, 2016, 2017, 2018, 2019]
        for season_id in seasons_id:
            res = requests.get(url % str(season_id),headers=headers)
            res_tree = tree_parse(res)
            typecode_urls = res_tree.xpath('//div[@class="game-center-selector"]/div[2]/select/option/@value')
            for typecode_url in typecode_urls:
                typecode_res = requests.get(start_url + typecode_url, headers=headers)
                typecode_res_tree = tree_parse(typecode_res)
                round_urls = typecode_res_tree.xpath('//div[@class="game-center-selector"]/div[3]/select/option/@value')
                for round_url in round_urls:
                    round_res = requests.get(start_url + round_url, headers=headers)
                    round_res_tree = tree_parse(round_res)
                    gamecode_urls = round_res_tree.xpath('//div[@class="game played"]/a/@href|//div[@class="game "]/a/@href')
                    for gamecode in gamecode_urls:
                        player_stat_end(season_id, gamecode)
    except Exception as e:
        logger.error(e)


