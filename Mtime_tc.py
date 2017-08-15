# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urllib import urlencode, unquote
from urllib2 import Request, urlopen

import json
from Crypto.Random import random


class UrlError(Exception):
    pass


class WrongData(Exception):
    pass


def geturl(url, dic, http=r'http://wdapitest.wandafilm.com/sitapi/thirdparty'):
    request_url = http + url + '?' + urlencode(dic)
    print unquote(request_url)
    print request_url
    return request_url


def include(dic_a, dic_b):
    diff = {}
    for key in dic_b:
        if dic_a.get(key) != dic_b[key]:
            diff.update({key: [dic_a.get(key), dic_b[key]]})
    return diff


def getresponse(url, dic):
    try:
        request_url = Request(url)
        response = urlopen(request_url)
        response_data = json.loads(response.read())
        print response_data
    except Exception, out:
        print out
        raise UrlError
    diff = include(response_data, dic)
    pass_data = ['order', 'ticketstate', 'orderstatus']
    if diff == {}:
        for keyword in pass_data:
            if keyword in response_data:
                list_ = response_data.items()
                list_.append(response_data.get(keyword))
                return list_
        if 'data' in response_data:
            return response_data.get('data')
        elif 'user' in response_data:
            list_ = response_data.items()
            list_.append(response_data.get('user').get('uid'))
            return list_
        else:
            return response_data.items()
    else:
        print diff
        raise UrlError


def form_dic(url_list, url):
    dic = {}
    for key in url_list:
        dic.update({key: url})
    return dic


def perform(request_list):
    body = {'clientid': 'TAOBAO', 'verifycode': r'30ad8nUZXX/eWN4Gos29WKSxIYHC9yB/bdb8Dp+zCilxYFylv++PdFjSUi5MUYGA',
            'clienttype': 2}
    # TODO:AES code calculated
    assertion = request_list[2]
    req_url = request_list[0]
    req_body = body
    req_body.update(request_list[1])
    url_dic = form_dic(info_list, r'/info/')
    url_dic.update(form_dic(user_list, r'/user/'))
    url_dic.update(form_dic(trade_list, r'/trade/'))
    url_dic.update(form_dic(pay_list, r'/trade/'))
    if req_url not in url_dic:
        return False
    try:
        response = getresponse(geturl(url_dic[req_url] + req_url, req_body), assertion)
        if isinstance(response, dict):
            response = response.items()
        try:
            update_dic_data(req_url, response)
        except WrongData:
            print "Update job fails while url is %r" % req_url
        if response != [] and req_url != 'cinemahallsections':
            print random.choice(response)
        if req_url == 'cinemahallsections':
            print response
        return True
    except UrlError:
        return False


def clear(dic):
    if not dic:
        return dic
    for seat in dic:
        del seat['available']
        del seat['status']
        del seat['hallid']
        del seat['cinemaid']
        del seat['sectionid']
        del seat['damaged']
        del seat['type']
    return dic


def form_req(seq):
    i = {}
    keyword = {'createorderwithmobile': 'seat', 'createorder': 'seat', }
    for key in seq[1]:
        if isinstance(key, str):
            if key in data_dic:
                i.update({key: data_dic[key]})
            else:
                raise WrongData
        else:
            available = data_dic.get('available_seat')
            not_available = data_dic.get('not_available_seat')
            clear(available)
            clear(not_available)
            try:
                i.update({keyword[seq[0]]: str(
                    random.sample(available, key["seat"][0]) + random.sample(not_available, key["seat"][1])).replace(
                    " ", "")})
            except:
                raise WrongData
    i.update(seq[2])
    reform = [seq[0], i, seq[3]]
    return reform


