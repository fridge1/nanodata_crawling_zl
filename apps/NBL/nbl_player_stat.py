import requests
import json
import traceback
import threading
from apps.NBL.nbl_tools import translate
from apps.NBL.tools import *
import time
from apps.send_error_msg import dingding_alter
from common.libs.log import LogMgr
logger = LogMgr.get('nbl_basketball_pbp_box_live')


class pbp_box(object):
    def __init__(self):
        self.team_id_get = get_team_id()

    def pbp_box_live(self,data_queue,match_id,match_time):
        while True:
            headers = {
                        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
                    }
            url = 'https://www.fibalivestats.com/data/%s/data.json' % str(match_id)
            logger.info(url)
            pbp_res = requests.get(url,headers=headers)
            if int(match_time) >= int(time.time()) and pbp_res.status_code != 200:
                logger.info('比赛未开赛.... %s' % str(match_id))
                time.sleep(10)
            else:
                pbp_dict = json.loads(pbp_res.text)
                for pbp_info in pbp_dict['pbp']:
                    pass




    def get_match_id(self,data_queue):
        try:
            url = 'https://api.nbl.com.au/_/custom/api/genius?route=competitions/24346/matches&matchType=REGULAR&limit=200&fields=matchId,matchStatus,matchTimeUTC,competitors,roundNumber,venue,ticketURL&liveapidata=false&filter[owner]=nbl'
            headers = {
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            }
            res = requests.get(url,headers=headers)
            match_dict = json.loads(res.text)
            for id_time in match_dict['data']:
                match_id = id_time['matchId']
                match_time = change_bjtime(id_time['matchTimeUTC'])
                threading.Thread(target=pbp_box().pbp_box_live,args=(data_queue,match_id,match_time)).start()
        except:
            dingding_alter(traceback.format_exc())
            logger.error(traceback.format_exc())






