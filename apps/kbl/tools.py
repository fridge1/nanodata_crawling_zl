# -*- coding: utf-8 -*-
import requests
from lxml import etree
import datetime,time
from datetime import date
from orm_connection.orm_session import MysqlSvr
from orm_connection.kbl_basketball import *
import re
import pandas as pd


def tree_parse(res):
    enconding = requests.utils.get_encodings_from_content(res.text)
    html_doc = res.content.decode(enconding[0])
    tree = etree.HTML(html_doc)
    return tree

def age_timeStamp(birthday):
    time_format = datetime.datetime.strptime(birthday, '%Y-%m-%d')
    timeArray = time.strptime(birthday, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    today = date.today()
    age = today.year - time_format.year - ((today.month, today.day) < (time_format.month, time_format.day))
    return timeStamp,age


def get_school_id(school_key):
    spx_dev_session = MysqlSvr.get('spider_zl')
    school_data = {
        'key':school_key,
        'name_en':school_key,
    }
    _, row = BleagueNblBasketballSchool.upsert(
                        spx_dev_session,
                        'key',
                        school_data
                    )
    return row.id


def get_manager_id(manager_key,team_id,assistant):
    spx_dev_session = MysqlSvr.get('spider_zl')
    manager_data = {
        'key':manager_key,
        'name_en':manager_key,
        'team_id':team_id,
        'assistant':assistant,
        'sport_id':2,
    }
    _, row = BleagueNblBasketballManager.upsert(
                        spx_dev_session,
                        'key',
                        manager_data
                    )
    return row.id


def get_city_id(city_key):
    spx_dev_session = MysqlSvr.get('spider_zl')
    city_data = {
        'key':city_key,
        'name_en':city_key,
    }
    _, row = BleagueNblBasketballCity.upsert(
                        spx_dev_session,
                        'key',
                        city_data
                    )
    return row.id


def change_bjtime(date):
    time_format = datetime.datetime.strptime(date, '%Y%m%d%H:%M')
    timeArray = datetime.datetime.strftime(time_format, '%Y.%m.%d %H:%M')
    timeArray1 = datetime.datetime.strptime(timeArray, '%Y.%m.%d %H:%M')
    bj_time = (timeArray1+datetime.timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M")
    bj_time1 = datetime.datetime.strptime(bj_time, '%Y-%m-%d %H:%M')
    timeStamp = int(time.mktime(bj_time1.timetuple()))
    return timeStamp


def get_team_id(team_name,logo):
    spx_dev_session = MysqlSvr.get('spider_zl')
    result = spx_dev_session.query(BleagueNblBasketballTeam).filter(BleagueNblBasketballTeam.name_en == logo).all()
    try:
        return result[0].id
    except:
        id = re.findall(r'\d+',logo)[0]
        team_data = {
            'id': id,
            'logo': logo,
            'name_en': team_name,
            'sport_id' : 2,
        }
        _, row = BleagueNblBasketballTeam.upsert(
            spx_dev_session,
            'id',
            team_data
        )
        return row.id

def change_match_bjtime(date):
    time_format = datetime.datetime.strptime(date, '%Y%m%d %H:%M')
    timeArray = datetime.datetime.strftime(time_format, '%Y%m%d %H:%M')
    timeArray1 = datetime.datetime.strptime(timeArray, '%Y%m%d %H:%M')
    bj_time = (timeArray1+datetime.timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M")
    bj_time1 = datetime.datetime.strptime(bj_time, '%Y-%m-%d %H:%M')
    timeStamp = int(time.mktime(bj_time1.timetuple()))
    return timeStamp

def get_team_name_id(team_name):
    try:
        spx_dev_session = MysqlSvr.get('spider_zl')
        return spx_dev_session.query(BleagueNblBasketballTeam).filter(BleagueNblBasketballTeam.name_en.like('%%'+team_name+'%%')).all()[0].id
    except:
        return 0

def get_player_name_id(player_name):
    try:
        spx_dev_session = MysqlSvr.get('spider_zl')
        return spx_dev_session.query(BleagueNblBasketballPlayer).filter(BleagueNblBasketballPlayer.name_en==player_name).all()[0].id
    except:
        return 0


def get_team_name():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueNblBasketballTeam).all()
    data_dict = {row.id: row.name_en for row in rows}
    return data_dict

def get_match_id():
    spx_dev_session = MysqlSvr.get('spider_zl')
    rows = spx_dev_session.query(BleagueNblBasketballMatch).filter(BleagueNblBasketballMatch.status_id==10).all()
    data_dict = {row.key: row.id for row in rows}
    return data_dict

def get_player_id():
    spx_dev_session = MysqlSvr.get('spider_zl')
    id_list = spx_dev_session.query(BleagueNblBasketballPlayer).all()
    list1 = []
    for player_info in id_list:
        list1.append(player_info.id)
    return list1

def upsert_player_id(id,name_en,team_id,shirt_number,position):
    spx_dev_session = MysqlSvr.get('spider_zl')
    data = {
        'id':int(id),
        'name_en':str(name_en),
        'team_id':int(team_id),
        'shirt_number':int(shirt_number),
        'position':str(position),
    }
    _, row = BleagueNblBasketballPlayer.upsert(
        spx_dev_session,
        'id',
        data
    )
    return row.id





season_id_dict = {'2008-2009': 1, '2009-2010': 2, '2010-2011': 3, '2011-2012': 4, '2012-2013': 5, '2013-2014': 6, '2014-2015': 7, '2015-2016': 8, '2016-2017': 9, '2017-2018': 10, '2018-2019': 11, '2019-2020': 12}
translater_team_name = {1: '양홍석매직팀', 2: '드림', 5: '여수 코리아텐더', 6: '부산KT', 10: '울산현대모비스', 15: '원주TG삼보', 16: '원주DB', 20: '광주나산', 25: '인천대우', 30: '고양오리온', 35: '서울삼성', 37: '인천SK', 40: '안양SBS', 45: '대전현대', 50: '창원LG', 55: '서울SK', 60: '전주KCC', 65: '인천전자랜드', 70: '안양KGC', 71: '주니어 올스타', 72: '시니어 올스타', 75: '상무', 76: '경희대', 77: '고려대', 80: '연세대', 81: '중앙대', 82: '한양대', 83: '건국대', 91: '중부선발', 92: '남부선발', 97: '드림팀', 98: '매직팀'}
translater_player_name = {'양동근': '梁东根', '조성민': '赵成珉', '오용준': '吴龙俊', '김동욱': '金东旭', '한정원': '韩正元', '이현민': '李贤敏', '함지훈': '洪志勋', '양희종': '杨熙钟', '김태술': '金泰戌', '송창무': '宋昌武', '정영삼': '郑永三', '신명호': '申明浩', '박상오': '朴常午', '김영환': '金英焕', '윤호영': '尹浩英', '김민수': '金民秀', '기승호': '姜胜浩', '강병현': '姜秉贤', '양우섭': '梁友燮', '애런 헤인즈': '艾伦·海恩斯', '문태영': '文泰英', '김강선': '金江善', '허일영': '许一英', '박성진': '朴成瑾', '전태풍': '全泰丰', '김우겸': '金宇圭', '변기훈': '卞基勋', '이민재': '李敏载', '찰스 로드': '查尔斯路', '송창용': '宋昌勇', '류종현': '柳宗贤', '민성주': '闵成珠', '박찬희': '朴灿熙', '이정현': '李正炫', '박형철': '朴亨哲', '김선형': '金善亨', '김현민': '金贤旻', '최진수': '崔镇秀', '김태홍': '金泰弘', '김우람': '金宇蓝', '함준후': '咸俊昊', '김현호': '金贤浩', '홍경기': '洪京奇', '김동량': '金东良', '유성호': '柳成浩', '이관희': '李冠熙', '오세근': '吴世根', '정창영': '郑昌永', '장민국': '张民国', '최지훈': '崔志勋', '최부경': '崔富京', '김건우': '金健友', '차바위': '车巴伟', '정준원': '郑俊元', '김승원': '金胜元', '최현민': '崔贤民', '박지훈': '朴智勋', '김시래': '金时来', '박병우': '朴丙宇', '조상열': '赵相烈', '리온 윌리엄스': '莱昂·威廉姆斯', '라건아': '罗健儿', '박경상': '朴京相', '정희재': '郑熙在', '임종일': '林宗日', '김현수': '金贤秀', '장재석': '张在锡', '임동섭': '林东硕', '김지완': '金智万', '김상규': '金相圭', '이원대': '李文代', '김윤태': '金允泰', '김민욱': '金敏旭', '유병훈': '刘炳勋', '배병준': '裴炳俊', '김종범': '金钟范', '한희원': '韩熙元', '성건주': '成建周', '이대헌': '李大宪', '한상혁': '韩相赫', '문성곤': '文成坤', '김창모': '金昌茂', '김영현': '金英贤', '이대성': '李大成', '박재현': '朴在贤', '김종규': '金宗圭', '한호빈': '韩浩彬', '임준수': '林俊秀', '이정제': '李正制', '김민구': '金敏具', '허웅': '许熊', '배수용': '裴秀勇', '김수찬': '金秀灿', '김준일': '金俊日', '배강률': '裴刚律', '최승욱': '崔升旭', '주지훈': '朱智勋', '이승현': '李胜贤', '송교창': '宋乔昌', '정성우': '郑成友', '박봉진': '朴峰真', '최성모': '崔成模', '이종현': '李宗贤', '김광철': '金光哲', '천기범': '千寄范', '최준용': '崔俊勇', '박인태': '朴仁泰', '장문호': '张文浩', '강상재': '姜相在', '김철욱': '金哲旭', '정희원': '郑熙元', '이진욱': '李真旭', '김낙현': '金洛贤', '최성원': '崔成元', '전태영': '全泰英', '남영길': '南英吉', '김진용': '金真勇', '안영준': '安英俊', '허훈': '许勋', '김국찬': '金国灿', '양홍석': '梁洪锡', '손홍준': '孙洪俊', '윤성원': '尹成元', '유현준': '柳贤俊', '김정년': '金正年', '브랜든 브라운': '布兰登·布朗', '머피 할로웨이': '墨菲·霍洛威', '섀넌 쇼터': '香农·肖特', '우동현': '禹东贤', '김성민': '金成民', '서명진': '徐明镇', '강바일': '江巴日', '전현우': '全贤友', '서현석': '徐贤锡', '권성진': '权成真', '장태빈': '张泰彬', '정진욱': '郑真旭', '조한진': '赵汉真', '김한솔': '金汉索', '김준형': '金俊亨', '원종훈': '元中勋', '이상민': '李相民', '권시현': '权时贤', '변준형': '卞俊迥', '임정헌': '林正宪', '천재민': '千在民', '박준영': '朴俊英', '홍석민': '洪锡民', '크리스 맥컬러': '克里斯托弗·麦卡洛', '알 쏜튼': '索顿', '바이런 멀린스': '拜伦·穆伦斯', '캐디 라렌': '科迪拉兰', '칼렙 그린': '加勒·格林', '닉 미네라스': '尼克·米纳拉斯', '델로이 제임스': '德利尔·詹姆斯', '자밀 워니': '贾米尔·沃尼', '조던 하워드': '乔丹·霍华德', '자코리 윌리엄스': '杰科里·威廉姆斯', '치나누 오누아쿠': '希纳努·奥努阿库', '마이크 해리스': '迈克·哈里斯', '전성환': '全成焕', '이재우': '李在友', '문상옥': '文相宇', '양재혁': '梁在赫', '김경원': '金京元', '박찬호': '朴灿浩', '김진영': '金真英', '권혁준': '权赫俊', '김세창': '金世昌', '김무성': '金武成', '박상권': '朴相权', '김훈': '金勋', '이동희': '李东熙', '박준은': '朴俊恩', '박건호': '朴建浩', '박정현': '朴正贤', '최진광': '崔真光', '임기웅': '林基文', '곽동기': '郭东基', '이진석': '李真锡', '김형빈': '金亨彬', '이윤수': '李允秀', '보리스 사보비치': '鲍里斯·萨沃伯', '카프리 알스턴': '卡弗里·阿尔斯顿','':''}
translate_pbp_dict = {'000': '없음', '001': '없음', '002': '比赛中断', '003': '短暂停', '009': '比赛结束', '010': '시간설정', '101': '被换上', '102': '被换下', '201': '两分球命中', '202': '两分球出手', '203': '罚球', '204': '자유투시도', '205': '三分球命中', '206': '三分球出手', '207': '扣篮', '208': '扣篮失败', '209': '进攻篮板', '210': '防守篮板', '211': '助攻', '212': '스틸', '213': '封盖', '214': '턴오버', '215': '犯规，对方罚球', '216': '犯规', '217': '팀속공', '218': '팀리바운드', '219': 'Illegal Def', '221': '防守', '223': '팀턴오버', '224': '其他犯规', '225': '全队犯规', 'EBF': '엘보우 파울', 'FRF': '三秒违例', 'FTF': '违体', 'PCF': '펀칭 파울', 'PNF': '犯规', 'TCF': '技术犯规', 'XXX': '없음', '104': '부상', '106': '퇴장', '000_0': '없음', '101_0': '없음', '104_0': '없음', '106_0': '없음', '106_1': '5次犯规', '106_2': '디스퀄리파잉', '106_3': '기타 퇴장'}