# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
import requests
import time
import hashlib
import collections
import json
from redis import Redis
import multiprocessing


def register(data, header):
    response = requests.post(http + urls[2], headers=header, data=data)
    # response = {"status": 0, "msg": "请求成功",
    #             "data": {"codeId": "5D3A0A35B17E47D08E22CC6CBB0FD654", "requestId": "640459dbcf9e4dab99389d989411c37d"}}
    print data.get('mobile'), json.loads(response.text).get('msg')
    return response.text


def exchange(post, head):
    print https + urls[-4], head, post
    try:
        response = requests.post(https + urls[-4], headers=head, data=post)
        # print response.text
        result = response.json()
        print result.get('data', {}).get('serialNo', None)
        if result.get('data', {}).get('serialNo', None):
            print post.get('memberNo')
            return str(post.get('memberNo') + ',' + result.get('data', {}).get('serialNo', None) + '\n')
        return ''
    except Exception, e:
        print e
        return ''


def get_code(post, head):
    response = requests.post(http + urls[0], headers=head, data=post)
    # print data.get('mobile'), json.loads(response.text).get('msg')
    result = json.loads(response.text)
    if result.get('status', -1) == 0:
        redi = Redis(host='10.0.0.31', port=6379)
        try:
            print post.get('mobile')
            code = redi.get('mpassport_user_sms_code_' + result['data']['codeId'])
            return str(post.get('mobile') + ',' + ',' + result['data']['codeId'] + ','
                       + result['data']['requestId'] + ',' + code + '\n')
        except KeyError:
            print result.get('msg', 'No error msg!'), result
            return ''
    return ''


def login(post, head):
    response = requests.post(http + urls[5], headers=head, data=post)
    result = json.loads(response.text)
    if result.get('status', -1) == 0 and result.get('data', {}).get('result', False):
        try:
            print post.get('mobile') + ',' + unicode(result['data']['userId']) + ',' + result['data']['token']
            return str(post.get('mobile') + ',' + unicode(result['data']['userId']) + ','
                       + result['data']['token'] + '\n')
        except KeyError:
            print result.get('msg', 'No error msg!'), result
            return ''
    return ''


def send_ver_code(post, head):
    response = requests.post(https + urls[-1], headers=head, data=post)
    result = response.json()
    if result.get('status', -1) == 0 and result.get('data', {}).get('result', False):
        try:
            print post.get('mobile') + ',' + unicode(result['data']['code'])
            return str(post.get('mobile') + ',' + unicode(result['data']['code']) + '\n')
        except KeyError:
            print result.get('msg', 'No error msg!'), result
            return ''
    return ''


def send_old_code(post, head):
    response = requests.post(http + urls[7], headers=head, data=post)
    result = response.json()
    # print result
    if result.get('status', -1) == 0 and result.get('data', {}).get('codeId', False):
        redi = Redis(host='10.0.0.31', port=6379)
        try:
            code = redi.get('mpassport_user_sms_code_' + result['data']['codeId'])
            s = [post.get('mobile'), post.get('token'), unicode(result['data']['codeId']),
                 unicode(result['data']['requestId']), unicode(code)]
            print ','.join(s)
            return str(','.join(s) + '\n')
        except KeyError:
            print result.get('msg', 'No error msg!'), result
            return ''
    else:
        print result['msg']
    return ''


def send_new_code(post, head):
    temp = {'mobile': post.get('mobile'), 'loginIp': post.get('loginIp')}
    response = requests.post(http + urls[9], headers=head, data=temp)
    result = response.json()
    if result.get('status', -1) == 0 and result.get('data', {}).get('codeId', False):
        redi = Redis(host='10.0.0.31', port=6379)
        try:
            code = redi.get('mpassport_user_sms_code_' + result['data']['codeId'])
            print code
            s = [post.get('mobile'), post.get('token'), unicode(result['data']['codeId']),
                 unicode(result['data']['requestId']), unicode(code), unicode(int(post.get('mobile')) - 1000000),
                 post.get('memberNo').strip()]
            print ','.join(s)
            return str(','.join(s) + '\n')
        except KeyError:
            print result.get('msg', 'No error msg!'), result
            return ''
    else:
        print result['msg']
    return ''


