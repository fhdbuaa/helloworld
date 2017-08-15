# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
import requests
import time
import hashlib
from redis import Redis
import multiprocessing


def reg_login(post, head):
    get_code = requests.post(http + urls[0], headers=head, data=post)
    # response = {"status": 0, "msg": "请求成功",
    #             "data": {"codeId": "5D3A0A35B17E47D08E22CC6CBB0FD654", "requestId": "640459dbcf9e4dab99389d989411c37d"}}
    text = get_code.json()
    # print text.get('msg')
    redi = Redis(host='10.0.0.31', port=6379)
    try:
        code = redi.get('mpassport_user_sms_code_' + text['data']['codeId'])
        # print data.get('mobile'), code
        reg = {'mobile': post.get('mobile'), 'code': code, 'codeId': text['data']['codeId'], 'password': '123456',
               'confirmPassword': '123456', 'requestId': text['data']['requestId'], 'platInfo': 3,
               'recruitEmployeeNo': '666666', 'recruitEmployeeName': 'Joey Doe'}
        register = requests.post(http + urls[2], headers=head, data=reg)
        print register.url, reg
        regi = register.json()
        print 'register', regi['msg']
        if regi.get('data', {}).get('memberNo', None):
            log = {'mobile': post.get('mobile'), 'password': '123456', 'platInfo': 3}
            login = requests.post(http + urls[5], headers=head, data=log)
            logi = login.json()
            print 'login', logi['msg']
            if logi.get('data', {}).get('result', False):
                return post.get('mobile') + ',' + regi.get('data', {}).get('memberNo') + ',' + '3' + \
                       ',' + logi.get('data', {}).get('token') + '\n'
        return ''
    except KeyError, e:
        print e, mobile
        return ''


def write_token(word):
    with open('logout.txt', str('a')) as f:
        f.write(str(word))


if __name__ == '__main__':
    time.sleep(0)
    secret_key = '7121E9263A4D2BD3DDADE00B23A8C57B7B61D83702C27F464CE6716E64050CAB'
    http = r'http://192.168.55.183:8604'
    urls = [r'/member/getCode', r'/member/validateCode', r'/member/register', r'/member/fasterRegister',
            r'/member/getMemberByToken', r'/member/login', r'/member/loginByCode', r'/member/checkOldMobile',
            r'/member/validateOldMobileCode', r'/member/checkNewMobile', r'/member/updateMobile',
            r'/member/updateHeadUrl', r'/member/updateUserName', r'/member/logout', r'/member/logoutAll',
            r'/member/queryIsConvert', r'/member/saveConvert', r'/points/query/history', r'/points/get/points',
            r'/points/exchange', r'/points/exchange/rollback', r'/points/add/points', r'/points/exchange/sendVerCode']
    header = {'Content-type': r'application/x-www-form-urlencoded;charset=utf-8', 'X-Timestamp': '', 'sc': 'memberapi',
              'pwd': '123456', 'X-Verifycode': '', 'X-Forwarded-For': '192.168.218.76'}
    now = unicode(int(time.time()))
    verify_code = hashlib.md5()
    verify_code.update(now + secret_key + 'memberapi123456')
    header.update({'X-Verifycode': verify_code.hexdigest(), 'X-Timestamp': now})

    pool = multiprocessing.Pool(10)
    for mobile in xrange(23700420001, 23700420201):
        pool.apply_async(func=reg_login, args=({'mobile': unicode(mobile)}, header), callback=write_token)
    pool.close()
    pool.join()
