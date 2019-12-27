import hashlib
import traceback
from qiniu import Auth, put_data, put_file
import os
from orm_connection.orm_session import MysqlSvr
from orm_connection.acb_basketball import BleagueAcbBasketballPlayer
import io
from PIL import Image
import requests



QINIU_ACCESS_KEY = 'ga0b9GeWuBl6AfEaD6B51TO_BfCzq_T68-deEl--'
QINIU_SECRET_KEY = 'pltamVO3mzmtlcQyqm8UDm-nEqUZbCMNn229Spf1'


def download_img():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(BleagueAcbBasketballPlayer).all()
    data_dict = {row.id: row.logo for row in rows}
    for key,value in data_dict.items():
        try:
            res = requests.get(value)
            byte_stream = io.BytesIO(res.content)
            roiImg = Image.open(byte_stream)
            imgByteArr = io.BytesIO()
            roiImg.save(imgByteArr, format='PNG')
            imgByteArr = imgByteArr.getvalue()
            with open('/Users/zhulang/Desktop/player/' + str(key) + ".png", "wb") as f:
                f.write(imgByteArr)
        except:
            print('链接请求不到。。。')
            print(value)


def player_logo():
    try:
        filePath = '/Users/zhulang/Desktop/player/'
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
            psw = 'basketball/%s/%s.png' % ('player', m.hexdigest())
            ret, info = put_file(token, psw, file_path)
            logo = ret['key']
            data_team = {
             'id' : key,
             'logo' : logo.split('/')[-1],
            }
            spx_dev_session = MysqlSvr.get('spider_zl')
            BleagueAcbBasketballPlayer.upsert(
                spx_dev_session,
                'id',
                data_team
            )
            print(data_team)
    except:
        print(traceback.format_exc())


if __name__ == '__main__':
    # download_img()
    player_logo()