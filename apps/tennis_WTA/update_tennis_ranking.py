import io
from apps.tennis_WTA.tools import competition_time_stamp
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
        {'name': 'backhand', 'type': ["int", "null"]},
        {'name': 'residence', 'type': ["int", "null"]},
        {'name': 'prize_current', 'type': ["int", "null"]},
        {'name': 'prize_total', 'type': ["int", "null"]},
    ]
}
parsed_schema = parse_schema(ranking_schema)


def single_rank_update():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(TennisPlayerInfoSingleRank).all()
    records = []
    for row in rows:
        pub_time = competition_time_stamp(row.key[:10])
        info_dict = {}
        info_dict['player_id'] = row.player_id
        info_dict['ranking'] = row.ranking
        info_dict['points'] = row.points
        info_dict['position_changed'] = row.promotion
        info_dict['pub_time'] = pub_time
        info_dict['type'] = 1
        records.append(info_dict)
    return records


def double_rank_update():
    session = MysqlSvr.get('spider_zl')
    rows = session.query(TennisPlayerInfoDoubleRank).all()
    records = []
    for row in rows:
        pub_time = competition_time_stamp(row.key[:10])
        info_dict = {}
        info_dict['player_id'] = row.player_id
        info_dict['ranking'] = row.ranking
        info_dict['points'] = row.points
        info_dict['position_changed'] = row.promotion
        info_dict['pub_time'] = pub_time
        info_dict['type'] = 2
        records.append(info_dict)
    return records


def send_single_data():
    records = single_rank_update()
    buffer = io.BytesIO()
    fastavro.writer(buffer, ranking_schema, records)
    ranking_data = buffer.getvalue()
    return ranking_data


def send_double_data():
    records = double_rank_update()
    buffer = io.BytesIO()
    fastavro.writer(buffer, ranking_schema, records)
    ranking_data = buffer.getvalue()
    return ranking_data