def update_dic_data(url, response_data=None):
    if response_data is None:
        response_data = []
    if response_data:
        record = random.choice(response_data)
        try:
            if url == 'cities':
                data_dic.update({"cityid": record["city"]["cid"]})
                return True
            if url == 'cinemas':
                data_dic.update({"cinemaid": record["cinema"]["cid"], "cityid": record["cinema"]["city"]["cid"]})
                return True
            if url == 'films':
                data_dic.update({"filmid": record["film"]["fid"], "dimen": record["film"]["dimen"]})
                return True
            if url == 'salefilms':
                data_dic.update({"filmid": record["film"]["fid"], "dimen": record["film"]["dimen"]})
                return True
            if url == 'filmsessions':
                data_dic.update({"filmid": record["filmsession"]["filmid"],
                                 "showdate": record["filmsession"]["showdate"]})
                return True
            if url == 'filmshows':
                data_dic.update({"filmid": record["show"]["fid"], 'serviceprice': record["show"]["serviceprice"],
                                 'hallid': record["show"]['hall']['hid'], 'cinemaid': record["show"]['hall']['cid'],
                                 'realpayprice': record["show"]["onlineprice"], "showid": record["show"]["sid"]})
                return True
            if url == 'cinemahallseats' or url == 'cinemahallphysicalseats':
                available_seat = []
                not_available_seat = []
                for seat in response_data:
                    if seat.get("available") == 1 and seat.get('type') == 'N' and seat.get('damaged') == 0:
                        available_seat.append(seat)
                    else:
                        not_available_seat.append(seat)
                data_dic.update({'available_seat': available_seat, 'not_available_seat': not_available_seat})
                return True
            if url == 'loginorregister':
                data_dic.update({'uid': response_data[-1]})
                return True
            if url == 'orders':
                data_dic.update({'orderid': record['order']['oid']})
                return True
            if url == 'filmshowreminds':
                data_dic.update(
                    {"filmid": record["filmsession"]["filmid"], "showdate": record["filmsession"]["showdate"]})
                return True
            if url == 'createorderwithmobile' or url == 'createorder' or url == 'orderdetail':
                data_dic.update({'orderid': response_data[-1]['oid'], 'realpayprice': response_data[-1]['totalprice'],
                                 'filmid': response_data[-1]['show']['fid'],
                                 'orderstate': response_data[-1]['orderstate'],
                                 'showid': response_data[-1]['show']['sid'], 'paystate': response_data[-1]['paystate']})
                return True
            if url == 'paysuccess':
                data_dic.update({'ticketstate': response_data[-1]})
                return True
            if url == 'orderstatus':
                if isinstance(response_data[-1], int):
                    data_dic.update({'orderstatus': response_data[-1]})
                return True
            if url == 'querycommodities' or url == 'sellcards':
                if isinstance(record, tuple):
                    record = record[1]
                data_dic.update(
                    {'cardnumber': record.get('card').get('cid'), 'cardtype': record.get('card').get('type')})
                return True
            return True
        except:
            raise WrongData
    return True


address = r'C:\document\data' + '\\'
name = 'SingleRequest.txt'
data = open(address + name)
req_list = data.readlines()
info_list = ['cinemahallphysicalseats', 'salefilms', 'filmdetail', 'cities', 'cinemas', 'cinemadetail', 'films',
             'filmsessions', 'filmshows', 'cinemahallsections', 'cinemahallseats']
user_list = ['loginorregister', 'smsauthcode', 'operatefilm', 'orders', 'filmshowreminds']
trade_list = ['createorderwithmobile', 'paysuccess', 'createorder', 'orderdetail', 'orderstatus', 'cancelorder',
              'pickupticketcode', 'refundorder', 'querycommodities', 'querycardinfo', 'sellcards', 'querycardorder',
              'queryreturnfee', 'queryrefundinfo', 'queryfavor', 'querypaymode', 'queryorderpoint',
              'queryordercoupons', 'querycoupon', 'lockcoupongifts', 'lockcoupons', 'cancelcouponseat',
              'cancelcoupon', 'cancelcoupongifts', 'invalidcoupon', 'renewcoupon', 'cancelcardfavor',
              'cancelpoint', 'usepoint', 'usediscountcard', 'usedebitcard', 'usefrequencycard', 'usefavoractivity',
              'payfree', 'paydebitcard', ]
pay_list = []
# TODO:pay sign md5 calculated
success = 0
fail = 0
fail_list = []
data_dic = {}
for req in req_list:
    request = json.loads(req)
    if len(request) == 4:
        try:
            request = form_req(request)
        except WrongData:
            print r"Case Doesn't Pass"
            fail += 1
            fail_list.append(success + fail)
            continue
    try:
        result = perform(request)
    except:
        result = False
    if result:
        success += 1
        print "Case Passes"
    else:
        fail += 1
        fail_list.append(success + fail)
        print r"Case Doesn't Pass"
print 'Pass:%d Fail:%d' % (success, fail)
print 'Fail Cases Number:%r' % fail_list
print data_dic
