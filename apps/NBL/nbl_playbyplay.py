import requests
import json
from apps.NBL.tools import *
import time
import queue




headers = {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
url = 'https://www.fibalivestats.com/data/1307430/data.json'
pbp_res = requests.get(url,headers=headers)
pbp_dict = json.loads(pbp_res.text)
for pbp_info in pbp_dict['pbp']:
    if 'familyName' in pbp_info.keys():
        player_name = pbp_info['familyName'] + ' ' + pbp_info['firstName']
        if pbp_info['scoring'] != 0 :
            success_dict = {'1': 'made','0':'missed'}
            if pbp_info['tno'] != 0:
                team = pbp_dict['tm'][str(pbp_info['tno'])]['name']
                if int(pbp_info['lead']) > 0:
                    word_text = str(pbp_info['shirtNumber']) + ',' + player_name + ',' + pbp_info['actionType'] \
                                + ' '+pbp_info['subType'] + ' ' +team + ' - lead by ' + str(pbp_info['lead'])
                elif int(pbp_info['lead']) < 0:
                    word_text = str(pbp_info['shirtNumber']) + ',' + player_name + ',' + pbp_info['actionType'] \
                                + ' ' + pbp_info['subType'] + ' ' + team + ' - trail by ' + str(pbp_info['lead'])
                else:
                    word_text = str(pbp_info['shirtNumber']) + ',' + player_name + ',' + pbp_info['actionType'] \
                                + ' ' + pbp_info['subType'] + ' ' + team + ' - tie'
            else:
                word_text = pbp_info['shirtNumber'] +','+ player_name
        else:
            if 'jumpball' in pbp_info['actionType']:
                word_text = pbp_info['shirtNumber'] +','+ player_name + ','+pbp_info['actionType'] + ' - ' + pbp_info['subType']
            else:
                word_text = pbp_info['shirtNumber'] + ',' + player_name + ',' + pbp_info['subType']
    else:
        word_text = pbp_info['actionType'] + ' ' + pbp_info['subType']
    print(word_text)