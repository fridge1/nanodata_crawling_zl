import requests
import json
from apps.NBL.tools import *
import traceback
from apps.send_error_msg import dingding_alter
from common.libs.log import LogMgr
logger = LogMgr.get('nbl_basketball_venue')



def venue_info():
    headers = {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
                }
    competitionId_list = [2254,9224,21029,18527,24346]
    for competitionId in competitionId_list:
        match_url = 'https://api.nbl.com.au/_/custom/api/genius?route=competitions/%s/matches&matchType=REGULAR&limit=200&fields=matchId,matchStatus,matchTimeUTC,competitors,roundNumber,venue,ticketURL&liveapidata=false&filter[owner]=nbl' % (
                        competitionId)
        res = requests.get(match_url,headers=headers)
        venue_dict = json.loads(res.text)
        for venue_info in venue_dict['data']:
            venue_id = venue_info['venue']['venueId']
            venue_name = venue_info['venue']['venueName']
            sport_id = 2
            stadium_id = venue_info['venue']['venueId']
            country = venue_info['venue']['venueNameInternational']
            data = {
                'id': venue_id,
                'name_en': venue_name,
                'stadium_id': stadium_id,
                'country': country,
                'sport_id': sport_id
            }
            spx_dev_session = MysqlSvr.get('spider_zl')
            BleagueNblBasketballVenue.upsert(
                spx_dev_session,
                'id',
                data
            )


