from sqlalchemy import Integer, Column, String, SmallInteger, TIMESTAMP, text, Text, create_engine
from orm_connection.orm_base import *
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://spider_zl:0EDbIRtu4JPGdiQnu3kvXxiOMDMjejow@rm-bp1ov656aj80p2ie8uo.mysql.rds.aliyuncs.com/spider_zl')


prefix = 'wta_tennis_'


# 球员表
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
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否删除')
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


class TennisMatch(BaseModel):
    __tablename__ = prefix + 'match'
    id = Column(Integer, primary_key=True, comment='id')
    open_id = Column(Integer, nullable=False, server_default='0', default=0, comment='雷速关联字段')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')
    competition_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='赛事id')
    season_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='赛季id')
    referee_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='裁判id')
    match_time = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='比赛时间')
    status_id = Column(Integer, nullable=False, server_default='0', default=0, comment='状态id 1未开赛，10比赛结束')
    match_num = Column(Integer, nullable=False, server_default='0', default=0, comment='第几场')
    player_id_home = Column(Integer, nullable=False, server_default='0', default=0, comment='参赛球员id')
    player_id_away = Column(Integer, nullable=False, server_default='0', default=0, comment='参赛球员id')
    home_scores = Column(String(255), nullable=False, default='', comment='主队详细比分')
    away_scores = Column(String(255), nullable=False, default='', comment='客队详细比分')
    type = Column(Integer, nullable=False, server_default='0', default=0, comment='单打1，双打2，混双3')
    elimination_type = Column(Integer, nullable=False, server_default='0', default=0, comment='1 64进32，2 32进16，3 16进8，4 8进4，5 4进2，6 决赛')
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
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
    start_time = Column(Integer, nullable=False, server_default='0', default=0, comment='赛事的开始时间')
    end_time = Column(Integer, nullable=False, server_default='0', default=0, comment='赛事的结束时间')
    city_id = Column(Integer, index=True, nullable=True, comment='城市id')
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
    updated_at = Column(TIMESTAMP, index=True, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TennisPlayerSingleRank(BaseModel):
    __tablename__ = prefix + 'single_rank'
    id = Column(Integer, primary_key=True)  # id
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    season_id = Column(Integer, index=True, nullable=False, comment='赛季id')
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    player_id = Column(Integer, index=True, nullable=False, comment='球员id')
    ranking = Column(Integer, nullable=False, comment='', default=0)
    points = Column(Integer, nullable=False, comment='', default=0)
    stat_cycle = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='统计周期')
    promotion = Column(Integer, nullable=False, server_default='0', default=0, comment='升降名次')
    promotion_type = Column(Integer, nullable=False, server_default='0', default=0, comment='升降类型 0为不变，1为升，2为降')
    scope_date = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='统计时间')
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class TennisPlayerDoubleRank(BaseModel):
    __tablename__ = prefix + 'double_rank'
    id = Column(Integer, primary_key=True)  # id
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    season_id = Column(Integer, index=True, nullable=False, comment='赛季id')
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    player_id = Column(Integer, index=True, nullable=False, comment='球员id')
    ranking = Column(Integer, nullable=False, comment='', default=0)
    points = Column(Integer, nullable=False, comment='', default=0)
    stat_cycle = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='统计周期')
    promotion = Column(Integer, nullable=False, server_default='0', default=0, comment='升降名次')
    promotion_type = Column(Integer, nullable=False, server_default='0', default=0, comment='升降类型 0为不变，1为升，2为降')
    scope_date = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='统计时间')
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class TennisPlayerInfoDoubleRank(BaseModel):
    __tablename__ = prefix + 'double_player_rank'
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



BaseModel.metadata.create_all(engine)