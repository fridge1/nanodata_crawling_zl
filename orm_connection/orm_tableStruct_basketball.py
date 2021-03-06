from sqlalchemy import Integer, Column, String, SmallInteger, TIMESTAMP, text, Text, create_engine
from orm_connection.orm_base import *
from sqlalchemy.orm import sessionmaker


# engine = create_engine('mysql+pymysql://spider_zl:0EDbIRtu4JPGdiQnu3kvXxiOMDMjejow@rm-bp1ov656aj80p2ie8uo.mysql.rds.aliyuncs.com/spider_zl')


prefix = 'nbl_league_basketball_'


# 球队表  ----2019现阶段b1 b2的36支球队已存
class BleagueNblBasketballTeam(BaseModel):
    __tablename__ = prefix + 'team'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')  # 球队id
    key = Column(String(25), nullable=False, server_default='', default='', index=True)  # 球队id的str
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')
    venue_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='场馆id')  # 需要在场馆表插入数据
    manager_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='教练id')
    competition_id = Column(Integer, index=True, nullable=False, server_default='0', default=0,
                            comment='联赛id')  # b1或者b2
    country_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='国家id')

    city_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='城市id')  # 所在城市的id   新增
    # 1 东  2-中 3-西

    conference_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='分区1,2,3,东，西，中')

    # conference_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='分区d,东西中')

    # 字段
    # conference = Column(String(25), nullable=False, server_default='', default='', comment='所在分区')      #所在分区，    新增

    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')  # 英文全称
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    name_zht = Column(String(255), nullable=False, server_default='', default='', comment='繁体名称')
    short_name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文简称')  # 英文简称
    short_name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文简称')
    short_name_zht = Column(String(255), nullable=False, server_default='', default='', comment='繁体简称')

    virtual = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否虚拟球队')
    national = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否国家队')
    logo = Column(String(255), nullable=False, server_default='', default='', comment='logo')  # 球队logo
    country_logo = Column(String(255), nullable=False, server_default='', default='', comment='国家logo')
    gender = Column(SmallInteger, nullable=False, server_default='1', default=1, comment='性别:0,未知 1,男 2,女')

    # 通用字段
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否删除')
    open_id = Column(Integer, nullable=False, server_default='0', default=0, comment='雷速关联字段')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 球员表  -----2019所有b1b2的球队的现役球员已存
class BleagueNblBasketballPlayer(BaseModel):
    __tablename__ = prefix + 'player'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')  # 球员id
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')
    team_id = Column(Integer, index=True, nullable=True, comment='球队id')

    # 字段
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    name_j = Column(String(255), nullable=False, server_default='', default='', comment='日文名称')
    short_name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文简称')
    short_name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文简称')
    short_name_zht = Column(String(255), nullable=False, server_default='', default='', comment='繁体简称')

    logo = Column(String(255), nullable=False, server_default='', default='', comment='logo')
    age = Column(Integer, nullable=False, server_default='0', default=0, comment='年龄')
    birthday = Column(Integer, nullable=False, server_default='0', default=0, comment='生日')
    weight = Column(Integer, nullable=False, server_default='0', default=0, comment='体重')
    height = Column(Integer, nullable=False, server_default='0', default=0, comment='身高')

    league_career_age = Column(Integer, nullable=False, server_default='0', default=0, comment='联盟球龄')
    school = Column(String(150), nullable=False, server_default='', default='', comment='毕业学院')
    school_id = Column(Integer, index=True, nullable=True, default=0, comment='毕业学院id')
    salary = Column(Integer, nullable=False, server_default='0', default=0, comment='年薪')
    contract_until = Column(Integer, nullable=False, server_default='0', default=0, comment='合同到期')
    shirt_number = Column(Integer, nullable=False, server_default='0', default=0, comment='球衣号')
    city = Column(String(50), nullable=False, server_default='', default='', comment='出生地')
    city_id = Column(Integer, index=True, nullable=True, comment='出生地id')
    nationality = Column(String(50), nullable=False, server_default='', default='', comment='国籍')
    position = Column(String(5), nullable=False, server_default='', default='', comment='位置')
    detailed_positions = Column(String(255), nullable=False, server_default='', default='', comment='详细位置')
    drafted = Column(Text, nullable=True, default='', comment='选秀信息')

    # 通用字段
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 教练表
class BleagueNblBasketballManager(BaseModel):
    __tablename__ = prefix + 'manager'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')
    team_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='执教球队')

    # 字段
    name_en = Column(String(50), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(50), nullable=False, server_default='', default='', comment='中文名称')
    name_j = Column(String(50), nullable=False, server_default='', default='', comment='繁体名称')
    short_name_en = Column(String(50), nullable=False, server_default='', default='', comment='英文简称')
    short_name_zh = Column(String(50), nullable=False, server_default='', default='', comment='中文简称')
    short_name_zht = Column(String(50), nullable=False, server_default='', default='', comment='繁体简称')

    logo = Column(String(255), nullable=False, server_default='', default='', comment='logo')
    age = Column(Integer, nullable=False, server_default='0', default=0, comment='年龄')
    birthday = Column(Integer, nullable=False, server_default='0', default=0, comment='生日')
    nationality = Column(String(50), nullable=False, server_default='', default='', comment='国籍')
    trainer_licence = Column(String(50), nullable=False, server_default='', default='', comment='教练执照')
    preferred_formation = Column(String(50), nullable=False, server_default='', default='', comment='习惯的阵型')

    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 场馆表  ----- 已存   城市表和场馆表的key都是字符串类型   也就是城市名和场馆名字
