import requests
from lxml import etree
import datetime, time
from datetime import date
from orm_connection.orm_session import MysqlSvr
from orm_connection.acb_basketball import BleagueAcbBasketballPlayer,BleagueAcbBasketballVenue


def tree_parse(res):
    enconding = requests.utils.get_encodings_from_content(res.text)
    html_doc = res.content.decode()
    tree = etree.HTML(html_doc)
    return tree


def change_match_bjtime(time_date):
    time_format = datetime.datetime.strptime(time_date, '%d/%m/%Y')
    timeArray = datetime.datetime.strftime(time_format, '%d/%m/%Y')
    timeArray1 = datetime.datetime.strptime(timeArray, '%d/%m/%Y')
    bj_time = (timeArray1 + datetime.timedelta()).strftime("%Y-%m-%d")
    bj_time1 = datetime.datetime.strptime(bj_time, '%Y-%m-%d')
    timeStamp = int(time.mktime(bj_time1.timetuple()))
    today = date.today()
    age = today.year - time_format.year - ((today.month, today.day) < (time_format.month, time_format.day))
    return timeStamp, age


def get_player_id():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueAcbBasketballPlayer).all()
    data_dict = {row.short_name_en: row.id for row in rows}
    return data_dict


def change_bjtime(date):
    time_format = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M')
    timeArray = datetime.datetime.strftime(time_format, '%d/%m/%Y %H:%M')
    timeArray1 = datetime.datetime.strptime(timeArray, '%d/%m/%Y %H:%M')
    bj_time = (timeArray1 + datetime.timedelta(hours=7)).strftime("%d/%m/%Y %H:%M")
    bj_time1 = datetime.datetime.strptime(bj_time, '%d/%m/%Y %H:%M')
    timeStamp = int(time.mktime(bj_time1.timetuple()))
    return timeStamp

def get_venue_id():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueAcbBasketballVenue).all()
    data_dict = {row.name_en: row.id for row in rows}
    return data_dict


a = ['1361366', '1361368', '1361365', '1361364', '1361378', '1361370', '1361377', '1361367', '1361369', '1361384', '1361382', '1361381', '1361385', '1361379', '1361393', '1361380', '1361383', '1361392', '1378264', '1378265', '1378259', '1378266', '1378263', '1378267', '1378261', '1378260', '1378262', '1384316', '1384315', '1384311', '1384313', '1384309', '1384310', '1384317', '1384307', '1384312', '1430073', '1430076', '1430069', '1430075', '1430077', '1430071', '1430074', '1430070', '1430072', '1435354', '1435358', '1435351', '1435356', '1435353', '1435360', '1435359', '1435352', '1435357', '1440178', '1440183', '1440181', '1440179', '1440182', '1440180', '1440176', '1440175', '1440177', '1446634', '1446633', '1446639', '1446632', '1446636', '1446638', '1446637', '1446631', '1446635', '1450729', '1450736', '1450732', '1450737', '1450733', '1450734', '1450731', '1450735', '1450730', '1454628', '1454621', '1454632', '1454634', '1454631', '1454627', '1454630', '1454619', '1454620', '1458344', '1458354', '1458342', '1458361', '1458362', '1458353', '1458355', '1458348', '1458343', '1458371', '1458387', '1458367', '1458384', '1458368', '1458388', '1458376', '1458375', '1458374', '1466206', '1466201', '1466204', '1466207', '1466208', '1466202', '1466205', '1466200', '1466203', '1469382', '1469387', '1469385', '1469386', '1469378', '1469380', '1469383', '1469379', '1469384', '1479566', '1479567', '1474340', '1479568', '1479565', '1479569', '1479564', '1474338', '1474339', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