def login_worker(*args):
    for x in args:
        data['mobile'] = x
        get_code(data, header)


def write_code(word):
    file = 'token.txt'
    print word
    with open(file, 'a') as log:
        log.write(word)


def write_points(word):
    file = 'exchange.txt'
    print word
    with open(file, 'a') as log:
        log.write(word)


def write_vercode(word):
    file = 'vercode.txt'
    # print word
    with open(file, 'a') as log:
        log.write(word)


def write_oldcode(word):
    file = 'CheckOldMobile.txt'
    # print word
    with open(file, 'a') as log:
        log.write(word)


def write_newcode(word):
    file = 'CheckNewMobile.txt'
    # print word
    with open(file, 'a') as log:
        log.write(word)


def lock(post, head):
    # print head
    temp = post
    try:
        response = requests.get('http://voucher.qas.cmc.com/voucher/lock', headers=head, params=temp)
        result = response.json()
        # print result
        if result.get('status', -1) == 0 and result.get('data', {}).get('lock_no', False):
            print result.get('data', {}).get('lock_no', False)
            return result.get('data', {}).get('lock_no', False) + '\n'
        else:
            print result['msg']
    except Exception, e:
        print e
    return ''


def sellcards(post, head):
    # print head
    temp = post
    try:
        response = requests.get('http://card.qas.cmc.com/card/sellcards', headers=head, params=temp)
        result = response.json()
        # print result
        if result.get('status', -1) == 0 and result.get('data', {}).get('card_infos', False):
            info = result.get('data', {}).get('card_infos')[0]
            print info
            return info.get('card_number') + ',' + info.get('card_pwd') + ',' + info.get('card_v_pwd') + '\n'
        else:
            print result['msg']
    except Exception, e:
        print e
    return ''


def write_lock(word):
    file = 'lock_no.txt'
    # print word
    with open(file, 'a') as log:
        log.write(word)


def write_cards(word):
    file = 'cards.txt'
    # print word
    with open(file, 'a') as log:
        log.write(word)