class BleagueNblBasketballVenue(BaseModel):
    __tablename__ = prefix + 'venue'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(100), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    stadium_id = Column(Integer, nullable=False, server_default='0', default=0, comment='体育场馆id')
    country_id = Column(Integer, nullable=False, server_default='0', default=0, comment='国家id')

    # 字段
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    name_zht = Column(String(255), nullable=False, server_default='', default='', comment='繁体名称')

    capacity = Column(Integer, nullable=False, server_default='0', default=0, comment='容量')
    city = Column(String(255), nullable=False, server_default='', default='', comment='城市')
    city_zh = Column(String(255), nullable=False, server_default='', default='', comment='城市中文翻译')
    country = Column(String(255), nullable=False, server_default='', default='', comment='国家')

    # 通用字段
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 城市表  -----已存
class BleagueNblBasketballCity(BaseModel):
    __tablename__ = prefix + 'city'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(100), nullable=False, server_default='', default='', index=True)
    # 字段
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')

    # 通用字段
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 毕业院校 ----- 已存
class BleagueNblBasketballSchool(BaseModel):
    __tablename__ = prefix + 'school'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(100), nullable=False, server_default='', default='', index=True)
    # 字段
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')

    # 通用字段
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 赛事
class BleagueNblBasketballCompetition(BaseModel):
    __tablename__ = prefix + 'competition'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    category_id = Column(Integer, nullable=False, server_default='0', default=0, comment='分类id')
    country_id = Column(Integer, nullable=False, server_default='0', default=0, comment='国家id')

    # 字段
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    name_zht = Column(String(255), nullable=False, server_default='', default='', comment='繁体名称')
    short_name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文简称')
    short_name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文简称')
    short_name_zht = Column(String(255), nullable=False, server_default='', default='', comment='繁体简称')

    type = Column(Integer, nullable=False, server_default='0', default=0, comment='赛事类型 1联赛 2杯赛')
    period = Column(Integer, nullable=False, server_default='45', default=45, comment='单阶段时间')
    period_count = Column(Integer, nullable=False, server_default='2', default=2, comment='总阶段')
    cur_season = Column(String(20), nullable=False, server_default='', default='', comment='当前赛季')
    cur_season_id = Column(Integer, nullable=False, server_default='2', default=0, comment='当前赛季id')  # 年份
    cur_stage_id = Column(Integer, nullable=False, server_default='2', default=0, comment='当前阶段id')
    cur_round = Column(Integer, nullable=False, server_default='2', default=0, comment='当前轮次')
    round_count = Column(Integer, nullable=False, server_default='2', default=0, comment='总轮次')

    logo = Column(String(255), nullable=False, server_default='', default='', comment='logo')
    level = Column(Integer, index=True, nullable=True, server_default='0', default=0, comment='level')
    has_stats = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否有资料库')

    # 通用字段
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 赛季
class BleagueNblBasketballSeason(BaseModel):
    __tablename__ = prefix + 'season'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, nullable=False, server_default='0', default=0, comment='球类id')
    competition_id = Column(Integer, nullable=False, server_default='0', default=0, comment='联赛id')

    # 字段
    season = Column(String(20), nullable=False, server_default='', default='', comment='赛季格式2018、2018-20192')
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    name_zht = Column(String(255), nullable=False, server_default='', default='', comment='繁体名称')

    has_player_stats = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否有球员统计')
    has_team_stats = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否有球队统计')

    # 通用字段
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 比赛阶段
class BleagueNblBasketballStage(BaseModel):
    __tablename__ = prefix + 'stage'
    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')
    season_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='赛季id')
    # 字段
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    name_zht = Column(String(255), nullable=False, server_default='', default='', comment='繁体名称')
    order = Column(Integer, nullable=False, server_default='0', default=0, comment='顺序')
    mode = Column(Integer, nullable=False, server_default='0', default=0, comment='比赛方式 1-积分赛 2-淘汰赛 3-资格赛 4-季前赛 5-常规赛')
    group_count = Column(Integer, nullable=False, server_default='0', default=0, comment='总分组')
    round_count = Column(Integer, nullable=False, server_default='0', default=0, comment='总轮数')
    has_table = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否有积分榜')
    is_top = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否顶级阶段')
    # 通用字段
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True)  # 是否删除
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 比赛表      -------有些球队已经不在b1  b2了  信息不完整
class BleagueNblBasketballMatch(BaseModel):
    __tablename__ = prefix + 'match'
    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')  # 比赛id
    key = Column(String(25), nullable=False, server_default='', default='', index=True)  # id的字符串格式
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')  # 2
    competition_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='赛事id')  # 1，2
    season_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='赛季id')  # 赛季id
    stage_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='阶段id')
    home_team_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='主队id')  # 客队id
    away_team_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='客队id')  # 主队id
    venue_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='场馆id')  # 场馆表
    referee_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='裁判id')
    # 字段
    match_time = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='比赛时间')  # 日期加时间
    status_id = Column(Integer, nullable=False, server_default='0', default=0, comment='状态id')
    round_num = Column(Integer, nullable=False, server_default='0', default=0, comment='第几轮')  # 轮次  第几轮
    group_num = Column(Integer, nullable=False, server_default='0', default=0, comment='第几组')
    neutral = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否中立场')
    home_score = Column(Integer, nullable=False, server_default='0', default=0, comment='主队比分')  # 主队总分
    away_score = Column(Integer, nullable=False, server_default='0', default=0, comment='客队比分')  # 客队总分
    home_half_score = Column(Integer, nullable=False, server_default='0', default=0, comment='主队半场比分')  # 下一个界面
    away_half_score = Column(Integer, nullable=False, server_default='0', default=0, comment='客队半场比分')  # 下一个
    home_scores = Column(String(255), nullable=False, default='', comment='主队详细比分')  # 包含每节比分存列表下一个
    away_scores = Column(String(255), nullable=False, default='', comment='客队详细比分')  # 包含每节比分下一个
    # 通用字段
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    open_id = Column(Integer, nullable=False, server_default='0', default=0, comment='雷速关联字段')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 球队阵容
class BleagueNblBasketballTeamLineup(BaseModel):
    __tablename__ = prefix + 'team_lineup'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')
    season_id = Column(Integer, index=True, nullable=True, server_default='0', default=0, comment='赛季id,可以存储历史赛季阵容')
    team_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球队id')
    player_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球员id')

    # 字段
    # C中锋 SF小前锋 PF大前锋 SG得分后卫 PG组织后卫 F前锋 G后卫
    position = Column(String(5), nullable=False, server_default='', default='', comment='位置')
    shirt_number = Column(String(5), nullable=False, server_default='', default='', comment='球衣号')
    is_captain = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否队长')
    order = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='顺序')

    # 通用字段
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, index=True, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 单场阵容信息
class BleagueNblBasketballLineupInfo(BaseModel):
    __tablename__ = prefix + 'match_lineup_info'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')
    match_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='比赛id')
    home_team_id = Column(Integer, index=True, nullable=True, comment='主队球队id')
    away_team_id = Column(Integer, index=True, nullable=True, comment='客队球队id')
    home_manager_id = Column(Integer, index=True, nullable=True, comment='主队教练id')
    away_manager_id = Column(Integer, index=True, nullable=True, comment='客队教练id')

    # 字段
    confirmed = Column(Integer, nullable=True, comment='阵容是否已经确认')
    home_formation = Column(String(10), nullable=False, server_default='', default='', comment='主队阵型')
    away_formation = Column(String(10), nullable=False, server_default='', default='', comment='客队阵型')
    home_team_rating = Column(Integer, nullable=True, default=0, comment='主队评分')
    away_team_rating = Column(Integer, nullable=True, default=0, comment='客队评分')

    # 通用字段
    updated_at = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='更新时间')


