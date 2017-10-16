# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
import json
import re
import codecs
import tinify
import xpinyin
import os


def d_format(word):
    while '[' in word:
        a = word.index('[')
        b = word.index(']')
        word = word[:a] + word[b + 1:]
    return word.strip('=')


def get_class(word):
    check = dict(zip(['法', '德', '战', '牧', '术', '园', '贼', '猎', '萨', '骑'],
                     ['法师', '德鲁伊', '战士', '牧师', '术士', '术士', '潜行者', '猎人', '萨满', '骑士']))
    return check[word[-1]]


def get_deck(word, info):
    for (key, value) in info.items():
        if isinstance(value, dict):
            for decks in value.get('deck', []):
                if decks['name'] == word:
                    return decks
    return {}


def update_deck(decks, info):
    word = decks['name']
    for (key, value) in info.items():
        if isinstance(value, dict):
            for index, temps in enumerate(value.get('deck', [])):
                if temps['name'] == word:
                    value.get('deck')[index] = decks
    return info


if __name__ == '__main__':
    exceptions_list = {}  # 卡组名前后不一致时添加对应关系
    pinyin, tinify.key = xpinyin.Pinyin(), 'm1wfTSfLD9GUu5uJ9iPLUW3H6dTEUhA3'
    href = 'https://longlang.github.io/deckimg/'  # 图片服务器地址前缀
    tid = 12607715  # nga文章tid编号
    if not os.path.exists('ts/' + unicode(tid)):
        os.mkdir(str('ts/' + unicode(tid)))
    ts_url = 'http://bbs.nga.cn/read.php?tid=' + unicode(tid)
    web = requests.session()
    web.trust_env = False
    soup = BeautifulSoup(web.get(ts_url).content, "html.parser")
    deck_info = {'intro': '', 'TS': {'Tintro': '', 'deck': []}, 'T1': {'Tintro': '', 'deck': []},
                 'T2': {'Tintro': '', 'deck': []}, 'T3': {'Tintro': '', 'deck': []}, 'T4': {'Tintro': '', 'deck': []},
                 'T5': {'Tintro': '', 'deck': []}}
    rank, deck_name, deck, level, title = 0, '', {}, 'TS', ''
    for string in soup.p.stripped_strings:
        string_ = d_format(string)
        if '[h]' in string:
            title = string_
            i = 0
        print string, '****', title
        if title == '引言' and re.match(str(r'^T.：'), string_):
            temp = string_.split('：')
            deck_info[temp[0]]['Tintro'] = temp[1]
        elif title == '本期简介':
            if '[' not in string and ']' not in string:
                deck_info['intro'] += string
            elif re.match(str(r'^T.：'), string_):
                temp = string_.split('：')
                for item in temp[1].split('、'):
                    for k, v in exceptions_list.items():
                        if item.startswith(k):
                            item = v + '(' + item.split('(')[1]
                    rank += 1
                    try:
                        deck = {'name': item.split('(')[0], 'weekRating': unicode(rank) + '(' + item.split('(')[1],
                                'class': get_class(item.split('(')[0])}
                        deck_info[temp[0]]['deck'].append(deck)
                    except (IndexError, KeyError):
                        deck = {'name': item, 'weekRating': '(-)',
                                'class': get_class(item)}
                        deck_info[temp[0]]['deck'].append(deck)
        elif re.match(str(r'^T.卡组'), title):
            level = title[:2]
            if '[/color]' in string and string.startswith('=='):
                if deck_name:
                    deck_info = update_deck(deck, deck_info)
                deck_name = string_
                deck = get_deck(deck_name, deck_info)
            elif string_.endswith('.png') and string_.startswith('./'):
                imgUrl = r'http://img.ngacn.cc/attachments' + string_[string_.index('/'):]
                deck['imgUrl'] = imgUrl
                source = tinify.from_url(imgUrl)
                source.to_file('ts/' + unicode(tid) + '/' + level + '-' + pinyin.get_pinyin(deck_name, '') + '.png')
                deck['imgSrc'] = href + level + '-' + pinyin.get_pinyin(deck_name, '') + '.png'
            elif string.startswith('套牌代码：') or string.startswith('代码：'):
                deck['code'] = string.split('：')[1]
            elif string.startswith('对阵快攻：'):
                deck['toFast'] = string.split('：')[1]
            elif string.startswith('对阵控制：'):
                deck['toControl'] = string.split('：')[1]
            elif string.startswith('劣势对抗：'):
                deck['cons'] = string.split('：')[1].split('、')
            elif '[' not in string and ']' not in string:
                deck['cardIntro'] = deck.get('cardIntro', '') + string
    print json.dumps(deck_info, ensure_ascii=False, indent=4)
    with codecs.open('ts/' + unicode(tid) + '/ts.json', 'wb', 'utf-8') as f:
        f.write(json.dumps(deck_info, ensure_ascii=False, indent=4))
