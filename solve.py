# _*_ coding: utf-8 _*_
from __future__ import unicode_literals

if __name__ == '__main__':
    member = {}
    with open('user.txt', str('r')) as user:
        for line in user.readlines():
            member.update({line.split(',')[0]: line.split(',')[-2]})
    with open('token.txt', str('r')) as token, open('member.txt', str('w+')) as mem:
        temp = []
        for line in token.readlines():
            temp.append(line[:-1] + ',' + member.get(line.split(',')[0]) + '\n')
        mem.writelines(temp)