# 积分榜升降级
class BleagueNblBasketballPromotion(BaseModel):
    __tablename__ = prefix + 'promotion'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(100), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')

    # 字段
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    name_zht = Column(String(255), nullable=False, server_default='', default='', comment='繁体名称')
    color = Column(String(255), nullable=False, server_default='', default='', comment='颜色')

    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 积分榜
class BleagueNblBasketballTable(BaseModel):
    __tablename__ = prefix + 'table'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')
    season_id = Column(Integer, index=True, nullable=True, server_default='0', default=0, comment='赛季id')
    stage_id = Column(Integer, index=True, nullable=True, server_default='0', default=0, comment='阶段id')

    # 字段
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    name_zht = Column(String(255), nullable=False, server_default='', default='', comment='繁体名称')
    # group = Column(Integer, nullable=True, server_default='0', default=0, comment='分组')
    conference = Column(String(255), nullable=False, server_default='', default='', comment='分区名称')

    scope = Column(Integer, default=0, comment='统计范围 1-赛季 2-预选赛 3-小组赛 4-季前赛 5-常规赛 6-淘汰赛(季后赛)')
    order = Column(Integer, nullable=True, server_default='0', default=0, comment='排序')

    # 通用字段
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 积分榜详细数据
class BleagueNblBasketballTableRow(BaseModel):
    __tablename__ = prefix + 'table_row'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')
    season_id = Column(Integer, index=True, nullable=True, server_default='0', default=0, comment='赛季id')
    team_id = Column(Integer, index=True, nullable=True, server_default='0', default=0, comment='球队id')
    table_id = Column(Integer, index=True, nullable=True, server_default='0', default=0, comment='积分榜id')
    promotion_id = Column(Integer, index=True, nullable=True, server_default='0', default=0, comment='升降级id')

    position = Column(Integer, nullable=False, server_default='0', default=0, comment='排名')
    order = Column(Integer, nullable=True, server_default='0', default=0, comment='排序,手动排名')
    is_live = Column(Integer, nullable=True, server_default='0', default=0, comment='是否实时')

    detail = Column(Text, nullable=True, default='', comment='详细数据')

    # 东西部积分榜
    # won-胜
    # lost-负
    # won_rate-胜率
    # game_back-胜场差
    # home-主场
    # away-客场
    # division-赛区
    # conference-东(西)部
    # points_avg-场均得分
    # points_against_avg-场均失分
    # diff_avg-场均净胜
    # streaks-近期战绩
    # last_10-近10场

    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 单场比赛球队统计        --------第三页   已存
