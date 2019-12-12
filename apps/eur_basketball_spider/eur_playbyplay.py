import requests
import traceback
from apps.send_error_msg import dingding_alter
import json
from apps.eur_basketball_spider.eur_tools import translate
import re
from apps.eur_basketball_spider.tools import *
import time
import queue
from common.libs.log import LogMgr

logger = LogMgr.get('eur_basketball_playbyplay_live')


class EurLeagueSpider_playbyplay(object):
    def __init__(self):
        self.data_queue = queue.Queue()
        self.headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
        self.get_player_id_key = get_player_id_key()


    def start_requests_2(self, data_queue, gamecode):
        headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
        while True:
            time.sleep(10)
            try:
                localtion_url = 'https://live.euroleague.net/api/Points?gamecode=%s&seasoncode=E2019&disp=' % str(
                    gamecode)
                localtion_json_res = requests.get(localtion_url, headers=self.headers)
                url = ' https://live.euroleague.net/api/PlayByPlay?gamecode=%s&seasoncode=E2019&disp=' % str(gamecode)
                logger.info(url)
                playbyplay_json_res = requests.get(url, headers=headers)
                if playbyplay_json_res.text == '':
                    logger.info('playbyplay比赛未开赛。。。 %s' % str(gamecode))
                else:
                    playbyplay_json_dict = json.loads(playbyplay_json_res.text)
                    localtion_json_dict = json.loads(localtion_json_res.text)
                    localtion_info_dict = {}
                    for row in localtion_json_dict['Rows']:
                        localtion_info_dict[row['NUM_ANOT']] = (row['COORD_X'], row['COORD_Y'], row['TEAM'])
                    key_list = []
                    for a in playbyplay_json_dict.keys():
                        key_list.append(a)
                    period = 1
                    point_A = 0
                    point_B = 0
                    playbyplay_list = []
                    home_team = playbyplay_json_dict['TeamA']
                    away_team = playbyplay_json_dict['TeamB']
                    for key in key_list[6:]:
                        if playbyplay_json_dict[key]:
                            for playbyplay_info in playbyplay_json_dict[key]:
                                playbyplay = {}
                                try:
                                    playbyplay['id'] = self.get_player_id_key[playbyplay_info['PLAYER_ID'][1:].strip()]
                                except:
                                    player_url = 'https://www.euroleague.net/competition/players/showplayer?pcode=%s&seasoncode=E2019' % str(
                                        playbyplay_info['PLAYER_ID'][1:].strip())
                                    player = {}
                                    player_res = requests.get(player_url, headers=headers)
                                    if player_res.status_code == 200:
                                        player_tree = tree_parse(player_res)
                                        player['sport_id'] = 2
                                        try:
                                            player['name_en'] = player_tree.xpath('//div[@class="name"]/text()')[0]
                                        except:
                                            player['name_en'] = ''
                                        player['key'] = re.findall(r'pcode=(.*?)&', player_url)[0]
                                        print(player['key'])
                                        try:
                                            player['logo'] = \
                                                player_tree.xpath('//div[@class="player_img-img"]/img/@src')[0]
                                        except:
                                            player['logo'] = ''
                                            print('没有该球员的图片...')
                                        try:
                                            player['shirt_number'] = \
                                                player_tree.xpath('//span[@class="dorsal"]/text()')[0]
                                        except:
                                            player['shirt_number'] = 0
                                        try:
                                            position = player_tree.xpath(
                                                '//div[@class="summary-first"]/span[last()]/span[last()]/text()')[0]
                                            player['position'] = position.encode('utf-8').decode('utf-8')[0]
                                        except:
                                            player['position'] = ''
                                        if 'Height' in \
                                                player_tree.xpath('//div[@class="summary-second"]/span[1]/text()')[
                                                    0].split(
                                                    ':')[0]:
                                            player['height'] = float(
                                                player_tree.xpath('//div[@class="summary-second"]/span[1]/text()')[
                                                    0].split(
                                                    ':')[-1]) * 100
                                            time_birthday = \
                                                player_tree.xpath('//div[@class="summary-second"]/span[2]/text()')[0]
                                            player['birthday'], player['age'] = time_stamp(time_birthday)
                                            player['nationality'] = \
                                                player_tree.xpath('//div[@class="summary-second"]/span[last()]/text()')[
                                                    0].split(':')[-1]
                                        else:
                                            player['height'] = 0
                                            time_birthday = \
                                                player_tree.xpath('//div[@class="summary-second"]/span[1]/text()')[0]
                                            player['birthday'], player['age'] = time_stamp(time_birthday)
                                            player['nationality'] = \
                                                player_tree.xpath('//div[@class="summary-second"]/span[last()]/text()')[
                                                    0].split(':')[-1]
                                        try:
                                            player['name_zh'] = translate_dict[player['name_en']]
                                        except:
                                            player['name_zh'] = ''
                                        print('player_img:', player)
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
                                        _, row = BleaguejpBasketballPlayer.upsert(
                                            spx_dev_session,
                                            'key',
                                            data
                                        )
                                        playbyplay['id'] = row.id
                                    else:
                                        playbyplay['id'] = 0
                                playbyplay['sport_id'] = 2
                                playbyplay['period'] = period
                                playbyplay['key'] = playbyplay_info['CODETEAM']
                                playbyplay['time_info'] = playbyplay_info['MARKERTIME']
                                if playbyplay_info['POINTS_A'] != None:
                                    playbyplay['POINTS_A'] = playbyplay_info['POINTS_A']
                                    point_A = playbyplay['POINTS_A']
                                else:
                                    playbyplay['POINTS_A'] = point_A
                                if playbyplay_info['POINTS_B'] != None:
                                    playbyplay['POINTS_B'] = playbyplay_info['POINTS_B']
                                    point_B = playbyplay['POINTS_B']
                                else:
                                    playbyplay['POINTS_B'] = point_B
                                playbyplay['score_info'] = str(playbyplay['POINTS_A']) + '-' + str(
                                    playbyplay['POINTS_B'])
                                if playbyplay_info['PLAYINFO'] and playbyplay_info['PLAYER']:
                                    name_zh = translate_player_name(playbyplay_info['PLAYER'])
                                    playbyplay['words_text'] = playbyplay_info['PLAYINFO']
                                    text = str(name_zh) + ' ' + str(translate(playbyplay['words_text']))
                                else:
                                    playbyplay['words_text'] = playbyplay_info['PLAYINFO']
                                    text = translate(playbyplay['words_text'])
                                if playbyplay_info['TEAM'] == home_team:
                                    belong = 1
                                elif playbyplay_info['TEAM'] == away_team:
                                    belong = 2
                                else:
                                    belong = 0
                                if '2FGM' in playbyplay_info['PLAYTYPE']:
                                    try:
                                        coordinate = localtion_info_dict[playbyplay_info['NUMBEROFPLAY']]
                                        if coordinate[2] in away_team:
                                            local_y = (coordinate[0] * (-416) / 1500 + 218) * 32 / 300
                                            local_x = (800 - ((coordinate[1] * 776 / 2800) + 56)) * 49 / 500
                                            if local_x > 49:
                                                local_x = local_x - 49
                                            else:
                                                local_x = local_x
                                            if local_y > 32:
                                                local_y = local_y - 32
                                            else:
                                                local_y = local_y
                                        else:
                                            local_y = 49 - (coordinate[0] * (416) / 1500 + 218) * 32 / 300
                                            local_x = ((coordinate[1] * 776 / 2800) + 56) * 49 / 500
                                        shooting_play = 1
                                        scoring_play = 1
                                        score_value = 2
                                    except:
                                        print('匹配动作。。。')
                                elif '2FGA' in playbyplay_info['PLAYTYPE']:
                                    try:
                                        coordinate = localtion_info_dict[playbyplay_info['NUMBEROFPLAY']]
                                        if coordinate[2] in away_team:
                                            local_y = (coordinate[0] * (-416) / 1500 + 218) * 32 / 300
                                            local_x = (800 - ((coordinate[1] * 776 / 2800) + 56)) * 49 / 500
                                            if local_x > 49:
                                                local_x = local_x - 49
                                            else:
                                                local_x = local_x
                                            if local_y > 32:
                                                local_y = local_y - 32
                                            else:
                                                local_y = local_y
                                        else:
                                            local_y = 49 - (coordinate[0] * (416) / 1500 + 218) * 32 / 300
                                            local_x = ((coordinate[1] * 776 / 2800) + 56) * 49 / 500
                                        shooting_play = 1
                                        scoring_play = 0
                                        score_value = 0
                                    except:
                                        print('匹配动作。。。')
                                elif '3FGM' in playbyplay_info['PLAYTYPE']:
                                    try:
                                        coordinate = localtion_info_dict[playbyplay_info['NUMBEROFPLAY']]
                                        if coordinate[2] in away_team:
                                            local_y = (coordinate[0] * (-416) / 1500 + 218) * 32 / 300
                                            local_x = (800 - ((coordinate[1] * 776 / 2800) + 56)) * 49 / 500
                                            if local_x > 49:
                                                local_x = local_x - 49
                                            else:
                                                local_x = local_x
                                            if local_y > 32:
                                                local_y = local_y - 32
                                            else:
                                                local_y = local_y
                                        else:
                                            local_y = 49 - (coordinate[0] * (416) / 1500 + 218) * 32 / 300
                                            local_x = ((coordinate[1] * 776 / 2800) + 56) * 49 / 500
                                        shooting_play = 1
                                        scoring_play = 1
                                        score_value = 3
                                    except:
                                        print('匹配动作。。。')
                                elif '3FGA' in playbyplay_info['PLAYTYPE']:
                                    try:
                                        coordinate = localtion_info_dict[playbyplay_info['NUMBEROFPLAY']]
                                        if coordinate[2] in away_team:
                                            local_y = (coordinate[0] * (-416) / 1500 + 218) * 32 / 300
                                            local_x = (800 - ((coordinate[1] * 776 / 2800) + 56)) * 49 / 500
                                            if local_x > 49:
                                                local_x = local_x - 49
                                            else:
                                                local_x = local_x
                                            if local_y > 32:
                                                local_y = local_y - 32
                                            else:
                                                local_y = local_y
                                        else:
                                            local_y = 49 - (coordinate[0] * (416) / 1500 + 218) * 32 / 300
                                            local_x = ((coordinate[1] * 776 / 2800) + 56) * 49 / 500
                                        shooting_play = 1
                                        scoring_play = 0
                                        score_value = 0
                                    except:
                                        print('匹配动作。。。')
                                elif 'FTA' in playbyplay_info['PLAYTYPE']:
                                    shooting_play = 1
                                    scoring_play = 0
                                    score_value = 0
                                    local_x = -1
                                    local_y = -1
                                elif 'FTM' in playbyplay_info['PLAYTYPE']:
                                    shooting_play = 1
                                    scoring_play = 1
                                    score_value = 1
                                    local_x = -1
                                    local_y = -1
                                elif 'LAYUPATT' in playbyplay_info['PLAYTYPE'] and 'Missed' not in \
                                        playbyplay['words_text']:
                                    shooting_play = 0
                                    scoring_play = 1
                                    score_value = 2
                                    local_x = -1
                                    local_y = -1
                                else:
                                    shooting_play = 0
                                    scoring_play = 0
                                    score_value = 0
                                    local_x = -1
                                    local_y = -1
                                if text == '比赛开始':
                                    playbyplay['time_info'] = '10:00'
                                elif text == '比赛结束' or text == '本节结束':
                                    playbyplay['time_info'] = '00:00'
                                data = {
                                    'id': int(str(13) + '0000') + int(gamecode),
                                    'type': 0,
                                    'home_score': playbyplay['POINTS_A'],
                                    'away_score': playbyplay['POINTS_B'],
                                    'belong': belong,
                                    'location_x': int(local_y),
                                    'location_y': int(local_x),
                                    'period': playbyplay['period'],
                                    'period_time': playbyplay['time_info'],
                                    'text': text,
                                    'shooting_play': shooting_play,
                                    'scoring_play': scoring_play,
                                    'score_value': score_value,
                                    'text_en': playbyplay['words_text'],
                                    'player_ids': [playbyplay['id']]
                                }
                                if playbyplay['words_text']:
                                    playbyplay_list.append(data)
                        period += 1
                    match_data_playbyplay = {'match': {'id': int(str(13) + '0000') + int(gamecode),
                                                       'basketball_items': {
                                                           'incident': {
                                                               'period': period,
                                                               'items': playbyplay_list}
                                                       }}}
                    data_queue.put(match_data_playbyplay)
                    logger.info('文字直播推送完成。。。 %s' % str(gamecode))
                    if playbyplay_list[-1]['text'] == '比赛结束':
                        break
            except:
                dingding_alter(traceback.format_exc())
                logger.error(traceback.format_exc())
                continue
