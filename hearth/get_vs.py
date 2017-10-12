# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
import json
import codecs
import tinify
import os


def d_format(word):
    while '[' in word:
        a = word.index('[')
        b = word.index(']')
        word = word[:a] + word[b + 1:]
    return word.strip('=')


def save_img(url, key, unique):
    print url
    img = requests.get(url, stream=True)
    if img.status_code == 200:
        source = tinify.from_url(url)
        source.to_file('vs/' + unicode(tid) + '/' + char[key] + '-' + unicode(unique) + '.png')
        return char[key] + '-' + unicode(unique) + '.png'
    else:
        return ''


char = {'潜行者': 'Rogue', '牧师': 'Priest', '德鲁伊': 'Druid', '术士': 'Warlock', '猎人': 'Hunter', '法师': 'Mage',
        '萨满': 'Shaman', '圣骑士': 'Paladin', '战士': 'Warrior', '天梯环境': 'Environment', '强度排序': 'Rank'}
tinify.key = 'm1wfTSfLD9GUu5uJ9iPLUW3H6dTEUhA3'
if __name__ == '__main__':
    deck_info, temp, title, i = {}, {'png': [], 'info': ''}, '', 0
    tid = 12582689
    if not os.path.exists('vs/' + unicode(tid)):
        os.mkdir('vs/' + unicode(tid))
    vs_url = 'http://bbs.nga.cn/read.php?tid=' + unicode(tid)
    web = requests.session()
    web.trust_env = False
    soup = BeautifulSoup(web.get(vs_url).content, "html.parser")
    for string in soup.p.stripped_strings:
        string_ = d_format(string)
        if '[h]' in string:
            title = string_
            temp = {'png': [], 'info': ''}
            i = 0
        print string, '====', title
        if title in char and '[h]' not in string:
            if string_.endswith('.png') and string_.startswith('./'):
                imgUrl = r'http://img.ngacn.cc/attachments' + string_[string_.index('/'):]
                temp['png'] += ['http://longlang.oschina.io/' + save_img(imgUrl, title, i)]
                i += 1
            elif not string_.endswith('.png'):
                temp['info'] += string_
            deck_info[char[title]] = temp
    print json.dumps(deck_info, ensure_ascii=False)
    with codecs.open('vs/' + unicode(tid) + '/vs.json', 'wb', 'utf-8') as f:
        f.write(json.dumps(deck_info, ensure_ascii=False, indent=4))
