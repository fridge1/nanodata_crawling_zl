from apps.kbl.tools import *
import traceback
import re
from apps.send_error_msg import dingding_alter
from common.libs.log import LogMgr
logger = LogMgr.get('kbl_basketball_match_live')


class match_info(object):
    def __init__(self):
        self.headers = {
            'user_agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.start_url = 'https://www.kbl.or.kr/main/main.asp'


    def get_match_info(self,url):
        match = {}
        res = requests.get(url, headers=self.headers)
        res_tree = tree_parse(res)
        match_urls = res_tree.xpath('//tbody/tr')
        year = re.findall(r'CalDate=(.*?)&',url)[0].split('-')[0]
        count = 1
        for time_info in match_urls:
            game_time = time_info.xpath('./@class')[0].split('_')[-1]
            hours = time_info.xpath('./td[@class="time"]/text()')[0]
            match['match_time'] = change_match_bjtime(year+game_time+' '+hours)
            match['sport_id'] = 2
            match['key'] = year+game_time+str(count)
            count += 1
            try:
                match['status_id'] = 10
                match_info_url = time_info.xpath('./td[last()]/a[2]/@href')[0]
                match['season_id'] = re.findall(r'scode=(.*?)&', match_info_url)[0]
                infos = requests.get('https://www.kbl.or.kr/schedule/today/'+match_info_url,headers=self.headers)
                infos_tree = tree_parse(infos)
                home_logo = infos_tree.xpath('//div[@class="col col_left"]/div/img/@src')[0]
                print(home_logo)
                home_name = infos_tree.xpath('//div[@class="col col_left"]/strong[@class="team_name"]/text()')[0]
                match['home_team_id'] = get_team_id(home_name,home_logo)
                print(match['home_team_id'])
                away_logo = infos_tree.xpath('//div[@class="col col_right"]/div/img/@src')[0]
                print(away_logo)
                away_name = infos_tree.xpath('//div[@class="col col_right"]/strong[@class="team_name"]/text()')[0]
                match['away_team_id'] = get_team_id(away_logo, away_name)
                print(match['away_team_id'])
                home_scores = infos_tree.xpath('//tbody/tr[1]/td/text()')[1:]
                home_total = infos_tree.xpath('//span[@class="l"]/text()')[0]
                home_scores.append(home_total)
                if '0' in home_scores:
                    home_scores.remove('0')
                    match['home_scores'] = str(list(map(int,home_scores)))
                else:
                    match['home_scores'] = str(list(map(int,home_scores)))
                away_scores = infos_tree.xpath('//tbody/tr[2]/td/text()')[1:]
                away_total = infos_tree.xpath('//span[@class="w"]/text()')[0]
                away_scores.append(away_total)
                if '0' in away_scores:
                    away_scores.remove('0')
                    match['away_scores'] = str(list(map(int, away_scores)))
                else:
                    match['away_scores'] = str(list(map(int, away_scores)))
                match['home_score'] = home_total
                match['away_score'] = away_total
                match['home_half_score'] = int(home_scores[1]) + int(home_scores[0])
                match['away_half_score'] = int(away_scores[1]) + int(away_scores[0])
                spx_dev_session = MysqlSvr.get('spider_zl')
                BleagueNblBasketballMatch.upsert(
                    spx_dev_session,
                    'key',
                    match
                )
                spx_dev_session.close()
                logger.info('已结束match:', match)
            except:
                logger.info(traceback.format_exc())
                match['status_id'] = 1
                home_name = time_info.xpath('./td[@class="match"]/span[@class="home"]/text()')[0]
                away_name = time_info.xpath('./td[@class="match"]/span[@class="away"]/text()')[0]
                match['home_team_id'] = get_team_name_id(home_name)
                match['away_team_id'] = get_team_name_id(away_name)
                spx_dev_session = MysqlSvr.get('spider_zl')
                BleagueNblBasketballMatch.upsert(
                    spx_dev_session,
                    'key',
                    match
                )
                spx_dev_session.close()
                logger.info('未开赛match:',match)




    def get_date_url(self,url):
        try:
            res = requests.get(url,headers=self.headers)
            match_info().get_match_info(url)
            res_tree = tree_parse(res)
            next_url = res_tree.xpath('//a[@class="btn_date_arrow next"]/@href')[0]
            map_url = 'https://www.kbl.or.kr/schedule/today/' + next_url
            match_info().get_date_url(map_url)
        except:
            dingding_alter(traceback.format_exc())
            logger.error(traceback.format_exc())




    def run(self):
        while True:
            date = time.strftime('%Y%m%d', time.localtime(time.time()))
            url = 'https://www.kbl.or.kr/schedule/today/list.asp?tdate=%s&CalDate=1997-02-01&SchSeason=S1' % date
            match_info().get_date_url(url)
            time.sleep(7200)

