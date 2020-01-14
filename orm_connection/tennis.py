from sqlalchemy import Integer, Column, String, SmallInteger, TIMESTAMP, text, create_engine, Float
from orm_connection.orm_base import *
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'mysql+pymysql://spider_zl:0EDbIRtu4JPGdiQnu3kvXxiOMDMjejow@rm-bp1ov656aj80p2ie8uo.mysql.rds.aliyuncs.com/spider_zl')

prefix = 'wta_tennis_'


class TennisPlayer(BaseModel):
    __tablename__ = prefix + 'player'
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')
    manager_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='教练id')
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    short_name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文简称')
    short_name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文简称')
    short_name_zht = Column(String(255), nullable=False, server_default='', default='', comment='繁体简称')
    gender = Column(SmallInteger, nullable=False, server_default='1', default=1, comment='性别:0,未知 1,男 2,女')
    logo = Column(String(255), nullable=False, server_default='', default='', comment='logo')
    age = Column(Integer, nullable=False, server_default='0', default=0, comment='年龄')
    birthday = Column(Integer, nullable=False, server_default='0', default=0, comment='生日')
    weight = Column(Integer, nullable=False, server_default='0', default=0, comment='体重')
    height = Column(Integer, nullable=False, server_default='0', default=0, comment='身高')
    plays = Column(Integer, nullable=False, server_default='0', default=0, comment='擅长手 1左， 2右， 3双')
    city_id = Column(Integer, index=True, nullable=True, comment='出生地id')
    nationality = Column(String(50), nullable=False, server_default='', default='', comment='国籍')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisManager(BaseModel):
    __tablename__ = prefix + 'manager'
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')
    name_en = Column(String(50), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(50), nullable=False, server_default='', default='', comment='中文名称')
    short_name_en = Column(String(50), nullable=False, server_default='', default='', comment='英文简称')
    short_name_zh = Column(String(50), nullable=False, server_default='', default='', comment='中文简称')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisSeason(BaseModel):
    __tablename__ = prefix + 'season'
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    season = Column(String(20), nullable=False, server_default='', default='', comment='赛季格式2018、2018-2019')
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    has_player_stats = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否有球员统计')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisCompetition(BaseModel):
    __tablename__ = prefix + 'competition'
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    season_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='赛季id')
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    surface = Column(Integer, nullable=False, server_default='0', default=0,
                     comment='1硬地场，2红土场，3草地场，4泥土沙地场，5合成塑胶场，6地毯球场')
    level = Column(String(255), nullable=False, server_default='', default='', comment='赛事等级')
    start_time = Column(Integer, nullable=False, server_default='0', default=0, comment='赛事的开始时间')
    end_time = Column(Integer, nullable=False, server_default='0', default=0, comment='赛事的结束时间')
    city_id = Column(Integer, index=True, nullable=True, comment='城市id')
    inOutdoor = Column(Integer, index=True, nullable=True, comment='1室内，2室外')
    country_id = Column(Integer, index=True, nullable=True, comment='国家id')
    prizeMoney = Column(Integer, index=True, nullable=True, comment='赛事奖金')
    prizeMoneyCurrency = Column(Integer, index=True, nullable=True, comment='1美')
    singlesDrawSize = Column(Integer, index=True, nullable=True, comment='单打参赛人数')
    doublesDrawSize = Column(Integer, index=True, nullable=True, comment='双打参赛人数')
    has_player_stats = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否有球员统计')
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisCity(BaseModel):
    __tablename__ = prefix + 'city'
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(100), nullable=False, server_default='', default='', index=True)
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    country_id = Column(Integer, nullable=False, server_default='0', default=0, comment='国家id')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisReferee(BaseModel):
    __tablename__ = prefix + 'referee'
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(100), nullable=False, server_default='', default='', index=True)
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    logo = Column(String(255), nullable=False, server_default='', default='', comment='logo')
    age = Column(Integer, nullable=False, server_default='0', default=0, comment='年龄')
    birthday = Column(Integer, nullable=False, server_default='0', default=0, comment='生日')
    matchs = Column(Integer, nullable=False, server_default='0', default=0, comment='执法场次')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisPlayerInfoDoubleRank(BaseModel):
    __tablename__ = prefix + 'double_player_rank'
    id = Column(Integer, primary_key=True)
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    season_id = Column(Integer, index=True, nullable=False, comment='赛季id')
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    player_id = Column(Integer, index=True, nullable=False, comment='球员id')
    ranking = Column(Integer, nullable=False, comment='', default=0)
    points = Column(Integer, nullable=False, comment='', default=0)
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    stat_cycle = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='统计周期')
    promotion = Column(Integer, nullable=False, server_default='0', default=0, comment='升降名次')
    promotion_type = Column(Integer, nullable=False, server_default='0', default=0, comment='升降类型 0为不变，1为升，2为降')
    scope_date = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='统计时间')
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisPlayerInfoSingleRank(BaseModel):
    __tablename__ = prefix + 'single_player_rank'
    id = Column(Integer, primary_key=True)  # id
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    season_id = Column(Integer, index=True, nullable=False, comment='赛季id')
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    player_id = Column(Integer, index=True, nullable=False, comment='球员id')
    ranking = Column(Integer, nullable=False, comment='', default=0)
    points = Column(Integer, nullable=False, comment='', default=0)
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    stat_cycle = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='统计周期')
    promotion = Column(Integer, nullable=False, server_default='0', default=0, comment='升降名次')
    promotion_type = Column(Integer, nullable=False, server_default='0', default=0, comment='升降类型 0为不变，1为升，2为降')
    scope_date = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='统计时间')
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisCountry(BaseModel):
    __tablename__ = prefix + 'country'
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(100), nullable=False, server_default='', default='', index=True)
    name_en = Column(String(50), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(50), nullable=False, server_default='', default='', comment='中文名称')
    name_zht = Column(String(50), nullable=False, server_default='', default='', comment='繁体名称')
    logo = Column(String(50), nullable=False, server_default='', default='', comment='')
    deleted = Column(Integer, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisPlayerCareer(BaseModel):
    __tablename__ = prefix + 'player_career'
    id = Column(Integer, primary_key=True)  # id
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    single_titles = Column(Integer, nullable=False, server_default='0', default=0, comment='单打获得冠军的次数')
    double_titles = Column(Integer, nullable=False, server_default='0', default=0, comment='双打获得冠军的次数')
    double_high = Column(Integer, nullable=False, server_default='0', default=0, comment='双打获得最高名次')
    single_win = Column(Integer, nullable=False, server_default='0', default=0, comment='单打所赢次数')
    double_win = Column(Integer, nullable=False, server_default='0', default=0, comment='双打所赢次数')
    single_lost = Column(Integer, nullable=False, server_default='0', default=0, comment='单打所输次数')
    double_lost = Column(Integer, nullable=False, server_default='0', default=0, comment='双打打所输次数')
    single_high = Column(Integer, nullable=False, server_default='0', default=0, comment='单打获得最高名次')
    prize_money = Column(Integer, nullable=False, server_default='0', default=0, comment='生涯所获奖金')
    player_id = Column(Integer, index=True, nullable=False, comment='球员id')
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisChampionship(BaseModel):
    __tablename__ = prefix + 'championship'
    id = Column(Integer, primary_key=True)
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    season_id = Column(Integer, index=True, nullable=False, comment='赛季id')
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    competition_id = Column(Integer, nullable=False, server_default='0', default=0, comment='赛事id')
    player_id = Column(Integer, index=True, nullable=False, comment='球员id')
    type = Column(Integer, index=True, nullable=False, comment='单双打类型 1单打，2双打')


class TennisSinglePlayerStatBySeason(BaseModel):
    __tablename__ = prefix + 'single_player_season_stat'
    id = Column(Integer, primary_key=True)
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    season_id = Column(Integer, index=True, nullable=False, comment='赛季id')
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    player_id = Column(Integer, index=True, nullable=False, comment='球员id')
    aces = Column(Integer, index=True, nullable=False, comment='一发对方未接住')
    double_faults = Column(Integer, index=True, nullable=False, comment='双发失误')
    service_points_win = Column(Float, index=True, nullable=False, comment='总发球得分率')
    first_serve = Column(Float, index=True, nullable=False, comment='一发成功率')
    first_serve_win = Column(Float, index=True, nullable=False, comment='一发得分率')
    second_serve_win = Column(Float, index=True, nullable=False, comment='二发得分率')
    break_point_saved = Column(Float, index=True, nullable=False, comment='挽救破发点成功率')
    service_games_win = Column(Float, index=True, nullable=False, comment='发球局胜率')
    service_games_played = Column(Integer, index=True, nullable=False, comment='总发球局数')
    first_return_points_won = Column(Float, index=True, nullable=False, comment='接一发获胜率/一发回球获胜率')
    second_return_points_won = Column(Float, index=True, nullable=False, comment='接二发获胜率/二发回球获胜率')
    break_point_converted = Column(Float, index=True, nullable=False, comment='把握破发点成功率')
    break_points_lost = Column(Integer, index=True, nullable=False, comment='')
    return_games_win = Column(Float, index=True, nullable=False, comment='接发球局数胜率')
    return_games_played = Column(Integer, index=True, nullable=False, comment='接发球局数')
    break_points_faced = Column(Integer, index=True, nullable=False, comment='')
    break_points_opportunities = Column(Integer, index=True, nullable=False, comment='破发机会')
    return_points_win = Column(Float, index=True, nullable=False, comment='接发球得分率')
    total_points_win = Column(Integer, index=True, nullable=False, comment='总得分')
    match_count = Column(Integer, index=True, nullable=False, comment='赛季参加的场数')
    surface = Column(Integer, nullable=False, server_default='0', default=0,
                     comment='1硬地场，2红土场，3草地场，4泥土沙地场，5合成塑胶场，6地毯球场')
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisSinglePlayerCareer(BaseModel):
    __tablename__ = prefix + 'single_player_career_stat'
    id = Column(Integer, primary_key=True)
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    season_id = Column(Integer, index=True, nullable=False, comment='赛季id')
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    player_id = Column(Integer, index=True, nullable=False, comment='球员id')
    aces = Column(Integer, index=True, nullable=False, comment='一发对方未接住')
    double_faults = Column(Integer, index=True, nullable=False, comment='双发失误')
    service_points_win = Column(Float, index=True, nullable=False, comment='总发球得分率')
    first_serve = Column(Float, index=True, nullable=False, comment='一发成功率')
    first_serve_win = Column(Float, index=True, nullable=False, comment='一发得分率')
    second_serve_win = Column(Float, index=True, nullable=False, comment='二发得分率')
    break_point_saved = Column(Float, index=True, nullable=False, comment='挽救破发点成功率')
    service_games_win = Column(Float, index=True, nullable=False, comment='发球局胜率')
    service_games_played = Column(Integer, index=True, nullable=False, comment='总发球局数')
    first_return_points_won = Column(Float, index=True, nullable=False, comment='接一发获胜率/一发回球获胜率')
    second_return_points_won = Column(Float, index=True, nullable=False, comment='接二发获胜率/二发回球获胜率')
    break_point_converted = Column(Float, index=True, nullable=False, comment='把握破发点成功率')
    break_points_lost = Column(Integer, index=True, nullable=False, comment='')
    return_games_win = Column(Float, index=True, nullable=False, comment='接发球局数胜率')
    return_games_played = Column(Integer, index=True, nullable=False, comment='接发球局数')
    break_points_faced = Column(Integer, index=True, nullable=False, comment='')
    break_points_opportunities = Column(Integer, index=True, nullable=False, comment='破发机会')
    return_points_win = Column(Float, index=True, nullable=False, comment='接发球得分率')
    total_points_win = Column(Integer, index=True, nullable=False, comment='总得分')
    match_count = Column(Integer, index=True, nullable=False, comment='生涯参加的场数')
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisMatch(BaseModel):
    __tablename__ = prefix + 'match'
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')
    competition_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='赛事id')
    season_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='赛季id')
    home_team_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='主队id')
    away_team_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='客队id')
    first_serve = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='发球方')
    match_time = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='比赛时间')
    status_id = Column(Integer, nullable=False, server_default='0', default=0, comment='状态id')
    round_num = Column(Integer, nullable=False, server_default='0', default=0, comment='第几轮')
    group_num = Column(Integer, nullable=False, server_default='0', default=0, comment='第几组')
    home_score = Column(Integer, nullable=False, server_default='0', default=0, comment='主队比分')
    away_score = Column(Integer, nullable=False, server_default='0', default=0, comment='客队比分')
    home_player_id = Column(String(255), nullable=False, server_default='', default='', comment='主队球员id')
    away_player_id = Column(String(255), nullable=False, server_default='', default='', comment='主队球员id')
    home_player_score = Column(String(255), nullable=False, server_default='', default='', comment='主队球员比分')
    away_player_score = Column(String(255), nullable=False, server_default='', default='', comment='客队球员比分')
    type = Column(Integer, nullable=False, server_default='0', default=0, comment='单打1，双打2，混双3')
    elimination_type = Column(Integer, nullable=False, server_default='0', default=0,
                              comment='1 64进32，2 32进16，3 16进8，4 8进4，5 4进2，6 决赛')
    surface = Column(Integer, nullable=False, server_default='0', default=0,
                     comment='1硬地场，2红土场，3草地场，4泥土沙地场，5合成塑胶场，6地毯球场')
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))