class BleagueNblBasketballTeamStats(BaseModel):
    __tablename__ = prefix + 'match_team_stat'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')  # 球类id   2
    match_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='比赛id')  # 单场比赛的id
    team_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球队id')  #  球队id

    # 字段
    period = Column(Integer, default=0, comment='比赛阶段')

    two_pointers_scored = Column(Integer, nullable=True, default=0, comment='两分球')  # 2分球命中数
    two_pointers_total = Column(Integer, nullable=True, default=0, comment='两分球总数')  # 2分球出手数
    two_pointers_accuracy = Column(String(10), nullable=True, default=0, comment='两分球命中率')  # 2分球命中率
    three_pointers_scored = Column(Integer, nullable=True, default=0, comment='三分球')  # 3分球命中数
    three_pointers_total = Column(Integer, nullable=True, default=0, comment='三分球总数')  # 3分球出手数
    three_pointers_accuracy = Column(String(10), nullable=True, default=0, comment='三分球命中率')  # 3分球命中率
    field_goals_scored = Column(Integer, nullable=True, default=0, comment='投篮')  # 投篮数
    field_goals_total = Column(Integer, nullable=True, default=0, comment='投篮总数')
    field_goals_accuracy = Column(String(10), nullable=True, default=0, comment='投篮命中率')
    free_throws_scored = Column(Integer, nullable=True, default=0, comment='罚球')
    free_throws_total = Column(Integer, nullable=True, default=0, comment='罚球总数')
    free_throws_accuracy = Column(String(10), nullable=True, default=0, comment='罚球命中率')

    total_fouls = Column(Integer, nullable=True, default=0, comment='犯规')
    timeouts = Column(Integer, nullable=True, default=0, comment='暂停')

    ball_possession = Column(Integer, nullable=True, default=0, comment='控球')
    rebounds = Column(Integer, nullable=True, default=0, comment='篮板')
    defensive_rebounds = Column(Integer, nullable=True, default=0, comment='防守篮板')
    offensive_rebounds = Column(Integer, nullable=True, default=0, comment='进攻篮板')
    assists = Column(Integer, nullable=True, default=0, comment='助攻')
    turnovers = Column(Integer, nullable=True, default=0, comment='失误')
    steals = Column(Integer, nullable=True, default=0, comment='抢断')
    blocks = Column(Integer, nullable=True, default=0, comment='盖帽')
    max_points_in_arow = Column(Integer, nullable=True, default=0, comment='最多连续得分')
    time_spent_in_lead = Column(Integer, nullable=True, default=0, comment='领先时间')
    lead_changes = Column(Integer, nullable=True, default=0, comment='领先变化')
    biggest_lead = Column(Integer, nullable=True, default=0, comment='最大领先优势')
    successful_attempts = Column(Integer, nullable=True, default=0, comment='出手命中')

    streaks = Column(Integer, nullable=True, default=0, comment='连胜(败)次数')

    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 单场比赛球员统计       -------第三页内容  核心
class BleagueNblBasketballPlayerStats(BaseModel):
    __tablename__ = prefix + 'match_player_stat'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')                #team_id+player_id
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')
    match_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='比赛id')
    team_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球队id')
    player_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球员id')

    # 字段
    period = Column(Integer, default=0, comment='比赛阶段')

    first = Column(Integer, nullable=True, default=0, comment='首发')   #0表示首发,  1表示不是  2
    minutes_played = Column(Integer, nullable=True, default=0, comment='出场时间')
    position = Column(String(5), nullable=False, server_default='', default='', comment='位置')

    # 总结
    points = Column(Integer, nullable=True, default=0, comment='得分')
    free_throws_scored = Column(Integer, nullable=True, default=0, comment='罚球命中数')
    free_throws_total = Column(Integer, nullable=True, default=0, comment='罚球总数')
    free_throws_accuracy = Column(String(10), nullable=True, default='', comment='罚球命中率')
    two_points_scored = Column(Integer, nullable=True, default=0, comment='两分球命中数')
    two_points_total = Column(Integer, nullable=True, default=0, comment='两分球总数')
    two_points_accuracy = Column(String(10), nullable=True, default=0, comment='两分球命中率')
    three_points_scored = Column(Integer, nullable=True, default=0, comment='三分球命中数')
    three_points_total = Column(Integer, nullable=True, default=0, comment='三分球总数')
    three_points_accuracy = Column(String(10), nullable=True, default=0, comment='三分球命中率')
    field_goals_scored = Column(Integer, nullable=True, default=0, comment='投篮命中数')
    field_goals_total = Column(Integer, nullable=True, default=0, comment='投篮总数')
    field_goals_accuracy = Column(String(10), nullable=True, default=0, comment='投篮命中率')

    # 篮板
    rebounds = Column(Integer, nullable=True, default=0, comment='篮板')
    defensive_rebounds = Column(Integer, nullable=True, default=0, comment='防守篮板')
    offensive_rebounds = Column(Integer, nullable=True, default=0, comment='进攻篮板')

    # 其他
    assists = Column(Integer, nullable=True, default=0, comment='助攻')
    turnovers = Column(Integer, nullable=True, default=0, comment='失误')
    steals = Column(Integer, nullable=True, default=0, comment='抢断')
    blocks = Column(Integer, nullable=True, default=0, comment='盖帽')
    personal_fouls = Column(Integer, nullable=True, default=0, comment='个人犯规')
    plus_minus = Column(Integer, nullable=True, default=0, comment='+/-')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 球队榜统计
