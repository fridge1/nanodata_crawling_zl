from apps.eur_basketball_spider.eur_playbyplay import *
import queue
import traceback
from apps.send_error_msg import dingding_alter
from apps.eur_basketball_spider.tools import *
from orm_connection.eur_basketball import *
from orm_connection.orm_session import MysqlSvr
from common.libs.log import LogMgr

logger = LogMgr.get('eur_basketball_boxscore_live')


class EurLeagueSpider_boxscore(object):
    def __init__(self):
        self.data_queue_svr = queue.Queue()
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
        self.get_team_id = get_team_id_box()
        self.get_player_id = get_player_id_key()
        self.get_player_shirt_number = get_player_shirt_number()

    def start_requests(self, data_queue, gamecode):
        while True:
            time.sleep(10)
            try:
                seasoncode = 2019
                url = 'https://live.euroleague.net/api/Boxscore?gamecode=%s&seasoncode=E%s&disp=' % (
                gamecode, seasoncode)
                logger.info(url)
                boxscore_api_res = requests.get(url, headers=self.headers)
                if boxscore_api_res.text == '':
                    logger.info('box比赛未开赛。。。 %s' % str(gamecode))
                else:
                    boxscore_json_dict = json.loads(boxscore_api_res.text)
                    boxscore_player = boxscore_json_dict['Stats']
                    team_stats_list = []
                    player_stats_list = []
                    belong = 1
                    for index in boxscore_player:
                        BkMatchTeamStats = {}
                        BkMatchTeamStats['belong'] = belong
                        name_en = index['Team']
                        BkMatchTeamStats['team_id'] = self.get_team_id[name_en.lower()]
                        BkMatchTeamStats['team_name'] = name_en
                        BkMatchTeamStats['three_point_goals'] = safe_get(index,'totr.FieldGoalsMade3')
                        BkMatchTeamStats['three_point_field'] = safe_get(index,'totr.three_point_field')
                        BkMatchTeamStats['goals'] = safe_get(index,'totr.FieldGoalsMade2') + BkMatchTeamStats['three_point_goals']
                        BkMatchTeamStats['field'] = safe_get(index,'totr.FieldGoalsAttempted2') + BkMatchTeamStats['three_point_field']
                        BkMatchTeamStats['free_throw_goals'] = safe_get(index,'totr.FreeThrowsMade')
                        BkMatchTeamStats['free_throw_field'] = safe_get(index,'totr.FreeThrowsAttempted')
                        BkMatchTeamStats['offensive_rebounds'] = safe_get(index,'totr.OffensiveRebounds')
                        BkMatchTeamStats['defensive_rebounds'] = safe_get(index,'totr.DefensiveRebounds')
                        BkMatchTeamStats['rebounds'] = safe_get(index,'totr.TotalRebounds')
                        BkMatchTeamStats['assists'] = safe_get(index,'totr.Assistances')
                        BkMatchTeamStats['steals'] = safe_get(index,'totr.Steals')
                        BkMatchTeamStats['blocks'] = safe_get(index,'totr.BlocksFavour')
                        BkMatchTeamStats['turnovers'] = safe_get(index,'totr.Turnovers')
                        BkMatchTeamStats['personal_fouls'] = safe_get(index,'totr.FoulsCommited')
                        BkMatchTeamStats['point'] = safe_get(index,'totr.Points')
                        BkMatchTeamStats['score_difference'] = safe_get(index,'totr.Valuation')
                        team_stats_list.append(BkMatchTeamStats)
                        belong += 1
                    for i in range(2):
                        for home_player in boxscore_json_dict['Stats'][i]['PlayersStats']:
                            player = {}
                            player['belong'] = i + 1
                            player['player_name'] = translate_player_name(home_player['Player'])
                            player_key = home_player['Player_ID'][1:]
                            id = safe_get(self.get_player_id,player_key.strip())
                            if id == 0:
                                url = 'https://www.euroleague.net/competition/players/showplayer?pcode=%s&seasoncode=E2019' % player_key
                                player_res = requests.get(url, headers=self.headers)
                                player_tree = tree_parse(player_res)
                                player['sport_id'] = 2
                                try:
                                    player['name_en'] = player_tree.xpath('//div[@class="name"]/text()')[0]
                                except:
                                    player['name_en'] = ''
                                player['key'] = player_key
                                try:
                                    player['logo'] = player_tree.xpath('//div[@class="player_img-img"]/img/@src')[0]
                                except:
                                    player['logo'] = ''
                                    logger.info('没有该球员的图片...')
                                try:
                                    player['shirt_number'] = player_tree.xpath('//span[@class="dorsal"]/text()')[0]
                                except:
                                    player['shirt_number'] = 0
                                try:
                                    position = \
                                        player_tree.xpath(
                                            '//div[@class="summary-first"]/span[last()]/span[last()]/text()')[
                                            0]
                                    player['position'] = position.encode('utf-8').decode('utf-8')[0]
                                except:
                                    player['position'] = ''
                                if 'Height' in \
                                        player_tree.xpath('//div[@class="summary-second"]/span[1]/text()')[0].split(
                                            ':')[0]:
                                    player['height'] = float(
                                        player_tree.xpath('//div[@class="summary-second"]/span[1]/text()')[0].split(
                                            ':')[-1]) * 100
                                    time_birthday = player_tree.xpath('//div[@class="summary-second"]/span[2]/text()')[
                                        0]
                                    player['birthday'], player['age'] = time_stamp(time_birthday)
                                    player['nationality'] = \
                                        player_tree.xpath('//div[@class="summary-second"]/span[last()]/text()')[
                                            0].split(
                                            ':')[-1]
                                else:
                                    player['height'] = 0
                                    time_birthday = player_tree.xpath('//div[@class="summary-second"]/span[1]/text()')[
                                        0]
                                    player['birthday'], player['age'] = time_stamp(time_birthday)
                                    player['nationality'] = \
                                        player_tree.xpath('//div[@class="summary-second"]/span[last()]/text()')[
                                            0].split(':')[-1]
                                try:
                                    player['name_zh'] = translate_dict[player['name_en']]
                                except:
                                    player['name_zh'] = ''
                                data = {
                                    'key': player['key'],
                                    'name_en': player['name_en'],
                                    'name_zh': player['name_zh'],
                                    'sport_id': player['sport_id'],
                                    'age': player['age'],
                                    'birthday': player['birthday'],
                                    'nationality': player['nationality'],
                                    'height': player['height'],
                                    'shirt_number': player['shirt_number'],
                                    'position': player['position'],
                                }
                                spx_dev_session = MysqlSvr.get('spider_zl')
                                BleagueEurBasketballPlayer.upsert(
                                    spx_dev_session,
                                    'key',
                                    data
                                )
                            player['player_id'] = self.get_player_id[player_key.strip()]
                            player['shirt_number'] = self.get_player_shirt_number[player_key.strip()]
                            times = home_player['Minutes']
                            if times != 'DNP':
                                player['enter_ground'] = 1
                                minutes = times.split(':')[0]
                                seconds = times.split(':')[-1]
                                if int(seconds) >= 30:
                                    player['minutes'] = int(minutes) + 1
                                else:
                                    player['minutes'] = int(minutes)
                            else:
                                player['enter_ground'] = 0
                                player['minutes'] = 0
                            player['two_points_goals'] = home_player['FieldGoalsMade2']
                            player['two_points_goals'] = safe_get(home_player,'FieldGoalsMade2')
                            player['two_points_total'] = safe_get(home_player,'FieldGoalsAttempted2')
                            player['three_point_goals'] = safe_get(home_player,'FieldGoalsMade3')
                            player['three_point_field'] = safe_get(home_player,'FieldGoalsAttempted3')
                            player['goals'] = int(player['two_points_goals']) + int(player['three_point_goals'])
                            player['field'] = int(player['two_points_total']) + int(player['three_point_field'])
                            player['free_throw_goals'] = safe_get(home_player,'FreeThrowsMade')
                            player['free_throw_field'] = safe_get(home_player,'FreeThrowsAttempted')
                            player['offensive_rebounds'] = safe_get(home_player,'OffensiveRebounds')
                            player['defensive_rebounds'] = safe_get(home_player,'DefensiveRebounds')
                            player['rebounds'] = safe_get(home_player,'TotalRebounds')
                            player['assists'] = safe_get(home_player,'Assistances')
                            player['steals'] = safe_get(home_player,'Steals')
                            player['blocks'] = safe_get(home_player,'BlocksFavour')
                            player['turnovers'] = safe_get(home_player,'Turnovers')
                            player['personal_fouls'] = safe_get(home_player,'FoulsCommited')
                            player['score_difference'] = safe_get(home_player,'Valuation')
                            player['point'] = safe_get(home_player,'Points')
                            player['first_publish'] = safe_get(home_player,'IsStarter')
                            first = safe_get(home_player,'IsPlaying')
                            if first == 1:
                                player['on_ground'] = 0
                            elif first == 0:
                                player['on_ground'] = 1
                            else:
                                player['on_ground'] = 0
                            player_data = {
                                'belong': int(player['belong']),
                                'player_id': int(player['player_id']),
                                'player_name': player['player_name'],
                                'minutes': int(player['minutes']),
                                'goals': int(player['goals']),
                                'field': int(player['field']),
                                'three_point_goals': int(player['three_point_goals']),
                                'three_point_field': int(player['three_point_field']),
                                'free_throw_goals': int(player['free_throw_goals']),
                                'free_throw_field': int(player['free_throw_field']),
                                'offensive_rebounds': int(player['offensive_rebounds']),
                                'defensive_rebounds': int(player['defensive_rebounds']),
                                'rebounds': int(player['rebounds']),
                                'assists': int(player['assists']),
                                'steals': int(player['steals']),
                                'blocks': int(player['blocks']),
                                'turnovers': int(player['turnovers']),
                                'personal_fouls': int(player['personal_fouls']),
                                'score_difference': int(player['score_difference']),
                                'point': int(player['point']),
                                'first_publish': int(player['first_publish']),
                                'enter_ground': int(player['enter_ground']),
                                'on_ground': int(player['on_ground']),
                                'shirt_number': int(player['shirt_number']),
                            }
                            player_stats_list.append(player_data)
                    match_id = int(str(13) + '0000') + int(gamecode)
                    match_data_boxscore = {'match': {'id': int(match_id),
                                                     'basketball_items': {
                                                         'player_stat': {
                                                             'items': player_stats_list},
                                                         'team_stat': {'items': team_stats_list}
                                                     }}}
                    if player_stats_list:
                        data_queue.put(match_data_boxscore)
                        logger.info('球员技术统计推送完成。。。 %s' % str(gamecode))
                        minutes_team = boxscore_json_dict['Stats'][0]['totr']['Minutes']
                        if minutes_team == '225:00' or minutes_team == '200:00':
                            break
            except:
                dingding_alter(traceback.format_exc())
                logger.error(traceback.format_exc())
                continue
