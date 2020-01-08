from sqlalchemy import Integer, Column, String, SmallInteger, TIMESTAMP, text, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from orm_connection.orm_base import *



engine = create_engine('mysql+pymysql://spider_zl:0EDbIRtu4JPGdiQnu3kvXxiOMDMjejow@rm-bp1ov656aj80p2ie8uo.mysql.rds.aliyuncs.com/spider_zl')

prefix = 'eur_league_basketball_'



# 球员表  -----2019所有b1b2的球队的现役球员已存
class BleagueEurBasketballPlayer(BaseModel):
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



# 球队教练表
class BleaguejpBasketballManager(BaseModel):
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
    team_key = Column(String(50), nullable=False, server_default='', default='', comment='队伍的key')
    deleted = Column(SmallInteger, nullable=False, server_default='0', default=0, comment='是否删除')
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# 球队表
class BleaguejpBasketballTeam(BaseModel):
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



# 球员榜统计
class BleaguejpBasketballPlayerTotal(BaseModel):
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


# 单场比赛球员统计       -------第三页内容  核心
class BleaguejpBasketballPlayerStats(BaseModel):
    __tablename__ = prefix + 'match_player_stat'

    # id和外部表id
    id = Column(Integer, primary_key=True, comment='id')                #team_id+player_id
    key = Column(String(255), index=True, server_default='', default='', comment='key')
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


# 比赛表      -------有些球队已经不在b1  b2了  信息不完整
class BleaguejpBasketballMatch(BaseModel):
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


class BleaguejpBasketballTeamStats(BaseModel):
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



class BleagueEurBasketballTable(BaseModel):
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
    updated_at = Column(TIMESTAMP, index=True, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))



BaseModel.metadata.create_all(engine)