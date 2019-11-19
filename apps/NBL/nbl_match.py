import requests
import json
from apps.NBL.tools import *




headers = {
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            }
url = 'https://api.nbl.com.au/_/custom/api/genius?route=competitions/24346/matches&matchType=REGULAR&limit=500&fields=matchId,matchStatus,matchTimeUTC,competitors,roundNumber,venue,ticketURL&liveapidata=false&filter[owner]=nbl'
res = requests.get(url,headers=headers)
match_dict = json.loads(res.text)
for data in match_dict['data']:
    id = data['matchId']
    if 'COMPLETE' in data['matchStatus']:
        status_id = 10
    else:
        status_id = 1
    competition_id = 7
    season_id = 24346
    home_team_id = data['competitors'][0]['teamId']
    away_team_id = data['competitors'][1]['teamId']
    venue_id = data['venue']['venueId']
    matchTimeUTC = data['matchTimeUTC']
    match_time = change_bjtime(matchTimeUTC)
    round_num = data['roundNumber']
    game_url = 'https://www.fibalivestats.com/data/%s/data.json' % id
    game_res = requests.get(game_url,headers=headers)
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
        home_p5_score = game_dict['tm']['1']['p5_score']
        home_scores = [home_p1_score,home_p2_score,home_p3_score,home_p4_score,home_p5_score,home_score]
    away_p1_score = game_dict['tm']['2']['p1_score']
    away_p2_score = game_dict['tm']['2']['p2_score']
    away_p3_score = game_dict['tm']['2']['p3_score']
    away_p4_score = game_dict['tm']['2']['p4_score']
    if away_score == away_p1_score + away_p2_score + away_p3_score + away_p4_score:
        away_scores = [away_p1_score,away_p2_score,away_p3_score,away_p4_score,away_score]
    id = data['matchId']
    id = data['matchId']
    id = data['matchId']
    id = data['matchId']
    id = data['matchId']
    id = data['matchId']
    id = data['matchId']
    id = data['matchId']
    id = data['matchId']
    id = data['matchId']
# url = 'https://api.nbl.com.au/_/custom/api/genius?route=leagues/7/competitions&competitionName=NBL&fields=season,competitionId&limit=500&filter[owner]=nbl'
# res = requests.get(url,headers=headers)
# match_dict = json.loads(res.text)
# match_info_dict = {}
# for data in match_dict['data']:
#     match_info_dict[data['season']] = data['competitionId']
# print(match_info_dict.values())
# for competitionId in match_info_dict.values():
#     match_url = 'https://api.nbl.com.au/_/custom/api/genius?route=competitions/%s/matches&matchType=REGULAR&limit=200&' \
#                 'fields=matchId,matchStatus,matchTimeUTC,competitors,roundNumber,venue,ticketURL&liveapidata=false&filter[owner]=nbl' % (competitionId)
#     match_res = requests.get(match_url, headers=headers)
#