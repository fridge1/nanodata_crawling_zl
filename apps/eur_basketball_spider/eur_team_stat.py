from apps.eur_basketball_spider.eur_playbyplay import *
from orm_connection.eur_basketball import *
from orm_connection.orm_session import MysqlSvr
import requests
import json
import re
from common.libs.log import LogMgr

logger = LogMgr.get('eur_basketball_team_stat_end')


def team_stat_end(season_id, gamecode):
    while True:
        headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        }
        code = re.findall(r'gamecode=(.*?)&', gamecode)[0]
        box_api_url = 'https://live.euroleague.net/api/Boxscore?gamecode=%s&seasoncode=E%s&disp=' % (code, season_id)
        box_api_res = requests.get(box_api_url, headers=headers)
        if box_api_res.text == '':
            logger.info('比赛未开赛...')
        else:
            box_api_dict = json.loads(box_api_res.text)
            count = 1
            for team_box in box_api_dict['Stats']:
                sport_id = 2
                match_id = int(
                    str(int(str(seasons[str(season_id) + '-' + str(season_id + 1)]) + '0000') + int(code)) + str(count))
                team_key = team_box['PlayersStats'][0]['Team']
                team_id = get_team_id_name(team_key)
                two_pointers_scored = int(team_box['totr']['FieldGoalsMade2'])
                two_pointers_total = int(team_box['totr']['FieldGoalsAttempted2'])
                if two_pointers_total == 0:
                    two_pointers_accuracy = 0
                else:
                    two_pointers_accuracy = round((two_pointers_scored / two_pointers_total) * 100)
                three_pointers_scored = int(team_box['totr']['FieldGoalsMade3'])
                three_pointers_total = int(team_box['totr']['FieldGoalsAttempted3'])
                if three_pointers_total == 0:
                    three_pointers_accuracy = 0
                else:
                    three_pointers_accuracy = round((three_pointers_scored / three_pointers_total) * 100)
                field_goals_scored = two_pointers_scored + three_pointers_scored
                field_goals_total = two_pointers_total + three_pointers_total
                if field_goals_total == 0:
                    field_goals_accuracy = 0
                else:
                    field_goals_accuracy = round((field_goals_scored / field_goals_total) * 100)
                free_throws_scored = int(team_box['totr']['FreeThrowsMade'])
                free_throws_total = int(team_box['totr']['FreeThrowsAttempted'])
                if free_throws_total == 0:
                    free_throws_accuracy = 0
                else:
                    free_throws_accuracy = round((free_throws_scored / free_throws_total) * 100)
                total_fouls = int(team_box['totr']['FoulsCommited'])
                defensive_rebounds = int(team_box['totr']['DefensiveRebounds'])
                offensive_rebounds = int(team_box['totr']['OffensiveRebounds'])
                rebounds = defensive_rebounds + offensive_rebounds
                assists = int(team_box['totr']['Assistances'])
                turnovers = int(team_box['totr']['Turnovers'])
                steals = int(team_box['totr']['Steals'])
                blocks = int(team_box['totr']['BlocksFavour'])
                successful_attempts = field_goals_scored
                data = {
                    'sport_id': sport_id,
                    'match_id': match_id,
                    'team_id': team_id,
                    'free_throws_scored': free_throws_scored,
                    'free_throws_total': free_throws_total,
                    'free_throws_accuracy': free_throws_accuracy,
                    'two_pointers_scored': two_pointers_scored,
                    'two_pointers_total': two_pointers_total,
                    'two_pointers_accuracy': two_pointers_accuracy,
                    'three_pointers_scored': three_pointers_scored,
                    'three_pointers_total': three_pointers_total,
                    'three_pointers_accuracy': three_pointers_accuracy,
                    'field_goals_scored': field_goals_scored,
                    'field_goals_total': field_goals_total,
                    'field_goals_accuracy': field_goals_accuracy,
                    'defensive_rebounds': defensive_rebounds,
                    'offensive_rebounds': offensive_rebounds,
                    'rebounds': rebounds,
                    'assists': assists,
                    'turnovers': turnovers,
                    'steals': steals,
                    'blocks': blocks,
                    'successful_attempts': successful_attempts,
                    'total_fouls': total_fouls,
                }
                spx_dev_session = MysqlSvr.get('spider_zl')
                BleaguejpBasketballTeamStats.upsert(
                    spx_dev_session,
                    'match_id',
                    data
                )
                count += 1
                logger.info(data)
            minutes_team = box_api_dict['Live']
            if minutes_team == False:
                break
            else:
                continue


def team_stat_run():
    try:
        season_id = 2019
        gamecode_urls = get_match_id()
        for gamecode in gamecode_urls:
            team_stat_end(season_id, gamecode)
    except:
        logger.error(traceback.format_exc())
        dingding_alter(traceback.format_exc())
