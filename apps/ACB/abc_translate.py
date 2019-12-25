import re

from apps.ACB.tools import get_acb_nana_player_name_zh

words = {'game end': '比赛结束', 'period end': '赛节结束', 'rebound defensive': '防守篮板', '2pt layup missed': '2分上篮不中',
         'steal ': '抢断',
         'turnover badpass': '传球失误', '3pt jumpshot missed': '3分跳投不中', 'timeout full': '长暂停',
         '2of2 Perth Wildcats': '第2罚(2罚):命中', '1of2 Perth Wildcats': '第1罚(2罚):命中', 'substitution in': '替换上场',
         'substitution out': '替换下场', 'foulon ': '被犯规', 'foul personal': '个人犯规', '2pt layup': '2分上篮命中',
         'freethrow 2of2 missed': '第2罚(2罚):不中', 'freethrow 1of2': '第1罚(2罚):命中', '2pt jumpshot missed': '2分跳投不中',
         'rebound offensive': '进攻篮板', 'block ': '封盖', 'turnover backcourt': '回场违例', '2pt fadeaway': '2分后仰投篮命中',
         'assist ': '助攻',
         'freethrow 2of2': '第2罚(2罚):命中', 'rebound offensivedeadball': '死球进攻篮板', 'freethrow 1of2 missed': '第1罚(2罚):不中',
         '2pt fadeaway missed': '2分后仰投篮不中', 'freethrow 3of3': '第3罚(3罚):命中', 'freethrow 2of3': '第2罚(3罚):命中',
         'freethrow 1of3': '第1罚(3罚):命中', '3pt jumpshot': '3分跳投命中', '2pt hookshot missed': '2分勾手投篮不中',
         'turnover travel': '走步失误',
         'foul unsportsmanlike': '违体犯规', '2pt drivinglayup': '2分突破上篮命中', 'jumpshot missed': '3分跳投不中',
         '2pt layup ': '2分上篮命中',
         '2pt floatingjumpshot missed': '2分漂移跳投不中', '3pt stepbackjumpshot': '3分后撤步跳投不中',
         '2pt floatingjumpshot': '2分漂移跳投命中',
         'freethrow 2of2 ': '第2罚(2罚):不中', 'jumpball heldball': '跳球 双方持球', 'turnover offensive': '进攻失误',
         'foul offensive': '进攻犯规', 'period start': '赛节开始', 'freethrow 1of1': '第1罚(2罚):命中',
         'turnover ballhandling': '运球失误',
         'turnover 3sec': '3秒违例失误', '2pt stepbackjumpshot missed': '2分后撤步跳投不中', '2pt dunk': '2分扣篮命中',
         '2pt pullupjumpshot': '2分跳投命中', '2pt jumpshot': '2分跳投命中', '2pt floatingjumpshot ': '2分漂移跳投命中',
         '3pt stepbackjumpshot missed': '3分后撤步跳投不中', '3pt fadeaway missed': '3分后仰投篮不中',
         'freethrow 3of3 missed': '第3罚(3罚):不中',
         '2pt hookshot': '2分勾手投篮命中', '2pt drivinglayup missed': '2分突破上篮不中', 'freethrow 1of2 ': '第1罚(2罚):命中',
         '2pt turnaroundjumpshot missed': '2分转身跳投命中', 'turnover outofbounds': '出界失误',
         '2pt turnaroundjumpshot': '2分转身跳投命中',
         ',3pt jumpshot missed': '3分跳投不中', '2pt pullupjumpshot missed': '2分急停跳投不中', 'jumpball - lost': '跳球-失败',
         'jumpball - won': '跳球-获胜', 'jumpball startperiod': '开场跳球', 'game start': '比赛开始',
         'Free throw 1 of 1 missed': '第1罚不中（1罚）',
         'Technical foul': '技术犯规', '2pt alleyoop': '2分空中接力命中', 'jumpball lodgedball': "双方倒地争抢形成争球",
         'turnover doubledribble': '两次运球失误',
         '3pt pullupjumpshotmissed': '3分急停跳投不中', '3pt pullupjumpshotmade': '3分急停跳投命中',
         '2pt stepbackjumpshot': '2分后撤步跳投命中', '3pt fadeaway': '3分后仰跳投', '3pt pullupjumpshot': '3分急停跳投',
         'turnover 24sec': '24秒违例', 'missed': '', 'foul': '犯规', '3pt floatingjumpshot': '3分空中漂移投篮','3pt turnaroundjumpshot':'3分转身跳投'}

players_sql = get_acb_nana_player_name_zh()
players_update = {}
players = dict(list(players_sql.items()) + list(players_update.items()))


def translate(text):
    text = text.lower()
    # for teamname_en, teamname_cn in sorted(nbateams.items(), reverse=True):
    #     teamname_en = teamname_en.lower()
    #     teamname_abbr = teamname_en.split()[-1]
    #     ind = text.find(teamname_abbr)
    #     if ind != -1:
    #         ind = len(teamname_abbr) + ind
    #         text = text.replace(text[0:ind], teamname_cn)
    for word_en, word_cn in sorted(words.items(), key=lambda t: len(t[0]), reverse=True):
        m = re.search(word_en, text)
        if m:
            try:
                num = m.group(1)
            except IndexError:
                word_en = m.group()
                text = text.replace(word_en, word_cn)
            else:
                word_en = m.group()
                if '的' in word_cn:
                    text = text.replace(word_en, ''.join(['的', num, word_cn.replace('的', '')]))
                else:
                    text = text.replace(word_en, ''.join([num, word_cn]))

    text = text.replace('-', ' ')
    for name_en, name_cn in players.items():
        name_en = name_en.lower()
        if name_en in text:
            text = text.replace(name_en, name_cn.replace('-', '·'))

    return text.replace('\t', '').strip().replace(',', ' ')
