# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
import json
import codecs


def player_info(bs):
    player_id = bs['data-id']
    nation = ''
    name = ''
    scores = bs.find(class_='numbers').string
    rank_change = bs.find(class_='rank-change').i['title']
    rank = bs.find(class_='rank').string
    name_info = bs.find(class_='main no-game').children
    for i, information in enumerate(name_info):
        if i == 0:
            nation = information['title']
        if i == 2:
            name = information.text
    return {'id': player_id, 'rank': rank, 'nation': nation, 'name': name, 'rank_change': rank_change, 'scores': scores}


def get_details(player_id):
    print 'http://www.gosugamers.net/rankings/show/player/' + player_id
    details = BeautifulSoup(requests.get('http://www.gosugamers.net/rankings/show/player/' + player_id).content,
                            "html.parser")
    img_url = 'http://www.gosugamers.net'+details.find(class_='rank-image')['style'].split("'")[1]
    full_name = details.find(class_='sub-header').text
    print {'img_url': img_url, 'full_name': full_name}
    return {'img_url': img_url, 'full_name': full_name}


def download_img(name, img_url):
    img = requests.get(img_url, stream=True)
    # print deck['name'], pinyin.get_pinyin(deck['name'], '')
    with open('src/' + name + '.' + img_url.split('.')[-1], str('wb')) as png:
        for chunk in img.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                png.write(chunk)
                png.flush()


if __name__ == '__main__':
    all_pages = set()
    all_players = []
    rank_url = 'http://www.gosugamers.net/hearthstone/rankings'
    web = requests.session()
    web.trust_env = False
    soup = BeautifulSoup(web.get(rank_url).content, "html.parser")
    pages = soup.find(class_='pages').find_all('a')
    for page in pages:
        all_pages.add(page['href'])
    # print all_pages
    for pg in all_pages:
        soup = BeautifulSoup(web.get('http://www.gosugamers.net' + pg).content, "html.parser")
        for info in soup.find_all(class_='ranking-link'):
            player = player_info(info)
            # detail = get_details(player['id'])
            print player
            all_players.append(player)
    # print get_details(all_players[0]['id'])
    with codecs.open('src/rank.json', 'a', 'utf-8') as f:
        f.write(json.dumps(all_players, ensure_ascii=False, indent=4))
