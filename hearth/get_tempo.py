# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
import json
import codecs
import xpinyin


def d_format(word):
    while '[' in word:
        a = word.index('[')
        b = word.index(']')
        word = word[:a] + word[b + 1:]
    return word.strip('=')


def get_class(word):
    check = dict(zip(['法', '德', '战', '牧', '术', '园', '贼', '猎', '萨', '骑'],
                     ['法师', '德鲁伊', '战士', '牧师', '术士', '术士', '盗贼', '猎人', '萨满', '骑士']))
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
            for i, temps in enumerate(value.get('deck', [])):
                if temps['name'] == word:
                    value.get('deck')[i] = decks
    return info


if __name__ == '__main__':
    # exceptions_list = {'中速骑': '鱼人骑'}
    exceptions_list = {}
    pinyin = xpinyin.Pinyin()
    deck_info = {'intro': '', 'TS': {'Tintro': '', 'deck': []}, 'T1': {'Tintro': '', 'deck': []},
                 'T2': {'Tintro': '', 'deck': []}, 'T3': {'Tintro': '', 'deck': []}, 'T4': {'Tintro': '', 'deck': []},
                 'T5': {'Tintro': '', 'deck': []}}
    tid = 12607715
    ts_url = 'http://bbs.ngacn.cc/read.php?tid=' + unicode(tid)
    web = requests.session()
    web.trust_env = False
    data = web.get(ts_url)
    # print data.content
    soup = BeautifulSoup(data.content, "html.parser")
    part = 0
    mark = 0
    rank = 0
    deck = {}
    kind = 'TS'
    deck_name = ''
    for string in soup.p.stripped_strings:
        string = d_format(string)
        print string
        if part == 0:
            if len(string) > 3 and string[2] == '：':
                temp = string.split('：')
                deck_info[temp[0]]['Tintro'] = temp[1]
            if string == '本期简介':
                part = 1
        elif part == 1:
            if string == '本期TS周报分级和走势为：':
                mark = 2
            if mark == 1:
                deck_info['intro'] += string
            elif mark == 2 and string != '本期TS周报分级和走势为：':
                temp = string.split('：')
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
                if temp[0] == 'T5':
                    mark = 3
                    rank = 0
            elif mark == 3:
                # print deck_name
                if len(string) == 4 and string.startswith('T') and string.endswith('卡组'):
                    kind = string[:2]
                if 0 < len(string) < 6 and string[-1] in ['法', '德', '战', '牧', '术', '园', '贼', '猎', '萨', '骑']:
                    if deck_name:
                        deck_info = update_deck(deck, deck_info)
                    deck_name = string
                    deck = get_deck(deck_name, deck_info)
                if string.endswith('.png'):
                    imgUrl = r'http://img.ngacn.cc/attachments' + string[string.index('/'):]
                    deck['imgUrl'] = imgUrl
                    img = requests.get(imgUrl, stream=True)
                    # print deck['name'], pinyin.get_pinyin(deck['name'], '')
                    with open('src/' + kind + '-' + pinyin.get_pinyin(deck_name, '') + '.png', str('wb')) as png:
                        for chunk in img.iter_content(chunk_size=1024):
                            if chunk:  # filter out keep-alive new chunks
                                png.write(chunk)
                                png.flush()
                        deck['imgSrc'] = 'https://longlang.github.io/deckimg/' + kind + '-' + pinyin.get_pinyin(
                            deck_name, '') + '.png'
                    rank = 1
                if string.startswith('套牌代码：'):
                    rank = 3
                    deck['code'] = string.split('：')[1]
                if string.startswith('对阵快攻：'):
                    rank = 3
                    deck['toFast'] = string.split('：')[1]
                if string.startswith('对阵控制：'):
                    deck['toControl'] = string.split('：')[1]
                if string.startswith('劣势对抗：'):
                    deck['cons'] = string.split('：')[1].split('、')
                if rank == 1 and not string.endswith('.png'):
                    deck['cardIntro'] = deck.get('cardIntro', '') + string

            if '—近期变化—' in string:
                mark = 1
    print json.dumps(deck_info, ensure_ascii=False)
    with codecs.open('src/temp.json', 'a', 'utf-8') as f:
        f.write(json.dumps(deck_info, ensure_ascii=False, indent=4))