class BleagueNblBasketballTeamTotal(BaseModel):
    __tablename__ = prefix + 'team_total'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, index=True, comment='key')
    sport_id = Column(Integer, index=True, nullable=False, comment='球类id')
    season_id = Column(Integer, index=True, nullable=False, comment='赛季id')
    team_id = Column(Integer, index=True, nullable=False, comment='球队id')

    # 字段
    scope = Column(Integer, default=0, comment='统计范围 1-赛季 2-预选赛 3-小组赛 4-季前赛 5-常规赛 6-淘汰赛(季后赛)')
    period = Column(Integer, default=0, comment='比赛阶段')
    matches = Column(Integer, default=0, comment='比赛场次')

    points = Column(Integer, nullable=True, default=0, comment='得分')

    two_pointers_scored = Column(Integer, nullable=True, default=0, comment='两分球')
    two_pointers_total = Column(Integer, nullable=True, default=0, comment='两分球总数')
    two_pointers_accuracy = Column(String(10), nullable=True, default=0, comment='两分球命中率')
    three_pointers_scored = Column(Integer, nullable=True, default=0, comment='三分球')
    three_pointers_total = Column(Integer, nullable=True, default=0, comment='三分球总数')
    three_pointers_accuracy = Column(String(10), nullable=True, default=0, comment='三分球命中率')
    field_goals_scored = Column(Integer, nullable=True, default=0, comment='投篮')
    field_goals_total = Column(Integer, nullable=True, default=0, comment='投篮总数')
    field_goals_accuracy = Column(String(10), nullable=True, default=0, comment='投篮命中率')
    free_throws_scored = Column(Integer, nullable=True, default=0, comment='罚球')
    free_throws_total = Column(Integer, nullable=True, default=0, comment='罚球总数')
    free_throws_accuracy = Column(String(10), nullable=True, default=0, comment='罚球命中率')

    total_fouls = Column(Integer, nullable=True, default=0, comment='犯规')
    timeouts = Column(Integer, nullable=True, default=0, comment='暂停')

    ball_possession = Column(Integer, nullable=True, default=0, comment='控球')
    rebounds = Column(Integer, nullable=True, default=0, comment='篮板')
    defensive_rebounds = Column(Integer, nullable=True, default=0, comment='防守篮板')
    offensive_rebounds = Column(Integer, nullable=True, default=0, comment='进攻篮板')
    assists = Column(Integer, nullable=True, default=0, comment='助攻')
    turnovers = Column(Integer, nullable=True, default=0, comment='失误')
    steals = Column(Integer, nullable=True, default=0, comment='抢断')
    blocks = Column(Integer, nullable=True, default=0, comment='盖帽')
    max_points_in_arow = Column(Integer, nullable=True, default=0, comment='最多连续得分')
    time_spent_in_lead = Column(Integer, nullable=True, default=0, comment='领先时间')
    lead_changes = Column(Integer, nullable=True, default=0, comment='领先变化')
    biggest_lead = Column(Integer, nullable=True, default=0, comment='最大领先优势')
    successful_attempts = Column(Integer, nullable=True, default=0, comment='出手命中')

    streaks = Column(Integer, nullable=True, default=0, comment='连胜(败)次数')

    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 球员榜统计
class BleagueNblBasketballPlayerTotal(BaseModel):
    __tablename__ = prefix + 'player_total'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, index=True, comment='key')
    sport_id = Column(Integer, index=True, nullable=False, comment='球类id')
    season_id = Column(Integer, index=True, nullable=False, comment='赛季id')
    team_id = Column(Integer, index=True, nullable=False, comment='球队id')
    player_id = Column(Integer, index=True, nullable=False, comment='球员id')

    # 字段
    scope = Column(Integer, default=0, comment='统计范围 1-赛季 2-预选赛 3-小组赛 4-季前赛 5-常规赛 6-淘汰赛(季后赛)')
    period = Column(Integer, default=0, comment='比赛阶段')
    matches = Column(Integer, default=0, comment='比赛场次')
    court = Column(Integer, default=0, comment='上场场次')

    # 总结
    minutes_played = Column(Integer, nullable=True, default=0, comment='上场时间')
    position = Column(String(5), nullable=False, server_default='', default='', comment='位置')

    # 得分
    points = Column(Integer, nullable=True, default=0, comment='得分')
    free_throws_scored = Column(Integer, nullable=True, default=0, comment='罚球命中数')
    free_throws_total = Column(Integer, nullable=True, default=0, comment='罚球总数')
    free_throws_accuracy = Column(String(10), nullable=True, default='', comment='罚球命中率')
    two_points_scored = Column(Integer, nullable=True, default=0, comment='两分球命中数')
    two_points_total = Column(Integer, nullable=True, default=0, comment='两分球总数')
    two_points_accuracy = Column(String(10), nullable=True, default=0, comment='两分球命中率')
    three_points_scored = Column(Integer, nullable=True, default=0, comment='三分球命中数')
    three_points_total = Column(Integer, nullable=True, default=0, comment='三分球总数')
    three_points_accuracy = Column(String(10), nullable=True, default=0, comment='三分球命中率')
    field_goals_scored = Column(Integer, nullable=True, default=0, comment='投篮命中数')
    field_goals_total = Column(Integer, nullable=True, default=0, comment='投篮总数')
    field_goals_accuracy = Column(String(10), nullable=True, default=0, comment='投篮命中率')

    # 篮板
    rebounds = Column(Integer, nullable=True, default=0, comment='篮板')
    defensive_rebounds = Column(Integer, nullable=True, default=0, comment='防守篮板')
    offensive_rebounds = Column(Integer, nullable=True, default=0, comment='进攻篮板')

    # 其他
    assists = Column(Integer, nullable=True, default=0, comment='助攻')
    turnovers = Column(Integer, nullable=True, default=0, comment='失误')
    steals = Column(Integer, nullable=True, default=0, comment='抢断')
    blocks = Column(Integer, nullable=True, default=0, comment='盖帽')
    personal_fouls = Column(Integer, nullable=True, default=0, comment='个人犯规')
    plus_minus = Column(Integer, nullable=True, default=0, comment='+/-')

    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 球队榜统计(计算)
