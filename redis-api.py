# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import multiprocessing
import random
import string

import requests
import requests.exceptions


def red(key, value):
    ret = [0, 0]
    try:
        set_url = 'http://192.168.55.155:8311/sensitiveword/setredis?key=' + key + '&value=' + value
        print set_url
        set_req = requests.get(set_url, timeout=20)
        print set_req.json()
        if set_req.json().get('msg') != 'OK':
            ret[0] = key
            print key, value
        get_url = 'http://192.168.55.155:8311/sensitiveword/getredis?key=' + key
        print get_url
        get_req = requests.get(get_url, timeout=20)
        print get_req.json()
        if get_req.json().get('msg') != value:
            ret[1] = key + ' ' + get_req.json().get('msg')
            print key, get_req.json().get('msg')
        return ret
    except [requests.exceptions.RequestException, ValueError]:
        return [1, 1]


def write_token(word):
    print word
    with open('redis.txt', str('a')) as f:
        if word[0] or word[1]:
            f.write(str(word + '\n'))


if __name__ == "__main__":
    pool = multiprocessing.Pool(5)
    for x in xrange(10000):
        keys = ''.join(random.sample(string.ascii_letters + string.digits, 6))
        values = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        print keys, values
        pool.apply_async(func=red, args=(keys, values), callback=write_token)
    pool.close()
    pool.join()
