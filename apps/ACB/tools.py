import requests
from lxml import etree
import datetime,time

def tree_parse(res):
    enconding = requests.utils.get_encodings_from_content(res.text)
    html_doc = res.content.decode()
    tree = etree.HTML(html_doc)
    return tree

def change_match_bjtime(date):
    time_format = datetime.datetime.strptime(date, '%d/%m/%Y')
    timeArray = datetime.datetime.strftime(time_format, '%d/%m/%Y')
    timeArray1 = datetime.datetime.strptime(timeArray, '%d/%m/%Y')
    bj_time = (timeArray1 + datetime.timedelta()).strftime("%Y-%m-%d")
    bj_time1 = datetime.datetime.strptime(bj_time, '%Y-%m-%d')
    timeStamp = int(time.mktime(bj_time1.timetuple()))
    return timeStamp


a = '21/03/1985'
print(change_match_bjtime(a))