class BleagueNblBasketballTeamTotalCal(BaseModel):
    __tablename__ = prefix + 'team_total_cal'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, index=True, comment='key')
    sport_id = Column(Integer, index=True, nullable=False, comment='球类id')
    season_id = Column(Integer, index=True, nullable=False, comment='赛季id')
    team_id = Column(Integer, index=True, nullable=False, comment='球队id')

    # 字段
    scope = Column(Integer, default=0, comment='统计范围 1-赛季 2-预选赛 3-小组赛 4-季前赛 5-常规赛 6-淘汰赛(季后赛)')
    period = Column(Integer, default=0, comment='比赛阶段')
    matches = Column(Integer, default=0, comment='比赛场次')

    points = Column(Integer, nullable=True, default=0, comment='得分')
    points_against = Column(Integer, nullable=True, default=0, comment='失分')

    two_pointers_scored = Column(Integer, nullable=True, default=0, comment='两分球')
    two_pointers_total = Column(Integer, nullable=True, default=0, comment='两分球总数')
    two_pointers_accuracy = Column(String(10), nullable=True, default=0, comment='两分球命中率')
    three_pointers_scored = Column(Integer, nullable=True, default=0, comment='三分球')
    three_pointers_total = Column(Integer, nullable=True, default=0, comment='三分球总数')
    three_pointers_accuracy = Column(String(10), nullable=True, default=0, comment='三分球命中率')
    field_goals_scored = Column(Integer, nullable=True, default=0, comment='投篮')
    field_goals_total = Column(Integer, nullable=True, default=0, comment='投篮总数')
    field_goals_accuracy = Column(String(10), nullable=True, default=0, comment='投篮命中率')
    free_throws_scored = Column(Integer, nullable=True, default=0, comment='罚球')
    free_throws_total = Column(Integer, nullable=True, default=0, comment='罚球总数')
    free_throws_accuracy = Column(String(10), nullable=True, default=0, comment='罚球命中率')

    total_fouls = Column(Integer, nullable=True, default=0, comment='犯规')
    timeouts = Column(Integer, nullable=True, default=0, comment='暂停')

    ball_possession = Column(Integer, nullable=True, default=0, comment='控球')
    rebounds = Column(Integer, nullable=True, default=0, comment='篮板')
    defensive_rebounds = Column(Integer, nullable=True, default=0, comment='防守篮板')
    offensive_rebounds = Column(Integer, nullable=True, default=0, comment='进攻篮板')
    assists = Column(Integer, nullable=True, default=0, comment='助攻')
    turnovers = Column(Integer, nullable=True, default=0, comment='失误')
    steals = Column(Integer, nullable=True, default=0, comment='抢断')
    blocks = Column(Integer, nullable=True, default=0, comment='盖帽')
    max_points_in_arow = Column(Integer, nullable=True, default=0, comment='最多连续得分')
    time_spent_in_lead = Column(Integer, nullable=True, default=0, comment='领先时间')
    lead_changes = Column(Integer, nullable=True, default=0, comment='领先变化')
    biggest_lead = Column(Integer, nullable=True, default=0, comment='最大领先优势')
    successful_attempts = Column(Integer, nullable=True, default=0, comment='出手命中')

    streaks = Column(Integer, nullable=True, default=0, comment='连胜(败)次数')

    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 球员榜统计(计算)
class BleagueNblBasketballPlayerTotalCal(BaseModel):
    __tablename__ = prefix + 'player_total_cal'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, index=True, comment='key')
    sport_id = Column(Integer, index=True, nullable=False, comment='球类id')
    season_id = Column(Integer, index=True, nullable=False, comment='赛季id')
    team_id = Column(Integer, index=True, nullable=False, comment='球队id')
    player_id = Column(Integer, index=True, nullable=False, comment='球员id')

    # 字段
    scope = Column(Integer, default=0, comment='统计范围 1-赛季 2-预选赛 3-小组赛 4-季前赛 5-常规赛 6-淘汰赛(季后赛)')
    period = Column(Integer, default=0, comment='比赛阶段')
    matches = Column(Integer, default=0, comment='比赛场次')
    first = Column(Integer, default=0, comment='首发场次')
    court = Column(Integer, default=0, comment='上场场次')

    # 总结
    minutes_played = Column(Integer, nullable=True, default=0, comment='上场时间')
    position = Column(String(5), nullable=False, server_default='', default='', comment='位置')

    # 得分
    points = Column(Integer, nullable=True, default=0, comment='得分')
    free_throws_scored = Column(Integer, nullable=True, default=0, comment='罚球命中数')
    free_throws_total = Column(Integer, nullable=True, default=0, comment='罚球总数')
    free_throws_accuracy = Column(String(10), nullable=True, default='', comment='罚球命中率')
    two_points_scored = Column(Integer, nullable=True, default=0, comment='两分球命中数')
    two_points_total = Column(Integer, nullable=True, default=0, comment='两分球总数')
    two_points_accuracy = Column(String(10), nullable=True, default=0, comment='两分球命中率')
    three_points_scored = Column(Integer, nullable=True, default=0, comment='三分球命中数')
    three_points_total = Column(Integer, nullable=True, default=0, comment='三分球总数')
    three_points_accuracy = Column(String(10), nullable=True, default=0, comment='三分球命中率')
    field_goals_scored = Column(Integer, nullable=True, default=0, comment='投篮命中数')
    field_goals_total = Column(Integer, nullable=True, default=0, comment='投篮总数')
    field_goals_accuracy = Column(String(10), nullable=True, default=0, comment='投篮命中率')

    # 篮板
    rebounds = Column(Integer, nullable=True, default=0, comment='篮板')
    defensive_rebounds = Column(Integer, nullable=True, default=0, comment='防守篮板')
    offensive_rebounds = Column(Integer, nullable=True, default=0, comment='进攻篮板')

    # 其他
    assists = Column(Integer, nullable=True, default=0, comment='助攻')
    turnovers = Column(Integer, nullable=True, default=0, comment='失误')
    steals = Column(Integer, nullable=True, default=0, comment='抢断')
    blocks = Column(Integer, nullable=True, default=0, comment='盖帽')
    personal_fouls = Column(Integer, nullable=True, default=0, comment='个人犯规')
    plus_minus = Column(Integer, nullable=True, default=0, comment='+/-')

    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))



