import requests
import json
from apps.NBL.tools import *
import os



headers = {
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            }
# url = 'https://api.nbl.com.au/_/custom/api/genius?route=leagues/7/competitions&competitionName=NBL&fields=season,competitionId&limit=500&filter[owner]=nbl'
# res = requests.get(url,headers=headers)
# match_dict = json.loads(res.text)
# match_info_dict = {}
# for data in match_dict['data']:
#     match_info_dict[data['season']] = data['competitionId']
# for competitionId in match_info_dict.values():
competitionId = 24346
match_url = 'https://api.nbl.com.au/_/custom/api/genius?route=competitions/%s/matches&matchType=REGULAR&limit=200&fields=matchId,matchStatus,matchTimeUTC,competitors,roundNumber,venue,ticketURL&liveapidata=false&filter[owner]=nbl' % (
                competitionId)
res = requests.get(match_url,headers=headers)
match_dict = json.loads(res.text)
for data in match_dict['data']:
    id = data['matchId']
    print(id)
    sport_id = 2
    competition_id = 7
    season_id = competitionId
    for index in data['competitors']:
        if index['isHomeCompetitor'] == 1:
            home_team_id = index['teamId']
        elif index['isHomeCompetitor'] == 0:
            away_team_id = index['teamId']
        else:
            print('主客队字段问题。。。')
    venue_id = data['venue']['venueId']
    matchTimeUTC = data['matchTimeUTC']
    match_time = change_bjtime(matchTimeUTC)
    round_num = data['roundNumber']
    try:
        if 'COMPLETE' in data['matchStatus']:
            status_id = 10
            game_url = 'https://www.fibalivestats.com/data/%s/data.json' % id
            game_res = requests.get(game_url, headers=headers)
            if game_res.status_code == 200:
                game_dict = json.loads(game_res.text)
                home_score = game_dict['tm']['1']['tot_sPoints']
                away_score = game_dict['tm']['2']['tot_sPoints']
                home_half_score = game_dict['tm']['1']['p1_score'] + game_dict['tm']['1']['p2_score']
                away_half_score = game_dict['tm']['2']['p1_score'] + game_dict['tm']['2']['p2_score']
                home_p1_score = game_dict['tm']['1']['p1_score']
                home_p2_score = game_dict['tm']['1']['p2_score']
                home_p3_score = game_dict['tm']['1']['p3_score']
                home_p4_score = game_dict['tm']['1']['p4_score']
                if home_score != home_p1_score + home_p2_score + home_p3_score + home_p4_score:
                    home_p5_score = game_dict['tm']['1']['ot_score']
                    home_scores = [home_p1_score, home_p2_score, home_p3_score, home_p4_score, home_p5_score, home_score]
                else:
                    home_scores = [home_p1_score, home_p2_score, home_p3_score, home_p4_score, home_score]
                away_p1_score = game_dict['tm']['2']['p1_score']
                away_p2_score = game_dict['tm']['2']['p2_score']
                away_p3_score = game_dict['tm']['2']['p3_score']
                away_p4_score = game_dict['tm']['2']['p4_score']
                if away_score != away_p1_score + away_p2_score + away_p3_score + away_p4_score:
                    away_p5_score = game_dict['tm']['2']['ot_score']
                    away_scores = [away_p1_score, away_p2_score, away_p3_score, away_p4_score, away_p5_score, away_score]
                else:
                    away_scores = [away_p1_score, away_p2_score, away_p3_score, away_p4_score, away_score]
                data = {
                    'id': id,
                    'status_id': status_id,
                    'competition_id': competition_id,
                    'season_id': season_id,
                    'home_team_id': home_team_id,
                    'away_team_id': away_team_id,
                    'venue_id': venue_id,
                    'match_time': match_time,
                    'round_num': round_num,
                    'home_score': home_score,
                    'away_score': away_score,
                    'home_half_score': home_half_score,
                    'away_half_score': away_half_score,
                    'home_scores': str(home_scores),
                    'away_scores': str(away_scores),
                    'sport_id': sport_id,
                }
                print(data)
                spx_dev_session = MysqlSvr.get('spider_zl')
                BleagueNblBasketballMatch.upsert(
                    spx_dev_session,
                    'id',
                    data
                )
            else:
                status_id = 10
                home_score = 0
                away_score = 0
                home_half_score = 0
                away_half_score = 0
                home_scores = 0
                away_scores = 0
        else:
            status_id = 1
            home_score = 0
            away_score = 0
            home_half_score = 0
            away_half_score = 0
            home_scores = 0
            away_scores = 0
            data = {
                'id': id,
                'status_id': status_id,
                'competition_id': competition_id,
                'season_id': season_id,
                'home_team_id': home_team_id,
                'away_team_id': away_team_id,
                'venue_id': venue_id,
                'match_time': match_time,
                'round_num': round_num,
                'home_score': home_score,
                'away_score': away_score,
                'home_half_score': home_half_score,
                'away_half_score': away_half_score,
                'home_scores': str(home_scores),
                'away_scores': str(away_scores),
                'sport_id': sport_id,
            }
            print(data)
            spx_dev_session = MysqlSvr.get('spider_zl')
            BleagueNblBasketballMatch.upsert(
                spx_dev_session,
                'id',
                data
            )
    except Exception as e:
        print(e)