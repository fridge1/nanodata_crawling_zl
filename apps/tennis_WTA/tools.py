from orm_connection.orm_session import MysqlSvr
from orm_connection.tennis import TennisPlayerInfoSingleRank,TennisPlayerInfoDoubleRank
import requests
from lxml import etree
import unicodedata


def get_en_name(data):
    return str(unicodedata.normalize('NFKD', data).encode('ascii', 'ignore'), encoding='utf-8')

def get_single_player_id():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(TennisPlayerInfoSingleRank).all()
    single_player_id_name = {}
    for row in rows:
        single_player_id_name[row.player_id] = '-'.join(row.name_en.lower().replace(' ','-').replace('í','-').replace('á','-').replace('é','-').split('-')).replace('--','-')
    return single_player_id_name


def get_double_player_id():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(TennisPlayerInfoDoubleRank).all()
    double_player_id_name = {}
    for row in rows:
        double_player_id_name[row.player_id] = '-'.join(row.name_en.lower().replace(' ','-').replace('í','-').replace('á','-').replace('é','-').split('-')).replace('--','-')
    return double_player_id_name

def tree_parse(res):
    enconding = requests.utils.get_encodings_from_content(res.text)
    html_doc = res.content.decode(enconding[0])
    tree = etree.HTML(html_doc)
    return tree