class TennisMatchPlayerStat(BaseModel):
    __tablename__ = prefix + 'match_player_stat'
    id = Column(Integer, primary_key=True)
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    match_id = Column(Integer, index=True, nullable=False, comment='比赛id')
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    player_ids = Column(String(255), nullable=False, server_default='', default='', comment='球员ids')
    aces = Column(Integer, index=True, nullable=False, comment='一发对方未接住')
    double_faults = Column(Integer, index=True, nullable=False, comment='双发失误')
    service_points_win = Column(Float, index=True, nullable=False, comment='总发球得分率')
    first_serve = Column(Float, index=True, nullable=False, comment='一发成功率')
    first_serve_win = Column(Float, index=True, nullable=False, comment='一发得分率')
    second_serve_win = Column(Float, index=True, nullable=False, comment='二发得分率')
    break_point_saved = Column(Float, index=True, nullable=False, comment='挽救破发点成功率')
    service_games_win = Column(Float, index=True, nullable=False, comment='发球局胜率')
    service_games_played = Column(Integer, index=True, nullable=False, comment='总发球局数')
    first_return_points_won = Column(Float, index=True, nullable=False, comment='接一发获胜率/一发回球获胜率')
    second_return_points_won = Column(Float, index=True, nullable=False, comment='接二发获胜率/二发回球获胜率')
    break_point_converted = Column(Float, index=True, nullable=False, comment='把握破发点成功率')
    break_points_lost = Column(Integer, index=True, nullable=False, comment='')
    return_games_win = Column(Float, index=True, nullable=False, comment='接发球局数胜率')
    return_games_played = Column(Integer, index=True, nullable=False, comment='接发球局数')
    break_points_faced = Column(Integer, index=True, nullable=False, comment='')
    break_points_opportunities = Column(Integer, index=True, nullable=False, comment='破发机会')
    return_points_win = Column(Float, index=True, nullable=False, comment='接发球得分率')
    total_points_win = Column(Integer, index=True, nullable=False, comment='总得分')
    set_num = Column(Integer, index=True, nullable=False, comment='1第一盘，2第二盘，3第三盘，4第四盘，5第五盘')
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisMatchTotalStat(BaseModel):
    __tablename__ = prefix + 'match_total_stat'
    id = Column(Integer, primary_key=True)
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    match_id = Column(Integer, index=True, nullable=False, comment='比赛id')
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    player_ids = Column(String(255), nullable=False, server_default='', default='', comment='球员ids')
    aces = Column(Integer, index=True, nullable=False, comment='一发对方未接住')
    double_faults = Column(Integer, index=True, nullable=False, comment='双发失误')
    service_points_win = Column(Float, index=True, nullable=False, comment='总发球得分率')
    first_serve = Column(Float, index=True, nullable=False, comment='一发成功率')
    first_serve_win = Column(Float, index=True, nullable=False, comment='一发得分率')
    second_serve_win = Column(Float, index=True, nullable=False, comment='二发得分率')
    break_point_saved = Column(Float, index=True, nullable=False, comment='挽救破发点成功率')
    service_games_win = Column(Float, index=True, nullable=False, comment='发球局胜率')
    service_games_played = Column(Integer, index=True, nullable=False, comment='总发球局数')
    first_return_points_won = Column(Float, index=True, nullable=False, comment='接一发获胜率/一发回球获胜率')
    second_return_points_won = Column(Float, index=True, nullable=False, comment='接二发获胜率/二发回球获胜率')
    break_point_converted = Column(Float, index=True, nullable=False, comment='把握破发点成功率')
    break_points_lost = Column(Integer, index=True, nullable=False, comment='')
    return_games_win = Column(Float, index=True, nullable=False, comment='接发球局数胜率')
    return_games_played = Column(Integer, index=True, nullable=False, comment='接发球局数')
    break_points_faced = Column(Integer, index=True, nullable=False, comment='')
    break_points_opportunities = Column(Integer, index=True, nullable=False, comment='破发机会')
    return_points_win = Column(Float, index=True, nullable=False, comment='接发球得分率')
    total_points_win = Column(Integer, index=True, nullable=False, comment='总得分')
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

BaseModel.metadata.create_all(engine)