#历史文本记录
class BleagueBasketballGameText(BaseModel):

    __tablename__ = prefix + 'game_text'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(25), nullable=False, server_default='', default='', index=True)
    sport_id = Column(Integer, index=True, nullable=False, server_default='0', default=0, comment='球类id')   #2

    season_id = Column(Integer, index=True, nullable=True, server_default='0', default=0, comment='赛季id')   #如2017，2018等
    competition_id = Column(Integer, index=True, nullable=False, server_default='0', default=0,
                            comment='联赛id')  # b1或者b2  1，2
    period = Column(Integer, index=True, nullable=True, server_default='0', default=0, comment='第几节') #1,2,3,4,5
    # stage_id = Column(Integer, index=True, nullable=True, server_default='0', default=0, comment='阶段id')
    round_num = Column(Integer, nullable=False, server_default='0', default=0, comment='第几轮')  # 轮次  第几轮
    team_id = Column(Integer, index=True, nullable=True, server_default='0', default=0, comment='当前队伍id') #1代表主队  2代表客队
    match_id = Column(Integer, index=True, nullable=True, server_default='0', default=0, comment='比赛id')  #比赛的id
    # 字段
    # name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    # name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    # name_zht = Column(String(255), nullable=False, server_default='', default='', comment='繁体名称')
    # group = Column(Integer, nullable=True, server_default='0', default=0, comment='分组')
    # conference = Column(String(255), nullable=False, server_default='', default='', comment='分区名称')

    # scope = Column(Integer, default=0, comment='统计范围 1-赛季 2-预选赛 3-小组赛 4-季前赛 5-常规赛 6-淘汰赛(季后赛)')
    # order = Column(Integer, nullable=True, server_default='0', default=0, comment='排序')
    words_text = Column(String(255), nullable=False, server_default='', default='', comment='文字直播内容')
    time_info = Column(String(255), nullable=False, server_default='', default='', comment='文字直播时间标示')
    score_info = Column(String(255), nullable=False, server_default='', default='', comment='当前比分消息')

    # 通用字段

    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))





