# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
import json

if __name__ == '__main__':
    with open('src/deck.json') as f:
        info = json.loads(f.read())
    for i in info:
        print i, info[i]
