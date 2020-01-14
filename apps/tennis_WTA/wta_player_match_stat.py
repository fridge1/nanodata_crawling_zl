import requests
from orm_connection.tennis import TennisMatch,TennisMatchPlayerStat,TennisMatchTotalStat
from orm_connection.orm_session import MysqlSvr
import json



class GetMatchPlayerStat(object):
    def __init__(self):
        self.session = MysqlSvr.get('spider_zl')
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }


    def get_match_info(self):
        rows = self.session.query(TennisMatch).all()
        for row in rows:
            season_id = row.key[:4]
            competition_id = row.key[4:-5]
            match_id = row.key[-5:]
            player_ids = [row.home_player_id] + [row.away_player_id]
            self.get_player_stat(competition_id,season_id,match_id,row.id,player_ids)



    def get_player_stat(self,competition_id,season_id,match_id,id,player_ids):
        url = 'https://api.wtatennis.com/tennis/tournaments/%s/%s/matches/%s/stats' % (competition_id,season_id,match_id)
        print(url)
        res = requests.get(url,headers=self.headers)
        infos = json.loads(res.text)
        if infos:
            for index in range(len(player_ids)):
                match_total = {}
                if index == 0:
                    match_total['key'] = str(id)+str(player_ids[index])
                    match_total['player_ids'] = player_ids[index]
                    match_total['sport_id'] = 3
                    match_total['match_id'] = id
                    match_total['aces'] = infos[0]['acesa']
                    match_total['double_faults'] = infos[0]['dblflta']
                    match_total['service_points_win'] = (infos[0]['ptstotwonserva'] / infos[0]['totservplayeda']) * 100
                    match_total['first_serve'] = (infos[0]['ptsplayed1stserva'] / infos[0]['totservplayeda']) * 100
                    match_total['first_serve_win'] = (infos[0]['ptswon1stserva'] / infos[0]['ptsplayed1stserva']) * 100
                    match_total['second_serve_win'] = (infos[0]['ptstotwonserva'] - infos[0]['ptswon1stserva']) / (infos[0]['totservplayeda'] - infos[0]['ptsplayed1stserva']) * 100
                    if infos[0]['breakptsplayedb'] != 0:
                        match_total['break_point_saved'] = infos[0]['breakptsconvb'] / infos[0]['breakptsplayedb'] * 100
                    else:
                        match_total['break_point_saved'] = 0
                    match_total['service_games_win'] = infos[0]['ptstotwonserva'] / infos[0]['totservplayeda'] * 100
                    match_total['service_games_played'] = infos[0]['servgamesplayeda']
                    match_total['return_games_played'] = infos[0]['servgamesplayedb']
                    match_total['first_return_points_won'] = infos[0]['pts1stservlostb'] / infos[0]['ptsplayed1stservb'] * 100
                    match_total['second_return_points_won'] = ((infos[0]['totservplayedb'] - infos[0]['ptsplayed1stservb']) - (infos[0]['ptstotwonservb'] - infos[0]['ptswon1stservb'])) / (infos[0]['totservplayedb'] - infos[0]['ptsplayed1stservb']) * 100
                    if infos[0]['breakptsplayeda'] != 0:
                        match_total['break_point_converted'] = infos[0]['breakptsconva'] / infos[0]['breakptsplayeda'] * 100
                    else:
                        match_total['break_point_converted'] = 0
                else:
                    match_total['key'] = str(id) + str(player_ids[index])
                    match_total['player_ids'] = player_ids[index]
                    match_total['sport_id'] = 3
                    match_total['match_id'] = id
                    match_total['aces'] = infos[0]['acesb']
                    match_total['double_faults'] = infos[0]['dblfltb']
                    match_total['service_points_win'] = (infos[0]['ptstotwonservb'] / infos[0]['totservplayedb']) * 100
                    match_total['first_serve'] = (infos[0]['ptsplayed1stservb'] / infos[0]['totservplayedb']) * 100
                    match_total['first_serve_win'] = (infos[0]['ptswon1stservb'] / infos[0]['ptsplayed1stservb']) * 100
                    match_total['second_serve_win'] = (infos[0]['ptstotwonservb'] - infos[0]['ptswon1stservb']) / (
                                infos[0]['totservplayedb'] - infos[0]['ptsplayed1stservb']) * 100
                    if infos[0]['breakptsplayeda'] != 0:
                        match_total['break_point_saved'] = infos[0]['breakptsconva'] / infos[0]['breakptsplayeda'] * 100
                    else:
                        match_total['break_point_saved'] = 0
                    match_total['service_games_win'] = infos[0]['ptstotwonservb'] / infos[0]['totservplayedb'] * 100
                    match_total['service_games_played'] = infos[0]['servgamesplayedb']
                    match_total['return_games_played'] = infos[0]['servgamesplayeda']
                    match_total['first_return_points_won'] = infos[0]['pts1stservlosta'] / infos[0][
                        'ptsplayed1stserva'] * 100
                    match_total['second_return_points_won'] = ((infos[0]['totservplayedb'] - infos[0]['ptsplayed1stservb']) - (infos[0]['ptstotwonservb'] - infos[0]['ptswon1stservb'])) / (infos[0]['totservplayedb'] - infos[0]['ptsplayed1stservb']) * 100
                    if infos[0]['breakptsplayedb'] != 0:
                        match_total['break_point_converted'] = infos[0]['breakptsconvb'] / infos[0]['breakptsplayedb'] * 100
                    else:
                        match_total['break_point_converted'] = 0
                TennisMatchTotalStat.upsert(
                    self.session,
                    'key',
                    match_total
                )
                print(match_total)



if __name__ == '__main__':
    GetMatchPlayerStat().get_match_info()



