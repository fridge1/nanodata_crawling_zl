from apps.kbl.tools import *
import traceback
from apps.send_error_msg import dingding_alter
from common.libs.log import LogMgr
logger = LogMgr.get('kbl_basketball_match_live')


class match_info(object):
    def __init__(self):
        self.headers = {
            'user_agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.start_url = 'https://www.kbl.or.kr/main/main.asp'
        self.url = 'https://www.kbl.or.kr/main/main.asp?game_date=20191005'


    def get_match_info(self,url):
        match = {}
        res = requests.get(url, headers=self.headers)
        res_tree = tree_parse(res)
        match_urls = res_tree.xpath('//ul[@id="schedule_result"]/li/a/@href')
        for match_url in match_urls:
            match_res = requests.get(self.start_url+match_url,headers=self.headers)
            match_tree = tree_parse(match_res)
            match_info_url = match_tree.xpath('//div[@class="btn_wrap game_end"]/a/@href')[0]
            print(match_info_url)
            match_date = re.findall(r'tdate=(.*)', match_info_url)[0]
            match['season_id'] = re.findall(r'scode=(.*?)&',match_info_url)[0]
            match_time =match_tree.xpath('//li[@class="col on"]/a/div/span[@class="time"]/text()')[0]
            match['match_time'] = change_bjtime(match_date + match_time)
            game_number = re.findall(r'gno=(.*?)&',match_info_url)[0]
            match['id'] = int(str(match['season_id']) + '000') + int(game_number)
            match['sport_id'] = 2
            status_mark = match_tree.xpath('//li[@class="col on"]/a/div/em[@class="txt_g game_r"]/text()')[0]
            if status_mark == '종료':
                match['status_id'] = 10
                home_team_name = match_tree.xpath('//div[@class="team_block fl_l"]/strong/text()')[0]
                away_team_name = match_tree.xpath('//div[@class="team_block fl_r"]/strong/text()')[0]
                match['home_team_id'] = get_team_id(home_team_name)
                match['away_team_id'] = get_team_id(away_team_name)
                home_team_score_list = match_tree.xpath('//tbody[1]/tr[1]/td/text()')[1:7]
                away_team_score_list = match_tree.xpath('//tbody[1]/tr[2]/td/text()')[1:7]
                match['home_score'] = home_team_score_list[-1]
                match['away_score'] = away_team_score_list[-1]
                match['home_half_score'] = int(home_team_score_list[0]) + int(home_team_score_list[1])
                match['away_half_score'] = int(away_team_score_list[0]) + int(away_team_score_list[1])
                if '0' in home_team_score_list:
                    home_team_score_list.remove('0')
                    match['home_scores'] = str(list(map(int, home_team_score_list)))
                else:
                    match['home_scores'] = str(list(map(int, home_team_score_list)))
                if '0' in away_team_score_list:
                    away_team_score_list.remove('0')
                    match['away_scores'] = str(list(map(int, away_team_score_list)))
                else:
                    match['away_scores'] = str(list(map(int, away_team_score_list)))
                spx_dev_session = MysqlSvr.get('spider_zl')
                BleagueNblBasketballMatch.upsert(
                    spx_dev_session,
                    'id',
                    match
                )
                logger.info('已结束:',match)
            else:
                match['status_id'] =1
                home_team_name = match_tree.xpath('//div[@class="team_block fl_l"]/strong/text()')[0]
                away_team_name = match_tree.xpath('//div[@class="team_block fl_r"]/strong/text()')[0]
                match['home_team_id'] = get_team_id(home_team_name)
                match['away_team_id'] = get_team_id(away_team_name)
                match['home_score'] = 0
                match['away_score'] = 0
                match['home_half_score'] = 0
                match['away_half_score'] = 0
                match['home_scores'] = 0
                match['away_scores'] = 0
                spx_dev_session = MysqlSvr.get('spider_zl')
                BleagueNblBasketballMatch.upsert(
                    spx_dev_session,
                    'id',
                    match
                )
                logger.info('未开赛:',match)





    def get_date_url(self,url):
        try:
            res = requests.get(url,headers=self.headers)
            match_info().get_match_info(url)
            res_tree = tree_parse(res)
            next_url = res_tree.xpath('//span[@id="span_next_date"]/a/@href')[0]
            if 'game_date' in next_url:
                map_url = self.start_url + next_url
                match_info().get_match_info(map_url)
                match_info().get_date_url(map_url)
            else:
                print('赛季结束。。。')
        except:
            dingding_alter(traceback.format_exc())
            logger.error(traceback.format_exc())


