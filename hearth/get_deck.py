# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
import requests, datetime

if __name__ == '__main__':
    date = datetime.date.today()
    ts_url = 'https://tempostorm.com/hearthstone/meta-snapshot/standard/' + date.strftime('%Y-%m-%d')
    web = requests.session()
    web.trust_env = False
    data = web.get(ts_url)
    print data.content.decode()
    print ts_url
    pass
