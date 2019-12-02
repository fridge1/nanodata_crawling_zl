import hashlib
import traceback
from qiniu import Auth, put_data, put_file
import os
from orm_connection.orm_session import MysqlSvr
from orm_connection.orm_tableStruct_basketball import *



QINIU_ACCESS_KEY = 'ga0b9GeWuBl6AfEaD6B51TO_BfCzq_T68-deEl--'
QINIU_SECRET_KEY = 'pltamVO3mzmtlcQyqm8UDm-nEqUZbCMNn229Spf1'


def player_logo():
    try:
        filePath = '/Users/zhulang/Desktop/nanodata_crawling/apps/NBL/nbl_player/'
        # for filePath in content_list:
        for fileName in os.listdir(filePath):
            key = fileName.split('.')[0]
            out_png_file = filePath + fileName
            with open(out_png_file, 'rb') as f:
                data = f.read()
            file_path = out_png_file
            q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
            bucket_name = 'spider-image'
            token = q.upload_token(bucket_name, None)
            m = hashlib.md5()
            m.update(data)
            psw = 'basketball/%s/%s.png' % ('nbl_player', m.hexdigest())
            ret, info = put_file(token, psw, file_path)
            logo = ret['key']
            data_team = {
             'id' : key,
             'logo' : logo.split('/')[-1],
            }
            spx_dev_session = MysqlSvr.get('spider_zl')
            BleagueNblBasketballPlayer.upsert(
                spx_dev_session,
                'id',
                data_team
            )
            print(data_team)
    except:
        print(traceback.format_exc())


if __name__ == '__main__':

    player_logo()