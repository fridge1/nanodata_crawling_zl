from orm_connection.orm_session import MysqlSvr
from orm_connection.kbl_basketball import BleagueNblBasketballStage,BleagueNblBasketballSeason


spx_dev_session = MysqlSvr.get('spider_zl')
years_list = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
id = 1
for year in years_list:
    sport_id = 2
    season = str(year)+'-'+str(year+1)
    season_id =spx_dev_session.query(BleagueNblBasketballSeason).filter(BleagueNblBasketballSeason.season == season).all()[0].id
    name_zh = season+'赛季'
    has_player_stats = 1
    has_team_stats = 1
    mode = 5
    data = {
        'id':int(id),
        'season_id':int(season_id),
        'sport_id':int(sport_id),
        'name_zh':str(name_zh),
        'mode':int(mode),
    }
    BleagueNblBasketballStage.upsert(
        spx_dev_session,
        'id',
        data
    )
    id += 1