if __name__ == '__main__':
    secret_key = '7121E9263A4D2BD3DDADE00B23A8C57B7B61D83702C27F464CE6716E64050CAB'
    http = r'http://192.168.55.183:8604'
    https = r'http://192.168.55.183:9351/api'
    urls = [r'/member/getCode', r'/member/validateCode', r'/member/register', r'/member/fasterRegister',
            r'/member/getMemberByToken', r'/member/login', r'/member/loginByCode', r'/member/checkOldMobile',
            r'/member/validateOldMobileCode', r'/member/checkNewMobile', r'/member/updateMobile',
            r'/member/updateHeadUrl', r'/member/updateUserName', r'/member/logout', r'/member/logoutAll',
            r'/member/queryIsConvert', r'/member/saveConvert', r'/points/query/history', r'/points/get/points',
            r'/points/exchange', r'/points/exchange/rollback', r'/points/add/points', r'/points/exchange/sendVerCode', ]
    header = {'Content-type': r'application/x-www-form-urlencoded;charset=utf-8', 'X-Timestamp': '', 'sc': 'memberapi',
              'pwd': '123456', 'X-Verifycode': '', 'X-Forwarded-For': '192.168.218.76'}
    now = unicode(int(time.time()))
    verify_code = hashlib.md5()
    verify_code.update(now + secret_key + 'memberapi123456')
    header.update({'X-Verifycode': verify_code.hexdigest(), 'X-Timestamp': now})
    data = {}
    api = -99

    if api == 2:
        with open(r"code.txt", 'r') as f, open(r"user.txt", 'a') as r:
            for line in f.readlines():
                temp = line.split(',')
                data['mobile'] = temp[0]
                data['codeId'] = temp[1]
                data['code'] = temp[3][:-1]
                data['password'] = '123456'
                data['confirmPassword'] = '123456'
                data['requestId'] = temp[2]
                data['platInfo'] = '2'
                data['recruitEmployeeNo'] = '666666'
                data['recruitEmployeeName'] = 'John Doe'
                response = json.loads(register(data, header)).get('data', {})
                if response.get('result'):
                    print response.get('memberNo'), response.get('userId')
                    r.write(str(line[:-1]) + ',' + str(
                        response.get('memberNo') + ',' + unicode(response.get('userId'))) + '\n')
    elif api == 0:
        with open(r'user.txt', 'r') as user:
            pool = multiprocessing.Pool(15)
            for x in user.readlines():
                temp = {'mobile': x.split(',')[0]}
                pool.apply_async(func=get_code, args=(temp, header), callback=write_code)
            pool.close()
            pool.join()
    elif api == 5:
        with open(r'user.txt', 'r') as user:
            pool = multiprocessing.Pool(5)
            for x in user.readlines():
                temp = {'mobile': x.split(',')[0], 'password': '123456', 'platInfo': '2'}
                pool.apply_async(func=login, args=(temp, header), callback=write_code)
            pool.close()
            pool.join()
    elif api == 19:
        with open(r'points.txt', 'r') as points:
            pool = multiprocessing.Pool(10)
            for x in points.readlines():
                string = x.strip().split(',')
                temp = {'memberNo': string[3], 'points': 1, 'cinemaCode': '1024', 'opeType': 2, 'memo': 'perform test',
                        'updateUser': 'John Doe', 'sourceId': unicode(int(time.time()))}
                pool.apply_async(func=exchange, args=(temp, header), callback=write_points)
            pool.close()
            pool.join()
    elif api == -1:
        with open(r'user.txt', 'r') as user:
            pool = multiprocessing.Pool(10)
            for x in user.readlines():
                temp = {'mobile': x.split(',')[0]}
                pool.apply_async(func=send_ver_code, args=(temp, header), callback=write_vercode)
            pool.close()
            pool.join()
    elif api == 7:
        with open(r'member.txt', 'r') as member:
            pool = multiprocessing.Pool(10)
            for x in member.readlines():
                temp = {'mobile': x.split(',')[0], 'token': x.split(',')[2]}
                pool.apply_async(func=send_old_code, args=(temp, header), callback=write_oldcode)
            pool.close()
            pool.join()
    elif api == 9:
        with open(r'member.txt', 'r') as member:
            pool = multiprocessing.Pool(10)
            for x in member.readlines():
                temp = {'mobile': unicode(int(x.split(',')[0]) + 1000000), 'loginIp': '127.0.0.1',
                        'token': x.split(',')[2], 'memberNo': x.split(',')[3]}
                pool.apply_async(func=send_new_code, args=(temp, header), callback=write_newcode)
            pool.close()
            pool.join()
    # count = collections.Counter(result)
    # for key,value in count.items():
    #     print json.loads(key).get('msg'),value
    elif api == -100:
        with open(r'./data/vouchers4.txt', 'r') as vouchers:
            pool = multiprocessing.Pool(50)
            for x in vouchers.readlines():
                temp = dict(channel='01', order_id='tests%r' % int(x.strip()), order_type='T',
                            film_info='[{"perform_id":"C304201706300000030","ticket_type_id":"2000000331",' +
                                      '"type_name":"test099","ticket_num":1,"voucher_number":"%r"}]' % int(x.strip()),
                            sale_channel='QD010319')
                header = {'sc': 'activity', 'X-Timestamp': '1492505817', 'Connection': 'keep-alive', 'pwd': '123457',
                          'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
                          'X-Verifycode': '9ffa9ddc17d108d0fef1264ada592441', }
                pool.apply_async(func=lock, args=(temp, header), callback=write_lock)
            pool.close()
            pool.join()
    elif api == -99:
        with open(r'./cards/cinemas.txt', 'r') as cinema:
            cinemas = cinema.readlines()[:]
            pool = multiprocessing.Pool(1)
            for count in xrange(300):
                x = cinemas[count % 11]
                temp = dict(cinema_code=x.strip(), sales_channel='QD010319', type_code='1200000820',
                            sales_order=100001 + count, sales_price_sum=0, sales_num=1, mobile_no='13716095648')
                header = {'sc': 'activity', 'X-Timestamp': '1492505817', 'Connection': 'keep-alive', 'pwd': '123457',
                          'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
                          'X-Verifycode': '9ffa9ddc17d108d0fef1264ada592441', }
                pool.apply_async(func=sellcards, args=(temp, header), callback=write_cards)
            pool.close()
            pool.join()
