import io
from apps.tennis_WTA.tools import competition_time_stamp,get_last_week_date
from orm_connection.orm_session import MysqlSvr
from orm_connection.tennis import TennisPlayerInfoDoubleRank, TennisPlayerInfoSingleRank, TennisPlayer
import fastavro
from fastavro import parse_schema

ranking_schema = {
    'name': 'tennis.ranking',
    'type': 'record',
    'fields': [
        {'name': 'player_id', 'type': 'int'},
        {'name': 'ranking', 'type': 'int'},
        {'name': 'points', 'type': 'int'},
        {'name': 'previous_points', 'type': ["int", "null"]},
        {'name': 'position_changed', 'type': ["int", "null"]},
        {'name': 'pub_time', 'type': ["int", "null"]},
        {'name': 'type', 'type': ["int", "null"]},
        {'name': 'competitions', 'type': ["int", "null"]},
    ]
}
player_schema = {
    'name': 'tennis.player',
    'type': 'record',
    'fields': [
        {'name': 'id', 'type': 'int'},
        {'name': 'name', 'type': 'string'},
        {'name': 'logo', 'type': 'string'},
        {'name': 'birthday', 'type': 'int'},
        {'name': 'weight', 'type': ["int", "null"]},
        {'name': 'height', 'type': ["int", "null"]},
        {'name': 'birthplace', 'type': ["string", "null"]},
        {'name': 'country_id', 'type': ["int", "null"]},
        {'name': 'plays', 'type': ["int", "null"]},
        {'name': 'prize_current', 'type': ["int", "null"]},
        {'name': 'prize_total', 'type': ["int", "null"]},
    ]
}



def single_rank_update():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(TennisPlayerInfoSingleRank).all()
    key_points = {}
    for row in rows:
        key_points[row.key] = row.points
    records = []
    for row in rows:
        pub_time = competition_time_stamp(row.key[:10])
        info_dict = {}
        info_dict['player_id'] = row.player_id
        info_dict['ranking'] = row.ranking
        info_dict['points'] = row.points
        info_dict['position_changed'] = row.promotion
        last_week = get_last_week_date(row.key[:10])
        key = str(last_week) + str(row.player_id)
        try:
            info_dict['previous_points'] = key_points[key]
        except:
            info_dict['previous_points'] = 0
        info_dict['pub_time'] = pub_time
        info_dict['type'] = 2
        records.append(info_dict)
    return records


def double_rank_update():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(TennisPlayerInfoDoubleRank).all()
    key_points = {}
    for row in rows:
        key_points[row.key] = row.points
    records = []
    for row in rows:
        pub_time = competition_time_stamp(row.key[:10])
        info_dict = {}
        info_dict['player_id'] = row.player_id
        info_dict['ranking'] = row.ranking
        info_dict['points'] = row.points
        info_dict['position_changed'] = row.promotion
        last_week = get_last_week_date(row.key[:10])
        key = str(last_week)+str(row.player_id)
        try:
            info_dict['previous_points'] = key_points[key]
        except:
            info_dict['previous_points'] = 0
        info_dict['pub_time'] = pub_time
        info_dict['type'] = 2
        records.append(info_dict)
    return records


def send_single_data():
    parsed_schema = parse_schema(ranking_schema)
    records = single_rank_update()
    buffer = io.BytesIO()
    fastavro.writer(buffer, ranking_schema, records)
    ranking_data = buffer.getvalue()
    return ranking_data


def send_double_data():
    parsed_schema = parse_schema(ranking_schema)
    records = double_rank_update()
    buffer = io.BytesIO()
    fastavro.writer(buffer, ranking_schema, records)
    ranking_data = buffer.getvalue()
    return ranking_data


def player_info_update():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(TennisPlayer).all()
    records = []
    for row in rows:
        pub_time = competition_time_stamp(row.key[:10])
        info_dict = {}
        info_dict['id'] = row.id
        info_dict['name'] = row.name_en
        info_dict['birthday'] = row.birthday
        info_dict['weight'] = row.weight
        info_dict['height'] = row.height
        info_dict['country_id'] = 1
        info_dict['plays'] = row.plays
        info_dict['prize_total'] = row.height
        info_dict['height'] = row.height
        records.append(info_dict)
    return records
