#coding:utf-8
import re
import pandas as pd


words = {'Assist ': '助攻', 'Begin Period': '比赛开始', 'Bench Foul ': '板凳犯规', 'Block ': '盖帽', 'Coach Foul ': '教练犯规', 'Def Rebound ': '防守篮板', 'End Game': '比赛结束', 'End Period': '本节结束', 'Foul Drawn ': '累计犯规', 'Free Throw In ': '罚球命中', 'Missed Free Throw ': '罚球不中', 'Missed Three Pointer ': '3分不中', 'Missed Two Pointer ': '2分不中', 'Off Rebound ': '前场篮板', 'Offensive Foul ': '进攻犯规', 'Shot Rejected ': '投篮被盖', 'Steal ': '抢断', 'Technical Foul ': '技术犯规', 'Three Pointer ': '三分命中', 'Time Out ': '暂停', 'Turnover ': '失误', 'TV Time Out ': '官方 暂停', 'Two Pointer ': '2分命中', 'Unsportsmanlike Foul  ': '违体犯规', 'Layup Made': '上篮得分', 'Missed Layup': '上篮不中', 'Foul ': '犯规', 'Out': '下场', 'In': '上场', 'Tip Off': '跳球', 'Tech Foul Coach': '教练技术犯规'}

def translate(text):
    text = text
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

    # text = text.replace('-', ' ')
    # for name_en, name_cn in players.items():
    #     name_en = name_en.lower()
    #     if name_en in text:
    #         text = text.replace(name_en, name_cn.replace('-', '·'))
    #
    return text.replace('\t', '').strip().replace(',',' ')

str1 = 'Begin Period'
print(translate(str1))