#处理xml文件  临时表格
class Xmlchangekey(BaseModel):
    __tablename__ = 'xml_data'

    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(100), nullable=False, index=True, comment='key')
    en = Column(String(255), nullable=False, default='', comment='en')
    af = Column(String(255), nullable=False, default='', comment='af')
    am = Column(String(255), nullable=False, default='', comment='am')
    ar = Column(String(255), nullable=False, default='', comment='ar')
    as1 = Column(String(255), nullable=False, default='', comment='as1')
    az = Column(String(255), nullable=False, default='', comment='az')
    b_sr_Latn = Column(String(100), nullable=False, default='', comment='b+sr+Latn')
    be = Column(String(100), nullable=False, default='', comment='be')
    bg = Column(String(100), nullable=False, default='', comment='bg')
    bn = Column(String(100), nullable=False, default='', comment='bn')
    bs = Column(String(100), nullable=False, default='', comment='bs')
    ca = Column(String(100), nullable=False, default='', comment='ca')
    cs = Column(String(100), nullable=False, default='', comment='cs')
    da = Column(String(100), nullable=False, default='', comment='da')
    de = Column(String(100), nullable=False, default='', comment='de')
    el = Column(String(100), nullable=False, default='', comment='el')
    en_rAU = Column(String(100), nullable=False, default='', comment='en_rAu')
    en_rCA = Column(String(100), nullable=False, default='', comment='en_rCA')
    en_rGB = Column(String(100), nullable=False, default='', comment='en_rGB')
    en_rIN = Column(String(100), nullable=False, default='', comment='en_rIN')
    en_rXC = Column(String(100), nullable=False, default='', comment='en_rXC')
    es = Column(String(100), nullable=False, default='', comment='es')
    es_rES = Column(String(100), nullable=False, default='', comment='es_rES')
    es_rUS = Column(String(100), nullable=False, default='', comment='en_rUS')
    et = Column(String(100), nullable=False, default='', comment='et')
    eu = Column(String(100), nullable=False, default='', comment='eu')
    fa = Column(String(100), nullable=False, default='', comment='fa')
    fi = Column(String(100), nullable=False, default='', comment='fi')
    fr = Column(String(100), nullable=False, default='', comment='fr')
    fr_rCA = Column(String(100), nullable=False, default='', comment='fr_rCA')
    gl = Column(String(100), nullable=False, default='', comment='gl')
    gu = Column(String(100), nullable=False, default='', comment='gu')
    hi = Column(String(100), nullable=False, default='', comment='hi')
    hr = Column(String(100), nullable=False, default='', comment='hr')
    hu = Column(String(100), nullable=False, default='', comment='hu')
    hy = Column(String(100), nullable=False, default='', comment='hy')
    id1 = Column(String(100), nullable=False, default='', comment='id')
    in1 = Column(String(100), nullable=False, default='', comment='in1')
    is1 = Column(String(100), nullable=False, default='', comment='is1')
    it1 = Column(String(100), nullable=False, default='', comment='it1')
    iw1 = Column(String(100), nullable=False, default='', comment='iw1')
    ja = Column(String(100), nullable=False, default='', comment='ja')
    ja_rJP = Column(String(100), nullable=False, default='', comment='ja_rJP')
    ka = Column(String(100), nullable=False, default='', comment='ka')
    kk = Column(String(100), nullable=False, default='', comment='kk')
    km = Column(String(100), nullable=False, default='', comment='km')
    kn = Column(String(100), nullable=False, default='', comment='kn')
    ko = Column(String(100), nullable=False, default='', comment='ko')
    ky = Column(String(100), nullable=False, default='', comment='ky')
    lo = Column(String(100), nullable=False, default='', comment='lo')
    lt = Column(String(100), nullable=False, default='', comment='lt')
    lv = Column(String(100), nullable=False, default='', comment='lv')
    mdpi = Column(String(100), nullable=False, default='', comment='mdpi')
    mk = Column(String(100), nullable=False, default='', comment='mk')
    ml = Column(String(100), nullable=False, default='', comment='ml')
    mn = Column(String(100), nullable=False, default='', comment='mn')
    mr = Column(String(100), nullable=False, default='', comment='mr')
    ms = Column(String(100), nullable=False, default='', comment='ms')
    my = Column(String(100), nullable=False, default='', comment='my')
    nb = Column(String(100), nullable=False, default='', comment='nb')
    ne = Column(String(100), nullable=False, default='', comment='ne')
    nl = Column(String(100), nullable=False, default='', comment='nl')
    or1 = Column(String(100), nullable=False, default='', comment='or')
    pa = Column(String(100), nullable=False, default='', comment='pa')
    pl = Column(String(100), nullable=False, default='', comment='pl')
    pt = Column(String(100), nullable=False, default='', comment='pt')
    pt_rBR = Column(String(100), nullable=False, default='', comment='pt_rBR')
    pt_rPT = Column(String(100), nullable=False, default='', comment='pt_rPT')
    ro = Column(String(100), nullable=False, default='', comment='ro')
    ru = Column(String(100), nullable=False, default='', comment='ru')
    si = Column(String(100), nullable=False, default='', comment='si')
    sk = Column(String(100), nullable=False, default='', comment='sk')
    sl = Column(String(100), nullable=False, default='', comment='sl')
    sq = Column(String(100), nullable=False, default='', comment='sq')
    sr = Column(String(100), nullable=False, default='', comment='sr')
    sv = Column(String(100), nullable=False, default='', comment='sv')
    sw = Column(String(100), nullable=False, default='', comment='sw')
    ta = Column(String(100), nullable=False, default='', comment='ta')
    te = Column(String(100), nullable=False, default='', comment='te')
    th = Column(String(100), nullable=False, default='', comment='th')
    tl = Column(String(100), nullable=False, default='', comment='tl')
    tr = Column(String(100), nullable=False, default='', comment='tr')
    uk = Column(String(100), nullable=False, default='', comment='uk')
    ur = Column(String(100), nullable=False, default='', comment='ur')
    uz = Column(String(100), nullable=False, default='', comment='uz')
    vi = Column(String(100), nullable=False, default='', comment='vi')
    zh_rCN = Column(String(100), nullable=False, default='', comment='zh_rCN')
    zh_rHK = Column(String(100), nullable=False, default='', comment='zh_rHK')
    zh_rTW = Column(String(100), nullable=False, default='', comment='zh_rTW')
    zu = Column(String(100), nullable=False, default='', comment='zu')



class BleagueAcbBasketballReferee(BaseModel):
    __tablename__ = prefix + 'referee'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')
    key = Column(String(100), nullable=False, server_default='', default='', index=True)
    # 字段
    name_en = Column(String(255), nullable=False, server_default='', default='', comment='英文名称')
    name_zh = Column(String(255), nullable=False, server_default='', default='', comment='中文名称')
    name_zht = Column(String(255), nullable=False, server_default='', default='', comment='繁体名称')
    logo = Column(String(255), nullable=False, server_default='', default='', comment='logo')
    age = Column(Integer, nullable=False, server_default='0', default=0, comment='年龄')
    birthday = Column(Integer, nullable=False, server_default='0', default=0, comment='生日')
    matchs = Column(Integer, nullable=False, server_default='0', default=0, comment='执法场次')
    # 通用字段
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
