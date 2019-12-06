from orm_connection.orm_session import MysqlSvr
from orm_connection.kbl_basketball import BleagueNblBasketballSeason


spx_dev_session = MysqlSvr.get('spider_zl')
years_list = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
id = 1
for year in years_list:
    sport_id = 2
    season = str(year)+'-'+str(year+1)
    name_zh = season+'赛季'
    has_player_stats = 1
    has_team_stats = 1
    data = {
        'id':int(id),
        'season':str(season),
        'sport_id':int(sport_id),
        'name_zh':str(name_zh),
        'has_player_stats':int(has_player_stats),
        'has_team_stats':int(has_team_stats),
    }
    BleagueNblBasketballSeason.upsert(
        spx_dev_session,
        'id',
        data
    )
    id += 1
