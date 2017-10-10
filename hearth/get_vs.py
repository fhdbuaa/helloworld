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


if __name__ == '__main__':
    char = {'潜行者': 'Rogue', '牧师': 'Priest', '德鲁伊': 'Druid', '术士': 'Warlock', '猎人': 'Hunter', '法师': 'Mage',
            '萨满': 'Shaman', '圣骑士': 'Paladin', '战士': 'Warrior', '天梯环境': 'Environment', '强度排序': 'Rank'}
    exceptions_list = {}
    pinyin = xpinyin.Pinyin()
    deck_info = {'Environment': {}, 'Rogue': [], 'Priest': [], }
    tid = 12582689
    ts_url = 'http://bbs.nga.cn/read.php?tid=' + unicode(tid)
    web = requests.session()
    web.trust_env = False
    data = web.get(ts_url)
    # print data.content
    soup = BeautifulSoup(data.content, "html.parser")
    title = ''
    temp = {'png': [], 'info': ''}
    i = 0
    for string in soup.p.stripped_strings:
        string_ = d_format(string)
        if '[h]' in string:
            title = string_
            temp = {'png': [], 'info': ''}
            i = 0
        print string, '====', title
        if title in char and '[h]' not in string:
            if string_.endswith('.png'):
                imgUrl = r'http://img.ngacn.cc/attachments' + string_[string_.index('/'):]
                img = requests.get(imgUrl, stream=True)
                with open('vs/' + char[title] + '-' + unicode(i) + '.png', str('wb')) as png:
                    for chunk in img.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            png.write(chunk)
                            png.flush()
                    temp['png'] += [char[title] + '-' + unicode(i) + '.png']
                    i += 1
            else:
                temp['info'] += string_
            deck_info[char[title]] = temp
    print json.dumps(deck_info, ensure_ascii=False)
    with codecs.open('vs/vs.json', 'wb', 'utf-8') as f:
        f.write(json.dumps(deck_info, ensure_ascii=False, indent=4))
